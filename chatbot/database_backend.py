from langgraph.graph import START, END, StateGraph
from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, List
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

model = ChatGroq(model="llama-3.3-70b-versatile")

class ChatState(TypedDict):
    """
        BaseMessage: adding BaseMessage class inplace of str as messages could be of any message type - HumanMessage, AiMessage, ToolMessage, SystemMessage
        add_messages: optimized way of add operator in langgraph
    """
    messages: Annotated[List[BaseMessage], add_messages]


def chat_node(state: ChatState):
    # fetch user query from state
    messages = state['messages']

    # call the LLM model
    response = model.invoke(messages)

    # store the response 
    return {'messages': [response]}

# SQLite database connection
sqlite_conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)         # as we are working on multiple threads but by defauly sqlite checks / doesnt allow to work on multiple thread

# sqlite connection setup
checkpoint = SqliteSaver(sqlite_conn)

graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)

graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer=checkpoint)


def retrieve_all_threads():
    all_threads = set()
    for point in checkpoint.list(None):
        threads = (point.config['configurable']['thread_id'])
        all_threads.add(threads)
    return list(all_threads)