from fastapi import FastAPI
from agents.main_agent import build_agent
from memory.session_store import get_session_history
#from langchain.runnables.history import RunnableWithMessageHistory
from tools.auth_tool import authenticate_user

app = FastAPI()

agent_executor = build_agent()


from langchain_core.messages import HumanMessage, AIMessage


def extract_ai_text(ai_message):
    content = ai_message.content

    # Case 1: plain string
    if isinstance(content, str):
        return content

    # Case 2: list of content blocks (Gemini / multimodal)
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict) and "text" in block:
                texts.append(block["text"])
            elif isinstance(block, str):
                texts.append(block)
        return "\n".join(texts)

    # Fallback
    return str(content)


def build_messages(history):
    messages = []
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    print("==================")
    print(messages)
    return messages

# def build_messages(history, new_message):
#     """
#     Convert stored session history into LangChain message format
#     """
#     messages = []

#     for h in history:
#         role = "user" if h["role"] == "user" else "assistant"
#         messages.append((role, h["content"]))

#     # add current user message
#     messages.append(("user", new_message))
#     print("=======================")
#     print(messages)

#     return messages

# agent_with_memory = RunnableWithMessageHistory(
#     agent_executor,
#     get_session_history,
#     input_messages_key="input",
#     history_messages_key="chat_history"
# )

# ---- LOGIN ----
@app.post("/login")
def login(username: str):
    session_id = authenticate_user.run(username)
    return {"session_id": session_id}




@app.post("/chat")
def chat(session_id: str, message: str):
    history = get_session_history(session_id)

    # add user message
    history.append({"role": "user", "content": message})
    print("STORE CONTENT:", history)

    # 🔑 send FULL history to agent
    messages = build_messages(history)

    result = agent_executor.invoke({"messages": messages})

    # extract AI text safely
    ai_message = result["messages"][-1]
    ai_text = extract_ai_text(ai_message)

    # store AI reply
    history.append({"role": "assistant", "content": ai_text})

    return {"response": ai_text}


# @app.post("/chat")
# def chat(session_id: str, message: str):
#     # 1) Get conversation history for this session
#     history = get_session_history(session_id)

#     messages = build_messages(history, message)
    
#     result = agent_executor.invoke({"messages": [("user", message)]})
#     #print("AGENT RESULT:", result, type(result))
#     ai_text = result["messages"][-1].content[0]["text"]

#     history.append({"role": "user", "content": message})
#     history.append({"role": "ai", "content": ai_text})

#     return {"response": ai_text}

# # ---- CHAT ----
# @app.post("/chat")
# def chat(session_id: str, message: str):
#     result = agent_with_memory.run(
#         message,
#         config={"configurable": {"session_id": session_id}}
#     )
#     return {"response": result}
#fastapi
#uvicorn app:app --reload  ## how to run 
#pip install fastapi uvicorn

##SLIDING WINDOW OF MESSAGE STORE
# def build_messages(history, max_messages=12):
#     system = [("system", AGENT_PROMPT)]
#     recent = history[-max_messages:]
#     return system + [(m["role"], m["content"]) for m in recent]


##can do summarization of chats,


# If you want next:

# 🔹 auto memory summarization

# 🔹 Redis / DB memory

# 🔹 per-user profile memory (name, city, hobby)

# 🔹 token-based trimming instead of count
#[HumanMessage(content='my name sujit ', additional_kwargs={}, response_metadata={}), 
# AIMessage(content='Hi Sujit, it is nice to meet you. How can I help you today?', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]),
#  HumanMessage(content='what is leave policy in my company', additional_kwargs={}, response_metadata={})]

#[HumanMessage(content='my name sujit ', additional_kwargs={}, response_metadata={}),
#  AIMessage(content='Hi Sujit, it is nice to meet you. How can I help you today?', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]), 
# HumanMessage(content='what is leave policy in my company', additional_kwargs={}, response_metadata={}), 
# AIMessage(content='I am sorry, I could not retrieve the leave policy from the internal documents. 
# Is there anything else I can help you with?', additional_kwargs={}, response_metadata={}, tool_calls=[], invalid_tool_calls=[]),
#  HumanMessage(content='what is my name then', additional_kwargs={}, response_metadata={})]