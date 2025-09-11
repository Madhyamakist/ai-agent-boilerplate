# Add other constants as needed
import os
from dotenv import load_dotenv
from enum import Enum
load_dotenv()
# Flask settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Fetch API key and LLM model from environment variable set via .env file
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")  # default if not set

# Chat input limits
max_input_length = 10000

# Database and table name
db_name = 'chatdb'
table_name  = 'chat_table'
# PostgreSQL Database Configuration
# Local PostgreSQL database (you'll need PostgreSQL installed locally)
# Default connection for local PostgreSQL instance
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:password@localhost:5432/')
DATABASE_URL = DATABASE_URL + db_name
first_chat_message = "Hi, Welcome to smallTech 👋. I'm here to help with any IT-related questions or concerns you might bring. What brings you to our website today?"
class agent_type(str, Enum):
    SALES = "sales"
    GENERIC = "generic"