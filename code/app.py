import os
from flask import Flask, render_template, request, jsonify
from validators import validate_input
from config import DEBUG


app = Flask(__name__)


#render HTML frontend
@app.route('/')
def chat():
    return render_template('chat.html')

#Rendering response
# chat_api is a Flask route function defined that acts as the backend API endpoint for chat exchanges. It is the API endpoint your front end calls to send user messages and receive chatbot responses.
# It receives a JSON request containing the user's chat input from the frontend, validates the input, sends the validated input to the LLM, and returns a JSON response.
@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    input = data.get('input', '').strip()
    is_valid, message = validate_input(input)
    if not is_valid:
        return jsonify({'success': False, 'error': message}), 400

    return jsonify({'success': True, 'response': "Hello"})

if __name__ == '__main__':
    app.run(debug=DEBUG)