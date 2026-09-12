from typing import Annotated

from fastapi import APIRouter, Depends, Body
from app.dependecy import get_user_service
from app.users.user_profile.schema import  UserCreateSchema
from app.users.auth.schema import UserLoginSchema
from app.users.user_profile.service import UserService

router = APIRouter(prefix='/user', tags=["user"])


@router.post("/register", response_model=UserLoginSchema)
async def create_user(
    user_service: Annotated[UserService, Depends(get_user_service)],  
    body: UserCreateSchema = Body(...)  
):
    return await user_service.create_user(body.username, body.password)