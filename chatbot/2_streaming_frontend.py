"""
    Streamlit Notes:
    Streamlit has a nature which executes the complete script from start to end after every input message
    st.session_state -> dict -> which does not resets after every input means does not execute the complete code 
    st.write_stream() -> for generating streaming response
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

    with st.chat_message('ai'):
        ai_response = st.write_stream(
            response_chunk.content for response_chunk, metadata in chatbot.stream(
                {'messages': [HumanMessage(content=user_input)]},
                config={'configurable': {'thread_id': CONFIG}},
                stream_mode='messages'
            )
        )
    st.session_state['message_history'].append({'role': 'ai', 'content': ai_response})

