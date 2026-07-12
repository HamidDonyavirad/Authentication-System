from pydantic import BaseModel, EmailStr

class ForgetPassword(BaseModel):
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    new_password: str