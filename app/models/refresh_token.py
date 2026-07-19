from sqlalchemy import Column, DateTime, Integer, String,ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.core.database import Base

def utc_now():
    return datetime.now(timezone.utc)

def refresh_token_expiry():
    return datetime.now(timezone.utc)+timedelta(days=7)

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"),index=True,nullable=False)
    hashed_token = Column(String,index=True,nullable=False)
    created_at = Column(DateTime,default=utc_now)
    expires_at = Column(DateTime,default=refresh_token_expiry,timezone=True,nullable=False)
    is_revoked = Column(Boolean, default=False)

    user = relationship("User", back_populates="refresh_tokens")