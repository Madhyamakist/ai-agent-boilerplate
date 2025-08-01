# Add other constants as needed
import os
from dotenv import load_dotenv
load_dotenv()
# Flask settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Fetch API key and LLM model from environment variable set via .env file
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_MODEL_NAME = os.environ.get("GROQ_MODEL_NAME", "meta-llama/llama-4-scout-17b-16e-instruct")  # default if not set

# Chat input limits
max_input_length = 10000