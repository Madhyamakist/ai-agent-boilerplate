import os
import asyncio
from concurrent.futures import ThreadPoolExecutor
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL_NAME, table_name, agent_type
from system_prompt import get_sales_prompt, get_generic_prompt
from langchain_postgres import PostgresChatMessageHistory
from db import sync_connection
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from conversation_processor.conversation_processor import process_conversation



# Database setup 
def get_session_history(session_id):
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=sync_connection
    )


def get_groq_response(input_text, session_id, request_type):
    
    # Choose prompt based on request type
    if request_type == agent_type.SALES:
        system_prompt = get_sales_prompt()
    else:
        system_prompt = get_generic_prompt()
    
    # Rest of your existing code...
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}")
    ])


    """
    Generate a Groq LLM response using RunnableWithMessageHistory for chat memory.
    
    Args:
        input_text: User input text
        session_id: Session identifier
        process_async: Whether to process conversation asynchronously (default: True)
    """


    # Create the LLM
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=GROQ_MODEL_NAME)
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
    # Process conversation asynchronously to avoid blocking the response
    _process_conversation_async(input_text, session_id, request_type)



    return bot_response



def _process_conversation_async(input_text, session_id, request_type):
    """Process conversation asynchronously using ThreadPoolExecutor."""
    def process_in_background():
        try:
            process_conversation(input_text, session_id, request_type)
            print("[LLM_API] Async conversation processing completed")
        except Exception as processing_error:
            print(f"[LLM_API] Warning: Async conversation processing failed: {processing_error}")
    
    # Submit to thread pool for background processing
    with ThreadPoolExecutor(max_workers=1) as executor:
        executor.submit(process_in_background)
