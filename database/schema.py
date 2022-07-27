from pydantic import BaseModel


class Login(BaseModel):
    email: str
    password: str


class User(BaseModel):
    email: str
    password: str
    name: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserFeed(BaseModel):
    name: str
    error: str or None = None
    class Config():
        orm_mode= True

class activeUser(BaseModel):
    email : str
    token : str