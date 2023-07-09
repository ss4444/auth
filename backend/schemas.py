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
    patronymic: Optional[str]
    birthday: Optional[str]
    username: str
    password_hash: str


class UserAuth(BaseSchema):
    username: str
    password_hash: str


class UserGet(BaseSchema):
    id: str
    username: str
    password_hash: str


class UserEdit(BaseSchema):
    last_name: Optional[str]
    name: Optional[str]
    patronymic: Optional[str]
    birthday: Optional[str]
    username: Optional[str]
    password_hash: Optional[str]


class CheckEmail(BaseSchema):
    username: str


class CheckAnswer(BaseSchema):
    answer: bool
