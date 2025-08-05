import os
import uuid
import psycopg
from langchain.memory import ConversationBufferMemory
from langchain_postgres import PostgresChatMessageHistory
from config import DATABASE_URL, db_name, table_name

def setup_database_connection():
    """
    Create database connection and setup tables using the langchain_postgres pattern.
    """
    try:
        # Parse from URL for creation
        base_url = DATABASE_URL.rsplit('/', 1)[0]
        postgres_url = f"{base_url}/postgres"
        
        # First, ensure the database exists
        try:
            with psycopg.connect(postgres_url) as temp_conn:
                temp_conn.autocommit = True
                with temp_conn.cursor() as cur:
                    cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
                    if not cur.fetchone():
                        cur.execute(f'CREATE DATABASE "{db_name}"')
                        print(f"Database '{db_name}' created successfully.")
                    else:
                        print(f"Database '{db_name}' already exists.")
        except Exception as e:
            print(f"Warning: Could not create database (may already exist): {e}")
        
        # Establish the main connection to our database
        sync_connection = psycopg.connect(DATABASE_URL)
        
        PostgresChatMessageHistory.create_tables(sync_connection, table_name)
        print(f"Table '{table_name}' created/verified successfully.")
        
        return sync_connection, table_name
        
    except Exception as e:
        print(f"Error setting up database connection: {e}")
        raise

# Initialize database connection and get table name
sync_connection, table_name = setup_database_connection()