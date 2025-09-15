from http import HTTPStatus
from config import max_input_length, agent_type
import uuid

def validate_input(input, request_type):
    """Validates the chat user input. Returns (is_valid, message)."""
    input = input.strip()
    if not input:
        return False, "Please enter a message before sending."
    if len(input) > max_input_length:
        return False, f"Your message is too long. Please limit to {max_input_length} characters."
        
    # Normalize and validate request_type
    try:
        request_type = agent_type(request_type.strip().lower()).value  # <-- return string value
    except (ValueError, AttributeError):
        request_type = agent_type.GENERIC.value  # <-- fallback string
    
    return True, request_type

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
            return False, "session_id is required", HTTPStatus.BAD_REQUEST

        # Validate UUID format
        if not is_valid_uuid(session_id):
            return False, "Invalid session_id format", HTTPStatus.BAD_REQUEST
        
        return True, "Valid session_id", HTTPStatus.OK

    except Exception as e:
        print(f"[Error] {e}")
        return False, "Internal Server Error", HTTPStatus.INTERNAL_SERVER_ERROR