from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str
    role: str


class UserLogin(BaseModel):
    email: str
    password: str