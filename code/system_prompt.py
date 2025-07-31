import json
from pathlib import Path
from functools import lru_cache

PROMPT_PATH = Path(__file__).parent / "prompts" / "sales_prompt.json"

@lru_cache()
def get_system_prompt_data():
    with open(PROMPT_PATH, encoding="utf-8") as f:
        return json.load(f)

def get_system_prompt():
    return get_system_prompt_data()["system"]

def get_few_shot_examples():
    return get_system_prompt_data().get("examples", [])