from pydantic import BaseModel


class SessionDomain(BaseModel):
    use_id: int


class SessionIn(BaseModel):
    user_id: int
    pandora_user_id: int
    pandora_session_id: str
