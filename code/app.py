import os
from flask import Flask, render_template, request, jsonify
from llm_api import get_groq_response
from validators import validate_input
from config import DEBUG
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

#render HTML frontend
@app.route('/')
def chat():
    return render_template('chat.html')

#Rendering response
# chat_api is a Flask route function defined that acts as the backend API endpoint for chat exchanges. It is the API endpoint your frontend calls to send user messages and receive chatbot responses.
# It receives a JSON request containing the user's chat input from the frontend, validates the input, sends the validated input to the LLM, and returns a JSON response.

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    input = data.get('input', '')
    session_id = data.get('session_id')
    # Input Validation
    is_valid, message = validate_input(input)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400
    # Get response from LLM
    try:
        bot_response = get_groq_response(input.strip(), session_id)
        return jsonify({'success': True, 'response': bot_response})
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return jsonify({
            'success': False,
            'error': "Sorry, something went wrong while processing your message. Please try again later."}), 500

if __name__ == '__main__':
    app.run(debug=DEBUG,port=5000)