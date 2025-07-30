
# Add other constants as needed
import os
from dotenv import load_dotenv
load_dotenv()
# Flask settings
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# DEBUG = os.getenv("DEBUG", "False").strip().lower() == "true"

# debug_str = os.getenv("DEBUG", "False")
# print(f"DEBUG environment variable raw: '{debug_str}'")
# DEBUG = debug_str.strip().lower() == "true"
# Chat input limits
max_input_length = 10000
