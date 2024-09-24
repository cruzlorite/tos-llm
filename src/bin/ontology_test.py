import getpass
import os

os.environ["OPENAI_API_KEY"] = "sk-Vn416fJ5l5gRRNoQnaIIMEbepS7T_EyaxWv8d3eTqIT3BlbkFJfReJ5s0y1hv82SWyit1aaKwM_PkX_Fx6c4GZjvsqoA"

from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini")

from tos.ontology.utdo import *

structured_llm = llm.with_structured_output(Permission)

output = structured_llm.invoke("""
You are an expert Knowledge Engineer and you are working on a project to build a knowledge graph.
You are required to generate a Policy object that represents the input term.

Stick to the specified format and ouput valid JSON.

Format

Term: '''
GitHub has the right to suspend or terminate your access to all or any part of the Website at any time, with or without cause, with or without notice, effective immediately. GitHub reserves the right to refuse service to anyone for any reason at any time.
'''
""")
