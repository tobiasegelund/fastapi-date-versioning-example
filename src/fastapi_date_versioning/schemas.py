import datetime
import typing as t

from pydantic import BaseModel, BeforeValidator, Field


def validate_date(date_str: str) -> datetime.date:
    date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
    return date


class RequestInput(BaseModel):
    input: str = Field(example="John")
    version: t.Annotated[datetime.date, BeforeValidator(validate_date)]


class ResponseOutput(BaseModel):
    message: str
