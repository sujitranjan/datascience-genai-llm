#from langchain_google_genai import ChatGoogleGenerativeAI
#from langchain.agents import create_react_agent, AgentExecutor
# You’re using LangChain 1.2.3, which is very new, and that’s why:

#AgentExecutor is no longer in langchain.agents

#create_react_agent is moved to langchain.agents.react.agent

#langchain.agents.agent doesn’t exist anymore

# from langchain.agents.agent import AgentExecutor
# from langchain.agents.react.agent import create_react_agent
# from tools.retriever import rag_tool
# from tools.web_search import web_search
# from prompts.agent_prompt import AGENT_PROMPT

# def build_agent():
#     llm = ChatGoogleGenerativeAI(
#         model="gemini-1.5-flash",
#         temperature=0.2
#     )

#     tools = [rag_tool, web_search]

#     agent = create_react_agent(
#         llm=llm,
#         tools=tools,
#         prompt=AGENT_PROMPT
#     )

#     return AgentExecutor(
#         agent=agent,
#         tools=tools,
#         verbose=True)## packaging evrything in agent executor, its just writing evrything together
################################
# from langchain.agents.react import ReActAgent
# from langchain.agents import Tool
# from langchain_google_genai import ChatGoogleGenerativeAI
# from prompts.agent_prompt import AGENT_PROMPT
# from tools.retriever import rag_tool
# from tools.web_search import web_search

# def build_agent():
#     llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.2)

#     tools = [
#         Tool(name="RAG Tool", func=rag_tool, description="Search internal docs"),
#         Tool(name="Web Search", func=web_search, description="Search recent info")
#     ]

#     agent = ReActAgent.from_llm_and_tools(
#         llm=llm,
#         tools=tools,
#         prompt=AGENT_PROMPT
#     )

#     return agent

# agents/main_agent.py
#from langchain.chat_models import ChatGoogleGenerativeAI




# from langchain.agents import create_agent
# from langchain_google_genai import ChatGoogleGenerativeAI
# from prompts.agent_prompt import AGENT_PROMPT
# from tools.retriever import rag_tool
# from tools.web_search import web_search

# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain.agents.react.agent import create_react_agent
# from langchain.agents import AgentExecutor
# from tools.retriever import rag_tool
# from tools.web_search import web_search
# from prompts.agent_prompt import AGENT_PROMPT

# def build_agent():
#     # 1) LLM Instance
#     llm = ChatGoogleGenerativeAI(
#         ##model="gemini-1.5-flash",
#         #model="gemini-2.5-flash",
#         model="gemini-2.5-flash-lite",
#         temperature=0.2,
#         api_key=""
#     )

#     # 2) Use tool functions directly (no Tool class)
#     tools = [rag_tool, web_search]

#     # 3) Create agent with system prompt
#     agent = create_agent(
#         model=llm,
#         tools=tools,
#         system_prompt=AGENT_PROMPT
#     )

#     return agent

#from langchain.agents.react.agent import create_react_agent
from langchain.agents import create_agent
#from langchain.agents import AgentExecutor
from langchain_google_genai import ChatGoogleGenerativeAI
from tools.retriever import rag_tool
from tools.web_search import web_search
from prompts.agent_prompt import AGENT_PROMPT

def build_agent():
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        temperature=0.2,
        api_key=""
    )

    tools = [rag_tool, web_search]

    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt=AGENT_PROMPT
    )

    return agent

