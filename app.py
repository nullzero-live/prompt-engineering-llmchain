"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
import os
import openai


#Import LLM wrapper
from langchain.llms import OpenAI
#Import Prompt Template
from langchain.prompts import PromptTemplate
#Import chains
from langchain.chains import LLMChain
#Import Sequential Chains
from langchain.chains import SimpleSequentialChain



def load_chain():
    os.environ["OPENAI_API_KEY"] = api_key
    llm = OpenAI(temperature=0.3)
    #user_in = input("Please describe your Python project in one to two sentences:  ")

    first_prompt = PromptTemplate(
        input_variables=["user_in"],
        template= "You are a senior Python Engineer. List five steps required to develop the software project specified. Use the common libraries available in Python3. Be verbose in the code and opinionated about framework choice.:\n\n {user_in}"
    )
    #First chain
    chain = LLMChain(llm=llm, prompt=first_prompt)

    second_prompt = PromptTemplate(
        input_variables=["project"],
        template= "Produce the python3 code for each step of the software {project} described. Use appropriate style, classes and variables. Be verbose."
    )

    chain_two = LLMChain(llm=llm, prompt=second_prompt)

    overall_chain = SimpleSequentialChain(chains=[chain, chain_two], verbose=True)

    code_output = overall_chain.run(user_in)

    return chain

chain = load_chain()

# From here down is all the StreamLit UI.
st.set_page_config(page_title="Python Project Generator", page_icon=":robot:")
st.header("Python Project Generator")

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []


def get_text():
    user_input = st.text_input("Please describe your python project in 1-2 sentences", key="input")
    return user_input, get_key

def get_key():
    get_key = st.text_input("Please enter your OpenAPI API Key", key="input")
    return get_key


api_key = get_key()
user_input = get_text()


if user_input:
    output = chain.run(input=user_input)

    st.session_state.past.append(user_input)
    st.session_state.generated.append(output)

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")