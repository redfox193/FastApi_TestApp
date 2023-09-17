from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    name: str
    email: str
    is_admin: bool

class UserCreate(UserBase):
    password: str


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    hashed_password: str