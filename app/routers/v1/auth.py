from fastapi import Depends,HTTPException,APIRouter
from sqlalchemy.orm import Session

from app.dependencies.dep_database import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.user import UserResponse
from app.core.security import hash_password

from app.schemas.auth import Token,LoginSchema
from app.core.security import verify_password,create_access_token,get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

@router.post("/signup", response_model=UserResponse)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
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
async def login(user_data: LoginSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email==user_data.email).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    is_valid_password = verify_password(user_data.password, user.hashed_password)
    if not is_valid_password:
        raise HTTPException(status_code=401, detail="Incorrect password")

    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
async def grt_me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}