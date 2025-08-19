from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaEmbeddings

ollama_embeddings = OllamaEmbeddings(model="mxbai-embed-large:latest")

huggingface_embeddings = HuggingFaceEmbeddings(model_name="intfloat/e5-base-v2")


if(__name__ == "__main__"):
    
    print("Initializing Embedding models...")