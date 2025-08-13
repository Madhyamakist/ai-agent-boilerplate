import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL_NAME, table_name
from system_prompt import get_system_prompt
from langchain_postgres import PostgresChatMessageHistory
from db import sync_connection
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from conversation_processor import process_conversation


# Database setup 
def get_session_history(session_id):
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=sync_connection
    )

def get_groq_response(input_text, session_id,process_async=True):
    """
    Generate a Groq LLM response using RunnableWithMessageHistory for chat memory.
    
    Args:
        input_text: User input text
        session_id: Session identifier
        process_async: Whether to process conversation asynchronously (default: True)
    """
    # Create the LLM
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=GROQ_MODEL_NAME)
    
    # Create a prompt template that includes system message and chat history
    prompt = ChatPromptTemplate.from_messages([
        ("system", get_system_prompt()),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])
    
    # Create the chain
    chain = prompt | llm
    
    # Wrap the chain with message history
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )
    
    # Configure the session
    config = {"configurable": {"session_id": session_id}}
    
    # Get response with history
    response = chain_with_history.invoke(
        {"input": input_text},
        config=config
    )

    bot_response = response.content

    # Handle conversation processing
    if process_async:
        # Process conversation asynchronously to avoid blocking the response
        _process_conversation_async(input_text, session_id)
    else:
        # Process conversation synchronously
        _process_conversation_sync(input_text, session_id)

    return bot_response

def _process_conversation_sync(input_text, session_id):
    """Process conversation synchronously."""
    try:
        process_conversation(input_text, session_id)
        print("[LLM_API] Conversation processing completed")
    except Exception as processing_error:
        print(f"[LLM_API] Warning: Conversation processing failed: {processing_error}")

def _process_conversation_async(input_text, session_id):
    """Process conversation asynchronously using ThreadPoolExecutor."""
    def process_in_background():
        try:
            process_conversation(input_text, session_id)
            print("[LLM_API] Async conversation processing completed")
        except Exception as processing_error:
            print(f"[LLM_API] Warning: Async conversation processing failed: {processing_error}")
    
    # Submit to thread pool for background processing
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(process_in_background)