from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.tools import QuerySQLDatabaseTool
from langchain.chains import create_sql_query_chain
from langchain_core.output_parsers import StrOutputParser
from prompt_defination import sql_query_prompt
from llm_parser import gemma2_2b,gemma3_1b,gemma3_4b


llm=gemma3_4b

def sql_query(question):
    db_user="root"
    db_password=""
    db_host="localhost"
    db_port=3306
    db_name="universitydb"
    db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}")

    query_statement_generator=create_sql_query_chain(llm,db)
    query_executor = QuerySQLDatabaseTool(db=db)

    sql = query_statement_generator.invoke({"question":question})
    # Clean the SQL query by removing the markdown formatting
    clean_sql = sql.replace("```sql", "").replace("```", "").strip()
    result=query_executor.invoke({"query": clean_sql})
    output= sql_query_prompt | llm | StrOutputParser()

    return output.invoke({"input": question, "result": result})

