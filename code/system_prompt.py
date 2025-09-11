import json
from pathlib import Path
from functools import lru_cache

GENERIC_PROMPT_PATH = Path(__file__).parent / "prompts" / "generic_prompt.json"

@lru_cache()
def get_generic_prompt_data():
    with open(GENERIC_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_generic_prompt():
    return get_generic_prompt_data()["system"]

SALES_PROMPT_PATH = Path(__file__).parent / "prompts" / "sales_prompt.json"

@lru_cache()
def get_sales_prompt_data():
    with open(SALES_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_sales_prompt():
    prompt_parts = get_sales_prompt_data()["system"]
    # Join all parts and format with the actual message
    sales_prompt = "\n".join(prompt_parts)
    return sales_prompt




NAME_PROMPT_PATH = Path(__file__).parent / "prompts" / "name_prompt.json"

@lru_cache()
def get_name_prompt_data():
    with open(NAME_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_name_prompt():
    prompt_parts = get_name_prompt_data()["system"]
    # Join all parts and format with the actual message
    name_prompt = "\n".join(prompt_parts)
    return name_prompt

INFO_PROMPT_PATH = Path(__file__).parent / "prompts" / "info_prompt.json"

@lru_cache()
def get_info_prompt_data():
    with open(INFO_PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_info_prompt():
    prompt_parts = get_info_prompt_data()["system"]
    # Join all parts and format with the actual message
    info_prompt = "\n".join(prompt_parts)
    return info_prompt