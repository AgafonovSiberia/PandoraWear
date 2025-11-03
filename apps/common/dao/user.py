from pydantic import BaseModel, ConfigDict


class User(BaseModel):
    id: int
    username: str
    email: str
    active: bool

    model_config = ConfigDict(from_attributes=True)

class AuthUser(User):
    ...


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


class PandoraCredIn(BaseModel):
    user_id: int
    email: str
    password: str


class PandoraCredDomain(BaseModel):
    user_id: int
    email: str
    password: str

    model_config = ConfigDict(from_attributes=True)


class UserData(BaseModel):
    user_id: int
    session_id: str
    pandora: PandoraCredDomain
