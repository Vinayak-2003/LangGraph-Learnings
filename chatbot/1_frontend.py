"""
    Streamlit Notes:
    Streamlit has a nature which executes the complete script from start to end after every input message
    st.session_state -> dict -> which does not resets after every input means does not execute the complete code 
"""

import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

CONFIG = {'configurable': {'thread_id': 'thread-1'}}

user_input = st.chat_input("Type here: ")

if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

if user_input:
    st.session_state['message_history'].append({'role': 'user', 'content': user_input})
    with st.chat_message('user'):
        st.text(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(user_input)]}, config=CONFIG)
    ai_message = response['messages'][-1].content
    st.session_state['message_history'].append({'role': 'ai', 'content': ai_message})
    with st.chat_message('ai'):
        st.text(user_input)

