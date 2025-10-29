from pydantic import BaseModel


class User(BaseModel):
    user_id: int
    email: str
    password_hash: str


class FormUserReg(BaseModel):
    name: str
    email: str
    password: str


class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserPandoraCredIn(BaseModel):
    email: str
    password: str


class UserPandoraCred(BaseModel):
    user_id: int
    pandora_email: str
    pandora_password: str


class SessionIn(BaseModel):
    user_id: int
    pandora_user_id: int
    pandora_session_id: str


class Session(BaseModel):
    user_id: int
    pandora_user_id: int
    pandora_session_id: str
