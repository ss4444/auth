from email.policy import default
from enum import unique
import ormar
from core.db import BaseMeta
from uuid import UUID, uuid4
from passlib.hash import bcrypt
from typing import Optional



class User(ormar.Model):
    class Meta(BaseMeta):
        pass

    id: UUID = ormar.UUID(primary_key=True, default=uuid4)
    last_name: str = ormar.String(max_length=50, nullable=True)
    name: str = ormar.String(max_length=50, nullable=True)
    username: str = ormar.String(max_length=50, unique=True)
    password: str = ormar.String(max_length=128)

    @classmethod
    async def get_user(cls, username):
        return cls.get(username=username)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password)
