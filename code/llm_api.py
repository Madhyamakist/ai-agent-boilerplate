import os
from langchain_groq import ChatGroq
from config import GROQ_API_KEY, GROQ_MODEL_NAME
from system_prompt import get_system_prompt
from langchain.schema import HumanMessage, AIMessage
from chat_history import memory


def get_groq_response(input):
    """
    Generate a Groq LLM response with single shared memory for all users (no session).
    """

    # Start the message list with system prompt
    messages = [("system", get_system_prompt())]

    # Add entire chat history (all users share same one)
    chat_history = memory.chat_memory.messages
    for message in chat_history:
        if isinstance(message, HumanMessage):
            messages.append(("human", message.content))
        elif isinstance(message, AIMessage):
            messages.append(("assistant", message.content))
    # Add current user input
    messages.append(("human", input))  

    # Call the LLM with all context
    llm = ChatGroq(groq_api_key=GROQ_API_KEY, model=GROQ_MODEL_NAME)
    response = llm.invoke(messages)
    # Save the current exchange to memory
    memory.chat_memory.add_user_message(input)
    memory.chat_memory.add_ai_message(response.content)

    return response.content