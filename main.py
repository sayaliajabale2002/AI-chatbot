import streamlit as st 
from langchain.chat_models import init_chat_model
from typing import TypedDict,Annotated
from dotenv import load_dotenv
from langchain.messages import AnyMessage, SystemMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

load_dotenv()
st.title("💬 LangGraph Chatbot")
llm_model = init_chat_model(model="gemini-2.5-flash",model_provider="google_genai")

class State(TypedDict):
    human_message : Annotated[list[HumanMessage],add_messages]
    ai_message: Annotated[list[AIMessage],add_messages]

def chatmodel(state: State):
    prompt = "you are an assistant who will assist user"
    resposne = llm_model.invoke([SystemMessage(content=prompt)] + state["human_message"])
    return {"ai_message" : resposne}

# @st.cache_resource
def get_agent():
    memory = MemorySaver()
    graph = StateGraph(State)
    graph.add_node("chatmodel", chatmodel)
    graph.add_edge(START, "chatmodel")
    graph.add_edge("chatmodel", END)
    return graph.compile(checkpointer= memory)

agent = get_agent()
config = {"configurable": {"thread_id": 1}}
userinput = st.text_input("enter user input...")

if st.button("send"):
    if userinput is not None:
        query = {"human_message" : [HumanMessage(content=userinput)]}
        response = agent.invoke(query,config=config)
        st.write(response["ai_message"][-1].content)


# query = {"human_message" : [HumanMessage(content="what is my name")]}
# response = agent.invoke(query,config=config)
# print(response["ai_message"][-1].content)