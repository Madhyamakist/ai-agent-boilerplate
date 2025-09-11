import uuid
from db import sync_connection, table_name
from langchain_postgres import PostgresChatMessageHistory
from llm_api import get_session_history
from config import first_chat_message

def _extract_messages(history):
    messages = []
    for msg in history.messages:
        messages.append({
            "type": msg.type,   # "human" or "ai"
            "content": msg.content
        })
    return messages

def get_history(session_id: str):
    """Retrieve chat history for a session_id as a list of dicts."""
    try:
        history = get_session_history(session_id)
        status = 200
        if not history.messages:
            # session exists
            history.add_ai_message(first_chat_message)
            status = 201
        messages = _extract_messages(history)

        return {
            "session_id": session_id,
            "history": messages
        }, status
    except Exception as e:
        print(f"[get_history Error] {e}")
        return {
            "error": "Network issue loading history.",
            "session_id": session_id
        }, 500

