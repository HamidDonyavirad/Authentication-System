from sqlalchemy import Column, Integer, String,Boolean,DateTime
from app.core.database import Base
from datetime import datetime,timezone
from sqlalchemy.orm import relationship


def utc_now():
    return datetime.now(timezone.utc)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String,index=True,nullable=False,unique=True)
    hashed_password = Column(String,nullable=True)
    provider = Column(String,default="local") #Statuses : local, google
    is_active = Column(Boolean,default=True)
    is_verified = Column(Boolean,default=False)
    created_at = Column(DateTime,default=utc_now)

    tasks = relationship('Task',back_populates="owner",cascade="all,delete-orphan")
    reset_tokens = relationship("PasswordResetToken",back_populates="user",cascade="all,delete-orphan")
    refresh_tokens = relationship("RefreshToken",back_populates="user",cascade="all,delete-orphan")

