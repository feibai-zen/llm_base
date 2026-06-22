import os
from http.client import responses

from langchain_openai import ChatOpenAI
from langchain_classic.chains import create_sql_query_chain
from langchain_community.utilities import SQLDatabase
import pymysql

db_user = os.getenv("DB_USER", "root")
db_host = os.getenv("DB_HOST", "127.0.0.1")
db_pass = os.getenv("DB_PASS", "123456")
db_name = os.getenv("DB_NAME", "llm_base")

db = SQLDatabase.from_uri(f"mysql://{db_user}:{db_pass}@{db_host}/{db_name}")

llm = ChatOpenAI()
chain = create_sql_query_chain(llm=llm, db=db)
response = chain.invoke({
    "question": "查询一个班级有多少学生？",
    "table_names_to_use": ["students"]
})

print(response)