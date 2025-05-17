from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.jwt import create_access_token, revoke_token
from auth.hashing import hash_password, verify_password
from db.database import get_session
from models.user import User, UserCreate, UserRead
from auth.dependencies import get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post(
    "/login",
    operation_id="user_login",  # Especificamos un operationId único
)
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = session.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    try:
        revoke_token(token)
        return {"message": "Successfully logged out"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
