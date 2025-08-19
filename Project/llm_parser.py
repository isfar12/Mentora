from langchain_ollama import ChatOllama,OllamaLLM

general_llm=OllamaLLM(model="gemma3:270m",temperature=.7)

gemma3_270m = ChatOllama(model="gemma3:270m", temperature=0.5)

gemma3_1b = ChatOllama(model="gemma3:1b", temperature=0.3)

gemma3_4b = ChatOllama(model="gemma3:4b", temperature=0.5)

gemma2_2b = ChatOllama(model="gemma2:2b", temperature=0.5)

llama_3_latest = ChatOllama(model="llama3.2:latest", temperature=0.5)