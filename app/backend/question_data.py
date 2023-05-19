"""
This is the data model for the request body when calling the endpoint.
"""


from pydantic import BaseModel


class QuestionData(BaseModel):
    """
    This class defines the data that is expected in the request body when
    calling the endpoint.
    """

    question_input: str
