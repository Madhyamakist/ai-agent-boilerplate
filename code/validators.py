from http import HTTPStatus
from config import max_input_length, agent_type
import uuid

def validate_input(input, request_type):
    """Validates the chat user input. Returns (is_valid, message)."""
    input = input.strip()
    if not input:
        return {"is_valid":False, "message":"Please enter a message before sending."}

    if len(input) > max_input_length:
        return {"is_valid":False, "message":f"Your message is too long. Please limit to {max_input_length} characters."}
        
    # Normalize and validate request_type
    try:
        request_type = agent_type(request_type.strip().lower()).value  # <-- return string value
    except (ValueError, AttributeError):
        request_type = agent_type.GENERIC.value  # <-- fallback string
    return {"is_valid":True, "message":request_type}

def is_valid_uuid(value: str) -> bool:
    """Check if a string is a valid UUID."""
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def validate_session_id(session_id):
    """Validate session_id and return chat history or create new session."""
    try:
        if session_id is None:
            return {"is_valid":False, "message":"session_id is required", "status":HTTPStatus.BAD_REQUEST}
        # Validate UUID format
        if not is_valid_uuid(session_id):
            return {"is_valid":False, "message":"Invalid session_id format", "status":HTTPStatus.BAD_REQUEST}
        return {"is_valid":True, "message":"Valid session_id", "status":HTTPStatus.OK}

    except Exception as e:
        print(f"[Error] {e}")
        return {"is_valid":False, "message":"Internal Server Error", "status":HTTPStatus.INTERNAL_SERVER_ERROR}