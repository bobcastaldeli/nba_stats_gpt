"""
This module contains the model that will be used to answer the questions.
"""


import yaml
from langchain.sql_database import SQLDatabase
from langchain.chains import SQLDatabaseChain
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


def model(question: str, type: list = ["chain", "agent"]):
    """
    This function will be used to answer the questions.

    Args:
        question (str): Question to be answered.
        type (list, optional): Type of model to be used. Defaults to ["chain", "agent"].
    """
    llm = ChatOpenAI(
        model_name=config["openai"]["modelname"],
        temperature=config["openai"]["temperature"],
        openai_api_key=config["openai"]["openaikey"],
    )
    db = SQLDatabase.from_uri(
        f"postgresql+psycopg2://{USER}:{PWD}@{HOST}:{PORT}/{DB}"
    )
    if type == "chain":
        chain = SQLDatabaseChain(llm=llm, db=db, verbose=True)
        answer = chain.run(question)
        return answer
    else:
        toolkit = SQLDatabaseToolkit(db, llm)
        agent_executor = create_sql_agent(
            llm=llm, toolkit=toolkit, verbose=True
        )
        answer = agent_executor.run(question)
        return answer
