from sqlalchemy import Column, Integer, String,Boolean,DateTime
from app.core.database import Base
from datetime import datetime,timezone
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True,index=True)
    email = Column(String,index=True,nullable=False,unique=True)
    hashed_password = Column(String,nullable=True)
    provider = Column(String,default="local") #Statuses : local, google
    is_active = Column(Boolean,default=True)
    is_verified = Column(Boolean,default=False)
    created_at = Column(DateTime,default=datetime.now(timezone.utc))

    tasks = relationship('Task',back_populates="owner")



