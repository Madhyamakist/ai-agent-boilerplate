from config import max_input_length, agent_type

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