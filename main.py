import streamlit as st 
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from typing import TypedDict,Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage,AnyMessage
from langgraph.graph.message import add_messages
from langgraph.graph import START, END, StateGraph
from langgraph.prebuilt import ToolNode,tools_condition
from langgraph.checkpoint.memory import MemorySaver

from tavily import TavilyClient
import os 
api_key = os.getenv('TAVILY_API_KEY')

load_dotenv()
st.title("💬 Chatbot")
llm_model = init_chat_model(model="gemini-2.5-flash",model_provider="google_genai",temperature=0.1)

class State(TypedDict):
    messages: Annotated[list[AnyMessage],add_messages]

def sum(a:int,b:int)->int:
    '''addition of a and b'''
    res = a+b
    return f'{a} + {b} = {res}'

def search_tool(state:State):
    '''answer user query on real time web search data'''
    client = TavilyClient(api_key)
    response = client.search(
        query=state['messages'][-1].content,
        # search_depth="advanced",
        max_results=2
    )
    search_result_text = str(response) 
    return {'messages': [AIMessage(content=search_result_text)]}

tools = [sum, search_tool]
llm_with_tool = llm_model.bind_tools(tools)

def chatbot(state:State):
    '''You are a chatbot who will answer user query'''
    res = llm_with_tool.invoke(state['messages'])
    return {'messages':[res]}

def get_agent():
    memory = MemorySaver()
    graph = StateGraph(State)
    graph.add_node('chatbot',chatbot)
    graph.add_node('tools',ToolNode(tools))
    graph.add_edge(START,'chatbot')
    graph.add_conditional_edges('chatbot',tools_condition)
    graph.add_edge('tools',END)
    return graph.compile(checkpointer=memory)

agent = get_agent()
config = {"configurable": {"thread_id": 1}}

query = st.text_input("Enter your Query...")
if st.button("send"):
    if query is not None:
        query = {'messages':[HumanMessage(content=query)]}
        res = agent.invoke(query,config=config)
        st.write(res['messages'][-1].content)
