from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File
import jwt
from managers.users import authenticate_user, get_user_current
from models import User
import asyncpg
from schemas import UserAllInfo, UserGet, UserAuth, UserEdit, CheckEmail, CheckAnswer
from passlib.hash import bcrypt
import ormar

JWT_SECRET = 'myjwtsecret'

router = APIRouter(
    prefix=""
)


@router.post('/')
async def auth(data: UserAuth):
    user = await authenticate_user(data.username, data.password)
    if not user:
        return {'error' : 'invaid credentials'}
    user = UserGet(
        id=str(user.id),
        username=user.username,
        password=user.password
    )
    token = jwt.encode(user.dict(), JWT_SECRET)
    return {'access_token' : token, 'token_type' : 'bearer'}


@router.post('/reg')
async def register(user: UserAllInfo):
    try:
        user.password = bcrypt.hash(user.password)
        user_dict = user.dict()
        await User.objects.create(**user_dict)
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=400, detail="User already exists")
    return Response(status_code=200, content="User created")


@router.post('/check_username')
async def check_username(username: CheckEmail):
    try:
        await User.objects.get(username=username.username)
        return CheckAnswer(answer=False)
    except ormar.exceptions.NoMatch:
        return CheckAnswer(answer=True)


@router.patch('/me')
async def user_edit(new_user: UserEdit, user=Depends(get_user_current)):
    if new_user.password:
        new_user.password = bcrypt.hash(new_user.password)
    user = await User.objects.get(id=user.id)
    try:
        await user.update(**{k: v for k, v in new_user.dict().items() if v})
    except asyncpg.exceptions.UniqueViolationError:
        raise HTTPException(status_code=409, detail="Nickname is already in use")
    return user


@router.get('/me')
async def get_me(user=Depends(get_user_current)):
    user_get = await User.objects.get(id=user.id)
    return user_get
