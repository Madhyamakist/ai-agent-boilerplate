import os
from langchain_groq import ChatGroq
from config import GROQ_API_KEY
from config import GROQ_MODEL_NAME
from system_prompt import get_system_prompt

def get_groq_response(input):
    # Initialize LangChain's ChatGroq with selected Groq model 

    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=GROQ_MODEL_NAME)

    # Build message sequence
    messages = [("system", get_system_prompt())]

    # Add actual user input
    messages.append(("human", input))

    # Invoke LLM
    response = llm.invoke(messages)
    return response.content