from langchain_core.prompts import PromptTemplate,ChatPromptTemplate,MessagesPlaceholder
from langchain_core.messages import HumanMessage,SystemMessage
from llm_parser import gemma3_270m,llama_3_latest,general_llm
from langchain_core.output_parsers import StrOutputParser
from database_connection import get_chat_history
from langchain.chains import create_history_aware_retriever
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from vector_store import load_retriever


'''----------------------------PROMPTS-----------------------------'''
#use in regular prompt question
general_prompt=PromptTemplate(
    template='''You are a helpful assistant. Answer the question: {question} in brief. If you do not have answer, say I don't know.
                Here is an example:
               ''',
    input_variables=["question"]
)

# use to contextualize the rag prompt
contextualize_system_prompt = (
    '''You must rewrite the user question to be standalone using chat history context. Return ONLY the rewritten question - nothing 
    else. No explanations, no answers. 
    
    Example: If user asks 'Was he the first president?' and chat history mentions George Washington,
    Return : 'Was George Washington the first president?'

    Example: If user asks 'What is the capital of Spain?' and No chat history mentioned,
    Return : 'What is the capital of Spain?'
    '''
)
#use when user wants to know database information
sql_query_prompt= PromptTemplate(
        template='''
            "You are a helpful assistant. You have two information. 
            User Query: {input} and 
            Returned Response: {result}
            
            The response contains user's answer to query. You task is to summarize the result to the user. Make a summary of the response"
        ''',
        input_variables=["input", "result"]
)
# RAG QA prompt for LLM 
rag_prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are a helpful assistant. Use the following context to answer the user's question."),
        ("system","{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("user","{input}")
    ]
)
# This portion is initialized when RAG mode is enabled
'''*********************** Functions ***********************'''
llm=gemma3_270m
general_llm=general_llm
chat=llama_3_latest
# when rag mode is enabled, these prompts will be used to contextualize the user question

def regular_assistant(question):
    '''
    This function is responsible for answering the question using the general prompt.
    '''
    full_prompt=general_prompt | general_llm | StrOutputParser()
    answer=full_prompt.invoke({"question": question})
    
    return answer


def context_aware_assistant(question,session_id):
    chat_history=get_chat_history(session_id)
    retriever=load_retriever(session_id)

    contextualize_full_prompt=ChatPromptTemplate.from_messages(
        [
            ("system",contextualize_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("user","{input}")
        ]   
    )
    #contextualized_question=contextualize_full_prompt | llm | StrOutputParser()

    #langchain's built-in function to create the chain automatically

    #use contextualize prompt for better question chain
    context_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_full_prompt)
    #use the rag prompt and llm to create the answering chain
    question_answer_chain = create_stuff_documents_chain(chat, rag_prompt)


    #combine both chains and make full rag_chain
    rag_chain = create_retrieval_chain(context_aware_retriever, question_answer_chain)

    answer = rag_chain.invoke({"input": question, "chat_history": chat_history})['answer']

    return answer


