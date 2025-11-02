from pydantic import BaseModel, ConfigDict


class UserDomain(BaseModel):
    id: int
    username: str = None
    email: str
    password_hash: str
    active: bool

    model_config = ConfigDict(from_attributes=True)


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
    password_hash: str


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
