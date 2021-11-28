from fastapi import APIRouter, Depends, HTTPException
from modules import auth
from modules.classes import TaskList, User, UserToken
from modules.database import add_user, list_task, user_exists, user_hash

router = APIRouter()

@router.post("/add", response_model=UserToken, tags=["users"])
async def add_user_(user: User):
    identifier = auth.generate_uuid(user.email)
    if not user_exists(identifier):
        add_user(identifier, auth.generate_hash(user.password))
        return UserToken(uuid=identifier, jwt=auth.generate_jwt(identifier))
    raise HTTPException(status_code=403)

@router.post("/auth", response_model=UserToken, tags=["users"])
async def authenticate_user_(user: User):
    identifier = auth.generate_uuid(user.email)
    if user_exists(identifier):
        if auth.check_password(user.password, user_hash(identifier)):
            return UserToken(uuid=identifier, jwt=auth.generate_jwt(identifier))
    raise HTTPException(status_code=401)

@router.get("/tasks", response_model=TaskList, tags=["users"])
async def view_user_tasks_(identifier: str = Depends(auth.header_to_identifier)):
    if identifier:
        return list_task(identifier)
    raise HTTPException(status_code=401)
