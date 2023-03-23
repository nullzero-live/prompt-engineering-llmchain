"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import os
import openai
import time

#OpenAI model deprecated from langchain
#from langchain.llms import OpenAI
#Import OpenAI Chat wrapper
from langchain.chat_models import ChatOpenAI
#Import Prompt Template
from langchain.prompts import PromptTemplate
#Import chains
from langchain.chains import LLMChain
#Import Sequential Chains
from langchain.chains import SimpleSequentialChain



def load_chain(api_key):
    os.environ["OPENAI_API_KEY"] = api_key
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.1)
    #user_in = input("Please describe your Python project in one to two sentences:  ")

    first_prompt = PromptTemplate(
        input_variables=["user_in"],
        template= "Write the outline of the coding steps to develop the program {user_in} in five steps. Use Python3 and Be concise. \n\n"
    )
    #First chain
    chain = LLMChain(llm=llm, prompt=first_prompt)

    second_prompt = PromptTemplate(
        input_variables=["program"],
        template= '''Write the python3 code for each step of the {program} described. Use python3 style. Be concise in the code and opinionated about framework choice.'''
    )

    chain_two = LLMChain(llm=llm, prompt=second_prompt)

    overall_chain = SimpleSequentialChain(chains=[chain, chain_two], verbose=True)


    return overall_chain




# From here down is all the StreamLit UI.
st.set_page_config(page_title="Python Project Generator", page_icon=":robot:")
st.header("Python Snippet Generator")

st.write("Enter your OpenAI API key below (not stored between sessions):")
openai_api_key = st.text_input("openai_api_key")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    user_input = st.text_input("Please describe your desired python project in 1-2 sentences. The output will be five steps including code.", key="input")
    return user_input


user_input = get_text()


if user_input:
    chain = load_chain(openai_api_key)
    
    with st.spinner('Wait for it...'):
        output = chain.run(input=user_input)
        time.sleep(5)
    st.success('Done!')
    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")