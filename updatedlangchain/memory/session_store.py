#from langchain.chains.memory import ChatMessageHistory
#from langchain.runnables.history import RunnableWithMessageHistory
# from langchain.memory.chat_message_histories import ChatMessageHistory


# store = {}

# def get_session_history(session_id: str):
#     if session_id not in store:
#         store[session_id] = ChatMessageHistory()
#     return store[session_id]


# memory/session_store.py

# Simple in-memory session store for multiple users
store = {}

def get_session_history(session_id: str):
    """
    Returns a list of messages for the given session_id.
    Each message is a dict with 'role' and 'content':
      role: 'user' or 'ai'
      content: the text
    """
    if session_id not in store:
        store[session_id] = []
    print(store)
    return store[session_id]

# In older langchain , this was the case.
#RunnableWithMessageHistory
#ChatMessageHistory
#ConversationBufferMemor