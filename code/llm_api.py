import os
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL_NAME, table_name
from system_prompt import get_system_prompt
from langchain_postgres import PostgresChatMessageHistory
from db import sync_connection
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Database setup 
def get_session_history(session_id):
    return PostgresChatMessageHistory(
        table_name,
        session_id,
        sync_connection=sync_connection
    )

def get_groq_response(input_text, session_id):
    """
    Generate a Groq LLM response using RunnableWithMessageHistory for chat memory.
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
    
    return response.content