import uuid
from database_connection import create_application_logs, insert_application_logs
from prompt_defination import context_aware_assistant
from llm_parser import gemma3_4b
from sql_agent import sql_query
from rag_loaders import file_to_vector_store,folder_creation

llm=gemma3_4b

create_application_logs()

# Example usage for a new user
# session_id = str(uuid.uuid4())
session_id = "57ea1328-6f1a-45cc-bd00-8c343849cc5b"  # Replace with actual session ID or generate a new one

folder_creation(session_id)

# This is a question about the company that i have stored in the context_creation.py 
question = "What is GreenGrow Innovations?"
answer = context_aware_assistant(question, session_id)
insert_application_logs(session_id, question, answer, "llama3.2:latest")
print(f"Human: {question}")
print(f"AI: {answer}\n")

# Example of a follow-up question
question2 = "Who is the founder of it?"
answer2 = context_aware_assistant(question2, session_id)
insert_application_logs(session_id, question2, answer2, "llama3.2:latest")
print(f"Human: {question2}")
print(f"AI: {answer2}")

question3 = "How much fund they raised this year?"
answer3 = context_aware_assistant(question3, session_id)
print(f"Human: {question3}")
print(f"AI: {answer3}")


# This part is about database query by llm
question4="List all the students of session 2021 who has more or equal cgpa than 3.6?"
answer4=sql_query(question4)
insert_application_logs(session_id, question4, answer4, "llama3.2:latest")
print(f"Human: {question4}")
print(f"AI: {answer4}")

# imaginary file upload and rag question answering demo
import shutil
#in streamlit we will save the file with session_id named folder and directly feed to vector store using file_to_Vector_Store
source = r"Files\LangChain_Overview.pdf"
destination = f"Files\{session_id}\LangChain_Overview.pdf"
shutil.move(source, destination)

file_to_vector_store("LangChain_Overview.pdf", session_id)
question5 = "What is LangChain?"
answer5 = context_aware_assistant(question5, session_id)
insert_application_logs(session_id, question5, answer5, "llama3.2:latest")
print(f"Human: {question5}")
print(f"AI: {answer5}")
