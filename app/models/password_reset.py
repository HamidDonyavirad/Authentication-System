from sqlalchemy import Column, Integer, String, ForeignKey, DateTime,Boolean
from sqlalchemy.orm import relationship

from app.core.database import Base

class PasswordResetToken(Base):
    __tablename__ = "password_reset_token"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String, nullable=False)
    expires_at = Column(DateTime)
    is_used = Column(Boolean, default=False)
    user = relationship("User", back_populates="reset_token")