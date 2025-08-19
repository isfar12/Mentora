from langchain_chroma import Chroma
from embedding_parser import huggingface_embeddings


def load_vector_store(session_id):
    vector_store = Chroma(
    embedding_function=huggingface_embeddings,
    persist_directory="vector_store",
    collection_name=f"{session_id}"
    )
    return vector_store

def load_retriever(session_id="default_session"):
    vector_store = load_vector_store(session_id)
    retriever = vector_store.as_retriever(search_kwargs={"k":4},search_type="similarity")
    return retriever
