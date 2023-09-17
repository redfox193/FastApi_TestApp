from typing import Annotated
from fastapi import APIRouter, Depends, Security
from .login import get_current_user
from ..database import schemas


router = APIRouter(prefix="/users", 
                   tags=["users"])


@router.get("/hello")
def root(user: Annotated[schemas.User, Depends(get_current_user)]):
    if user.is_admin:
        return f"Hello Admin {user.name}"
    else:
        return f"Hello User {user.name}"
    

@router.get("/info", response_model=schemas.User)
def info(user: Annotated[schemas.User, Security(get_current_user, scopes=["data_access"])]):
    return user