from pydantic import BaseModel
import orjson
from typing import Optional


class BaseSchema(BaseModel):
    class Config:
        anystr_strip_whitespace = True
        min_anystr_length = 1
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class UserAllInfo(BaseSchema):
    last_name: str
    name: str
    username: str
    password: str


class UserAuth(BaseSchema):
    username: str
    password: str


class UserGet(BaseSchema):
    id: str
    username: str
    password: str


class UserEdit(BaseSchema):
    last_name: Optional[str]
    name: Optional[str]
    username: Optional[str]
    password: Optional[str]


class CheckEmail(BaseSchema):
    username: str


class CheckAnswer(BaseSchema):
    answer: bool
