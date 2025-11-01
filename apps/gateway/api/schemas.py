from pydantic import constr, BaseModel

PairCode = constr(pattern=r"^[0-9]{6}$")


class FormUserReg(BaseModel):
    name: str
    email: str
    password: str
