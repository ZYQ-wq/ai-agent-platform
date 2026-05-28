from pydantic import BaseModel,Field

class RegisterRequest(BaseModel):
    username:str
    email:str
    password:str


class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str