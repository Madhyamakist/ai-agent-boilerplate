from config import max_input_length

def validate_input(input):
    """Validates the chat user input. Returns (is_valid, message)."""
    input = input.strip()
    if not input:
        return False, "Please enter a message before sending."
    if len(input) > max_input_length:
        return False, f"Your message is too long. Please limit to {max_input_length} characters."
    return True, ""
