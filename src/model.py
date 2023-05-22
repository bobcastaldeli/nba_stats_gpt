"""
This module contains the model that will be used to answer the questions.
"""


import yaml
from langchain.sql_database import SQLDatabase
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.chat_models import ChatOpenAI


with open("conf/secrets.yaml", "r", encoding="utf-8") as f:
    config = yaml.safe_load(f)

USER = config["databse"]["user"]
PWD = config["databse"]["password"]
HOST = config["databse"]["host"]
PORT = config["databse"]["port"]
DB = config["databse"]["name"]


def model(question: str):
    """
    Função que cria o modelo de consulta da base de dados.
    """
    llm = ChatOpenAI(
        model_name=config["openai"]["modelname"],
        temperature=config["openai"]["temperature"],
        openai_api_key=config["openai"]["openaikey"],
    )
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{USER}:{PWD}@{HOST}:{PORT}/{DB}"
    )
    toolkit = SQLDatabaseToolkit(db, llm)
    agent_executor = create_sql_agent(llm=llm, toolkit=toolkit, verbose=True)
    answer = agent_executor.run(question)
    return answer
