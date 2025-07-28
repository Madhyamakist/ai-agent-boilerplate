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
    user_input = request.json['user_input']
    try:
        return jsonify({'response': "Hello"})
    except Exception as e:
        return jsonify({'response': f"Error: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
