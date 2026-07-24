
from fastapi import Depends,HTTPException,APIRouter,Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone

from app.core import database
from app.dependencies.dep_database import get_db
from app.models.refresh_token import RefreshToken,refresh_token_expiry
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.core.security import hash_password, hash_refresh_token, verify_refresh_token
from app.schemas.auth import Token, LoginSchema, LogoutSchema, RefreshTokenSchema
from app.core.security import verify_password,create_access_token,get_current_user,create_refresh_token
from app.core.limiter import limiter
router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse)
@limiter.limit("5/minute")
async def signup(user_data: UserCreate,request: Request, db: Session = Depends(get_db)):
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = hash_password(user_data.password)

    new_user = User(email=user_data.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
async def login(user_data: LoginSchema,request: Request, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    is_valid_password = verify_password(user_data.password, user.hashed_password)
    if not is_valid_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token_str =create_refresh_token(data={"sub": user.email})
    hashed_refresh_token = hash_refresh_token(refresh_token_str)
    refresh_token = RefreshToken(
        user_id=user.id,
        hashed_token=hashed_refresh_token,
        expires_at=refresh_token_expiry())
    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)
    return {"access_token": access_token,"refresh_token": refresh_token_str}

@router.get("/me")
async def grt_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}

@router.post("/refresh")
@limiter.limit("5/minute")
async def token_refresh(data:RefreshTokenSchema,db: Session = Depends(get_db)):
    refresh_token = data.refresh_token
    payload = verify_refresh_token(refresh_token)
    hashed_refresh_token = hash_refresh_token(refresh_token)
    token_record = db.query(RefreshToken).filter(
        RefreshToken.hashed_token == hashed_refresh_token,
    ).first()
    if not token_record:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")
    if token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token is expired")
    if token_record.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")
    user = token_record.user
    token_record.is_revoked = True
    access_token = create_access_token(data={"sub": user.email})
    new_refresh_token = create_refresh_token(data={"sub": user.email})
    new_hashed_refresh_token = hash_refresh_token(new_refresh_token)
    new_refresh_token_record = RefreshToken(
        user_id=user.id,
        hashed_token=new_hashed_refresh_token,
        expires_at=refresh_token_expiry(),
    )
    db.add(new_refresh_token_record)
    try:
        db.commit()
    except Exception :
        db.rollback()
        raise
    return {"access_token": access_token,"refresh_token": new_refresh_token}


@router.post("/logout")
async def logout(data:LogoutSchema, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    refresh_token = data.refresh_token
    hashed_refresh_token = hash_refresh_token(refresh_token)
    token_record = db.query(RefreshToken).filter(
                RefreshToken.hashed_token == hashed_refresh_token,
                RefreshToken.user_id == current_user.id
                ).first()
    if not token_record:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")
    if token_record.expires_at < datetime.now(timezone.utc):
        raise HTTPException(status_code=401, detail="Refresh token is expired")
    if token_record.is_revoked:
        raise HTTPException(status_code=401, detail="Refresh token is invalid")
    token_record.is_revoked = True
    try:
        db.commit()
    except Exception :
        db.rollback()
        raise
    return HTTPException(status_code=204, detail="Successfully logged out")
