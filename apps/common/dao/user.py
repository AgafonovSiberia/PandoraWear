from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


class AuthUser(User):
    token: str


class UserDomain(User):
    password_hash: bytes


class UserInLogin(BaseModel):
    email: str
    password: str


class UserInRegister(BaseModel):
    username: str = None
    email: str
    password: str


class CreateUser(BaseModel):
    username: str
    email: str
    password_hash: bytes
