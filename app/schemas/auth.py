from pydantic import BaseModel,EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenSchema(BaseModel):
    access_token: str
    refresh_token: str

class LogoutSchema(BaseModel):
    refresh_token: str