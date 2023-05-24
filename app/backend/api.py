"""
This module contains the API that will be used to answer the questions.
"""


import uvicorn
from fastapi import FastAPI, HTTPException
from question_data import QuestionData
from src.model import model


app = FastAPI()


@app.get("/")
def root():
    """This is the test root of the API."""
    return {"message": "This is the root of the API."}


@app.get("/query")
async def query(question: str, model_type: str = "agent"):
    """
    This function will be used to answer the questions.

    Args:
        question (str): Question to be answered.
        model_type (str, optional): Type of model to be used. Defaults to "chain".
    """
    try:
        answer = model(question, model_type)
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
