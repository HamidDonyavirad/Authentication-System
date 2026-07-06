from pydantic import BaseModel, EmailStr, Field,ConfigDict
from datetime import datetime



class UserCreate (BaseModel):
    email: EmailStr
    hashed_password: str = Field(min_length=8,max_length=64)

class UserResponse (BaseModel):
    id: int
    email: EmailStr
    provider: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)