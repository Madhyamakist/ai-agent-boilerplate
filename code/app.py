from http import HTTPStatus
import os
from flask import Flask, render_template, request, jsonify
from llm_api import get_groq_response
from validators import validate_input, validate_session_id, validate_update_data
from config import DEBUG
from flask_cors import CORS 
from flask_swagger_ui import get_swaggerui_blueprint
from history import get_history
from leads import get_all_leads
from leads_update import update_lead
app = Flask(__name__)
CORS(app)

# Swagger UI setup
SWAGGER_URL = '/docs'  # URL for exposing Swagger UI
API_URL = '/static/swagger.yaml'  # Path to your swagger file

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Chat API"
    }
)

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

#render HTML frontend
@app.route('/')
def chat():
    return render_template('chat.html')

@app.route("/health", methods=["GET"])
def hello():
    return jsonify({"message": "Hello World"})

# History API to load previous messages while loading the page
@app.route("/history", methods=["GET"])
def history_endpoint():
    session_id = request.args.get("session_id")
    # Validate
    result = validate_session_id(session_id)
    if not result["is_valid"]:
        return jsonify({"error": result["message"]}), result["status"]
    # Continue if valid
    history_data, status = get_history(session_id)
    return jsonify(history_data), status

@app.route('/leads', methods=['GET'])
def get_leads():
    try:
        leads_data, status = get_all_leads()
        return jsonify({"leads":leads_data}), status
    except Exception as e:
        print(f"Error in get_leads endpoint: {e}")
        return jsonify({
            "error": "Unable to fetch chat info. Please try again later."
        }), HTTPStatus.INTERNAL_SERVER_ERROR

@app.route('/chat-info', methods=['PATCH'])
def patch_updates():
    try:
        update_data = request.get_json()
        session_id = update_data.get("session_id")
        status = update_data.get("status")
        remarks = update_data.get("remarks")

        #validate update data
        result = validate_update_data(update_data, session_id, status)
        if not result["is_valid"]:
            return jsonify({"error": result["message"]}), result["status"]
        update_lead(session_id, status, remarks)
        return jsonify({"sucess":True, "message":"Leads updated"}), HTTPStatus.OK
    except Exception as e:
        return jsonify({
            "sucess": False,
            "message": f"Unable to update lead. Please try again later. ({str(e)})"
        }), HTTPStatus.INTERNAL_SERVER_ERROR

#Rendering response
# chat_api is a Flask route function defined that acts as the backend API endpoint for chat exchanges. It is the API endpoint your frontend calls to send user messages and receive chatbot responses.
# It receives a JSON request containing the user's chat input from the frontend, validates the input, sends the validated input to the LLM, and returns a JSON response.

@app.route('/chat', methods=['POST'])
def chat_api():
    data = request.get_json()
    input = data.get('input', '')
    session_id = data.get('session_id')
    request_type = data.get('request_type')
    # Input Validation

    result = validate_input(input, request_type)

    if not result["is_valid"]:
        return jsonify({'success': False, 'error': result["message"]}), HTTPStatus.BAD_REQUEST
    request_type = result["message"] 

    # Get response from LLM
    try:
        bot_response = get_groq_response(input.strip(), session_id, request_type)
        return jsonify({'success': True, 'response': bot_response})
    except Exception as e:
        print(f"Error during LLM call: {e}")
        return jsonify({
            'success': False,
            'error': "Sorry, something went wrong while processing your message. Please try again later."}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=DEBUG,port=5000)


