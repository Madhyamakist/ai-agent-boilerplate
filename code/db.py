import os
import uuid
import psycopg
from langchain.memory import ConversationBufferMemory
from langchain_postgres import PostgresChatMessageHistory
from config import DATABASE_URL, db_name, table_name

def ensure_database_exists(DATABASE_URL, db_name):
    """
    Connect to the 'postgres' system database. Create db_name if not exists.
    """
    # Parse from URL for creation
    base_url = DATABASE_URL.rsplit('/', 1)[0]
    postgres_url = f"{base_url}/postgres"
        
    # First, ensure the database exists

    with psycopg.connect(postgres_url) as temp_conn:
        temp_conn.autocommit = True
        with temp_conn.cursor() as cur:
            cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
            if not cur.fetchone():
                cur.execute(f'CREATE DATABASE "{db_name}"')
                print(f"Database '{db_name}' created successfully.")
            else:
                print(f"Database '{db_name}' already exists.")


def create_sync_connection(DATABASE_URL):
    """
    Establish a connection to the specified database.
    """
    conn = psycopg.connect(DATABASE_URL)
    conn.autocommit = False
    return conn

def ensure_chat_table_exists(sync_connection, table_name):
    """
    Use LangChain's helper to make sure the chat history table exists.
    """
    PostgresChatMessageHistory.create_tables(sync_connection, table_name)
    print(f"Table '{table_name}' created or verified.")
        # Now add the request_type column if it doesn't exist
    try:
        with sync_connection.cursor() as cur:
            # Check if request_type column exists
            cur.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = %s AND column_name = 'request_type'
            """, (table_name,))
            
            if not cur.fetchone():
                # Add request_type column
                cur.execute(f"""
                    ALTER TABLE {table_name} 
                    ADD COLUMN request_type VARCHAR(50)
                """)
                
                # Add index for better query performance
                cur.execute(f"""
                    CREATE INDEX IF NOT EXISTS idx_{table_name}_request_type 
                    ON {table_name}(request_type)
                """)
                
                sync_connection.commit()
                print(f"Added 'request_type' column to '{table_name}' table.")
            else:
                print(f"Column 'request_type' already exists in '{table_name}' table.")
                
    except Exception as e:
        print(f"Error adding request_type column: {e}")
        sync_connection.rollback()


def ensure_summaries_table_exists(sync_connection):
    """
    Create the chat_info table for storing lead information and summaries.
    """
    try:
        with sync_connection.cursor() as cur:
            # Create the chat_info table
            create_table_query = """
            CREATE TABLE IF NOT EXISTS chat_info (
                id SERIAL PRIMARY KEY,
                session_id TEXT NOT NULL,
                contact_name TEXT,
                created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                metadata JSONB DEFAULT '{}',
                
                -- Add constraint to prevent duplicate summaries for same session
                UNIQUE(session_id)
            );
            
            -- Create indexes for efficient querying
            CREATE INDEX IF NOT EXISTS idx_chat_info_session_id 
            ON chat_info(session_id);
            
            
            CREATE INDEX IF NOT EXISTS idx_chat_info_created_at 
            ON chat_info(created_at);
            """
            
            cur.execute(create_table_query)
            sync_connection.commit()
            print("Table 'chat_info' created/verified successfully.")
            
    except Exception as e:
        print(f"Error creating chat_info table: {e}")

def setup_database_and_table(database_url, table_name):
    """
    Orchestrates DB and table setup, returns the live connection and table name.
    """
    try:
        ensure_database_exists(DATABASE_URL, db_name)
        sync_connection = create_sync_connection(DATABASE_URL)

        ensure_chat_table_exists(sync_connection, table_name)
        ensure_summaries_table_exists(sync_connection)
        return sync_connection, table_name
    except Exception as e:
        print(f"Error setting up database: {e}")
        raise
        

# Usage — get the ready connection and table name
sync_connection, table_name = setup_database_and_table(DATABASE_URL, table_name)
