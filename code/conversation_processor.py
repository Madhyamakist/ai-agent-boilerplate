import json
from datetime import datetime
from db import sync_connection
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL_NAME

def process_conversation(user_input, bot_response, session_id):
    """
    Main hook function that processes each conversation exchange.
    Only processes sessions that don't already have a name detected.
    Uses LLM to detect if user provided their name in the current input.

    """
    try:
        # First check: Does this session already have a name?
        if session_has_name(session_id):
            print(f"[PROCESSOR] Session {session_id} already has name detected. Skipping processing.")
            return
        
        print(f"[PROCESSOR] Processing session {session_id} for name detection...")
        
        # Use LLM to detect if user provided their name
        name_info = detect_name_with_llm(user_input)
        
        if name_info and name_info.get('name_detected', False):
            extracted_name = name_info.get('name', '').strip()
            if extracted_name:
                print(f"[PROCESSOR] Name detected: '{extracted_name}' in session {session_id}")
                
                # Save name to database
                save_name_to_database(session_id, extracted_name, user_input)
                print(f"[PROCESSOR] Name saved for session {session_id}. Future processing will be skipped.")
            else:
                print(f"[PROCESSOR] Name detection indicated positive but no name extracted.")
        else:
            print(f"[PROCESSOR] No name detected in current message for session {session_id}")
        
    except Exception as e:
        print(f"[PROCESSOR] Error in conversation processor: {e}")
        # Don't let processing errors break the chat flow

def session_has_name(session_id):
    """
    Check if a session already has a name detected.
    
    Args:
        session_id (str): Session identifier
        
    Returns:
        bool: True if name already exists for this session, False otherwise
    """
    try:
        # Rollback any pending transaction first
        sync_connection.rollback()
        
        with sync_connection.cursor() as cur:
            cur.execute(
                "SELECT contact_name FROM chat_info WHERE session_id = %s",
                (session_id,)
            )
            result = cur.fetchone()
            return result is not None and result[0] is not None and result[0].strip() != ""
            
    except Exception as e:
        print(f"[PROCESSOR] Error checking for existing name: {e}")
        # Rollback on error to clean transaction state
        try:
            sync_connection.rollback()
        except:
            pass
        return False

def detect_name_with_llm(message):
    """
    Use LLM to detect if the user provided their name in the message.
    
    Args:
        message (str): User's message to analyze
        
    Returns:
        dict: Contains 'name_detected' (bool) and 'name' (str) if found
    """
    try:
        # Create LLM instance for name detection
        llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=GROQ_MODEL_NAME)
        
        # Focused prompt for name detection
        detection_prompt = f"""
You are a name detection assistant. Analyze the following user message and determine if the user is introducing themselves or providing their name.

User message: "{message}"

Rules:
1. Only detect when the user is clearly providing THEIR OWN name
2. Don't extract names of other people mentioned in conversation
3. Don't extract names from phrases like "My name is not..." or "I don't want to give my name"
4. Look for patterns like: "I'm [Name]", "My name is [Name]", "Call me [Name]", "I go by [Name]", etc.

Respond ONLY with valid JSON in this exact format:
{{
    "name_detected": true/false,
    "name": "extracted name here or empty string",
    "confidence": "high/medium/low"
}}

Examples:
- "Hi, I'm John Smith" → {{"name_detected": true, "name": "John Smith", "confidence": "high"}}
- "My name is Sarah" → {{"name_detected": true, "name": "Sarah", "confidence": "high"}}
- "Call me Mike" → {{"name_detected": true, "name": "Mike", "confidence": "high"}}
- "John called me yesterday" → {{"name_detected": false, "name": "", "confidence": "high"}}
- "What's the weather like?" → {{"name_detected": false, "name": "", "confidence": "high"}}

Analyze the message and respond:
"""

        # Get LLM response
        response = llm.invoke(detection_prompt)
        response_text = response.content.strip()
        
        print(f"[NAME_DETECTION] LLM Response: {response_text}")
        
        # Parse JSON response
        try:
            name_info = json.loads(response_text)
            return name_info
        except json.JSONDecodeError:
            print(f"[NAME_DETECTION] Failed to parse LLM response as JSON: {response_text}")
            return {"name_detected": False, "name": "", "confidence": "low"}
            
    except Exception as e:
        print(f"[NAME_DETECTION] Error in LLM name detection: {e}")
        return {"name_detected": False, "name": "", "confidence": "low"}

def save_name_to_database(session_id, name, original_message):
    """
    Save detected name to chat_info table.
    
    Args:
        session_id (str): Session identifier
        name (str): Extracted name
        original_message (str): The original message where name was detected
    """
    try:
        # Ensure clean transaction state
        sync_connection.rollback()
        
        with sync_connection.cursor() as cur:
            # Create initial summary entry with name
            # summary_text = f"User introduced themselves as: {name}"
            
            # Store metadata about detection
            metadata = {
                "name_detected_from_message": original_message,
                "detection_method": "llm",
                "detection_timestamp": datetime.now().isoformat()
            }
            
            # Insert or update the conversation summary
            insert_query = """
            INSERT INTO chat_info (
                session_id, 
                contact_name, 
                metadata,
                created_at
            ) VALUES (%s, %s, %s, %s)
            ON CONFLICT (session_id) 
            DO UPDATE SET 
                contact_name = EXCLUDED.contact_name,
                metadata = EXCLUDED.metadata
            """
            
            cur.execute(insert_query, (
                session_id,
                name,
                json.dumps(metadata),
                datetime.now()
            ))
            
            sync_connection.commit()
            print(f"[DATABASE] Name '{name}' saved for session {session_id}")
            
    except Exception as e:
        print(f"[DATABASE] Error saving name to database: {e}")
        # Rollback on error to clean transaction state
        try:
            sync_connection.rollback()
        except:
            pass
