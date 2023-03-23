''' Experimentation with chaining LLM's together to complete complicated tasks'''
import os
import openai
import time
os.environ["OPENAI_API_KEY"] = "YOUR OPEN AI KEY"

#Import LLM wrapper
from langchain.llms import OpenAI
#Import Prompt Template
from langchain.prompts import PromptTemplate
#Import chains
from langchain.chains import LLMChain
#Import Sequential Chains
from langchain.chains import SimpleSequentialChain


llm = OpenAI(temperature=0.3)
user_in = input("Please describe your Python project in one to two sentences:  ")

first_prompt = PromptTemplate(
    input_variables=["user_in"],
    template= "You are a senior Python Engineer. List five steps required to develop the python3 project {user_in}\n\nimport" 
    )
#First chain
chain = LLMChain(llm=llm, prompt=first_prompt)

second_prompt = PromptTemplate(
    input_variables=["project"],
    template= "Produce the python3 code for each step of the software {project} described. Use appropriate style, classes and variables. Be verbose in the code."
)

chain_two = LLMChain(llm=llm, prompt=second_prompt)

overall_chain = SimpleSequentialChain(chains=[chain, chain_two], verbose=True)

code_output = overall_chain.run(user_in)

print(code_output[-1])

#print(chain.run(user_in))
