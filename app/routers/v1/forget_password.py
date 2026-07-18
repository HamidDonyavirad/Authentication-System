from fastapi import Depends,APIRouter,HTTPException,Request
from sqlalchemy.orm import Session
import  secrets
from datetime import datetime, timedelta, timezone


from app.dependencies.dep_database import get_db
from app.models.password_reset import PasswordResetToken
from app.schemas.password_reset import ForgetPassword, ResetPassword
from app.models.user import User
from app.core.security import hash_password
from app.core.limiter import limiter

router = APIRouter( prefix="/auth",tags=["forget"])

@router.post("/forget-password")
@limiter.limit("2/minute")
async def forget_password(data: ForgetPassword,request:Request,db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==data.email).first()
    if not user:
        return {"message":
    "If the email exists, a reset link has been sent."}
    token = secrets.token_urlsafe(32)
    expires = datetime.now(timezone.utc) + timedelta(minutes=30)
    reset = PasswordResetToken(
        token=token,
        user_id=user.id,
        expires_at=expires,
    )
    db.add(reset)
    db.commit()

    #Need to connect to email service
    print(
        f"http://localhost:8000/reset-password?token={token}"
    )
    return {
        "message":
            "If the email exists, a reset link has been sent."
    }

@router.post("/reset-password")
@limiter.limit("5/minute")
async  def reset_password(data: ResetPassword,request:Request,db: Session = Depends(get_db)):
    reset = db.query(PasswordResetToken).filter(
        PasswordResetToken.token==data.token
    ).first()
    if not reset:
        raise HTTPException(status_code=400, detail="Invalid token")
    if reset.is_used :
        raise HTTPException(status_code=400, detail="Token already used")
    if reset.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=400, detail="Token expired")
    user = db.query(User).get(reset.user_id)
    user.hashed_password = hash_password(data.new_password)
    reset.is_used = True
    db.commit()
    return {
        "message":
            "Password changed successfully"
    }


