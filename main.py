from app.google_api_agents import main_agent
from swarm import Swarm
from openai import OpenAI
import streamlit as st

from dotenv import load_dotenv
import os
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# streamlit run main.py <- command to run the app

if __name__ == '__main__':
    swarm_client = Swarm(OpenAI(api_key=OPENAI_API_KEY))
    agent = main_agent

    st.title('Agente de IA - Google Calendar')

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    if prompt := st.chat_input('Coloque seu prompt aqui'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user', avatar='👷'):
            st.markdown(prompt)

        with st.chat_message('ai', avatar='🤖'):
            # print('Session state message', st.session_state.messages)
            response = swarm_client.run(
                agent=agent,
                debug=False,
                # messages=[{'role': 'user', 'content': prompt}],
                messages=st.session_state.messages,
            )
            st.markdown(response.messages[-1]['content'])
        st.session_state.messages.append(
            {'role': 'assistant', 'content': response.messages[-1]['content']})
