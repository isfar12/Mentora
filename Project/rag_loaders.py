import os
from langchain_community.document_loaders import PyPDFLoader,Docx2txtLoader,TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from vector_store import load_vector_store

def document_loader(file_path):
    '''
    This function is responsible for loading a document from a file path.
    '''
    if file_path.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path.endswith(".txt"):
        loader = TextLoader(file_path)
    else:
        raise ValueError("Unsupported file format")
    
    documents=loader.load()
    for doc in documents:
        doc.page_content = " ".join(doc.page_content.split())
    return documents

def text_splitter(text:str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=200
    )
    splitted_docs = text_splitter.split_text(text)
    return splitted_docs

def folder_creation(session_id:str):
    '''
    This function is responsible for creating a folder for the user in the Files directory.
    '''
    directory=os.getcwd()
    directory=os.path.join(directory,"Files",session_id)
    
    if not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)
    
    return directory


def file_to_vector_store(file_name:str,session_id:str):
    '''
    This function is responsible for loading a file from the user directory and converting it to a vector store.
    '''
    directory=os.getcwd()
    directory=os.path.join(directory,"Files",session_id)
    file_path=os.path.join(directory,file_name)

    documents=document_loader(file_path)
    # Extract text from documents and combine
    full_text = " ".join([doc.page_content for doc in documents])
    splitted_docs=text_splitter(full_text)
    vector_store=load_vector_store(session_id)
    vector_store.add_texts(splitted_docs)
    return f"Document added to vector store: {file_name}"




