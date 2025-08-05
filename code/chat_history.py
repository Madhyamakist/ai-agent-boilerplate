import os
import uuid
import psycopg
from langchain.memory import ConversationBufferMemory
from langchain_postgres import PostgresChatMessageHistory
from config import DATABASE_URL

def setup_database_connection():
    """
    Create database connection and setup tables using the langchain_postgres pattern.
    """
    try:
        # Parse database name from URL for creation
        db_name = DATABASE_URL.split('/')[-1]
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
        
        table_name = "chat_history"
        PostgresChatMessageHistory.create_tables(sync_connection, table_name)
        print(f"Table '{table_name}' created/verified successfully.")
        
        return sync_connection, table_name
        
    except Exception as e:
        print(f"Error setting up database connection: {e}")
        raise

# Initialize database connection and get table name
sync_connection, table_name = setup_database_connection()

# Database setup - using a single session for local testing
# Using uuid.uuid4() for unique sessions
SESSION_ID = str(uuid.uuid4()) # for unique sessions
# Initialize the chat history manager using langchain_postgres pattern
postgres_history = PostgresChatMessageHistory(
    table_name,
    SESSION_ID,
    sync_connection=sync_connection
)

# GLOBAL memory object using PostgreSQL backend
memory = ConversationBufferMemory(
    memory_key="chat_history", 
    return_messages=True, 
    chat_memory=postgres_history
)