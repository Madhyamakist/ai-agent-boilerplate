from config import max_input_length

def validate_input(input):
    """Validates the chat user input. Returns (is_valid, message)."""
    input = input.strip()
    if not input:
        return False, "Please enter a message before sending."
    if len(input) > max_input_length:
        return False, "Your message is too long. Please limit to 10000 characters."
    return True, ""
