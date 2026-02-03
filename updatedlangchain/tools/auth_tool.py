from langchain.tools import tool
import uuid

@tool
def authenticate_user(username:str)->str:
    """
    Dummy authentication tool.
    Accepts any user and returns a session_id.
    """
    session_id=str(uuid.uuid4())
    return session_id
    
