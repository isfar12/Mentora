from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_ollama import ChatOllama


chat=ChatOllama(
    model="gemma2:2b",
    temperature=.5
)

parser=StrOutputParser()

prompt=PromptTemplate(
    template='''
    Explain the {task} in detail, including the steps involved and any relevant considerations. Provide a comprehensive overview that would help someone unfamiliar with the task understand how to approach it effectively.
''',
    input_variables=["task"]
)

chain = prompt | chat | parser

print(chain.invoke({"task": "How to cook a perfect steak?"}))
