import uuid
import datetime
import typing as t

from pydantic import BaseModel, BeforeValidator, Field


def validate_date(date_str: str) -> datetime.date:
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return date


class RequestInput(BaseModel):
    input: str = Field(example="John")
    top_k: int = Field(example=5)
    version: t.Annotated[datetime.date, BeforeValidator(validate_date)]

    # May be decorator to add _uuid field
    # _uuid = Field(default_factory=uuid.uuid4, alias="uuid")


class QuestionAnswer(BaseModel):
    question: str
    answer: str


class ResponseOutput(BaseModel):
    output: list[QuestionAnswer]
