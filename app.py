import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv


# Loads .env file

load_dotenv()  

app = Flask(__name__)


#render HTML frontend
@app.route('/')
def chat():
    return render_template('chat.html')

#Rendering response

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    user_input = data.get('user_input', '').strip()

    # Input validation
    if not user_input:
        return jsonify({'success': False, 'error': "Please enter a message before sending."}), 400
    if len(user_input) > 100:
        return jsonify({'success': False, 'error': "Your message is too long. Please limit to 100 characters."}), 400

    try:
        return jsonify({'success': True, 'response': "Hello"})
    except Exception as e:
        # Log the error on server side as needed
        print(f"Error on server side: {e}")
        return jsonify({'success': False, 'error': "Sorry, something went wrong while processing your message. Please try again later."}), 500





if __name__ == '__main__':
    app.run(debug=True)