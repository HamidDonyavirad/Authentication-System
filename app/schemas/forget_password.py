from pydantic import BaseModel, EmailStr

class ForgetPassword(BaseModel):
    email: EmailStr

