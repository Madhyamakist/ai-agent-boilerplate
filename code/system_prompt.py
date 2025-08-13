import json
from pathlib import Path
from functools import lru_cache

SALES_PROMPT_PATH = Path(__file__).parent / "prompts" / "sales_prompt.json"

@lru_cache()
def get_system_prompt_data():
    with open(SALES_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_system_prompt():
    return get_system_prompt_data()["system"]



NAME_PROMPT_PATH = Path(__file__).parent / "prompts" / "name_prompt.json"

@lru_cache()
def get_name_prompt_data():
    with open(NAME_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_name_prompt():
    return get_name_prompt_data() 
