import uuid

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
            return False, "session_id is required", 400

        # Validate UUID format
        if not is_valid_uuid(session_id):
            return False, "Invalid session_id format", 400
        
        return True, "Valid session_id", 200

    except Exception as e:
        print(f"[Error] {e}")
        return False, "Internal Server Error", 500