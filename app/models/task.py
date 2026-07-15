from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.sql import  func

from sqlalchemy.orm import relationship
from app.core.database import Base

class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    category = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    owner_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    owner = relationship("User", back_populates="tasks")