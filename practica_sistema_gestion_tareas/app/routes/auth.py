from fastapi import APIRouter, Depends, HTTPException, Form, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlmodel import Session
from auth.jwt import create_access_token, create_refresh_token, verify_refresh_token, verify_access_token
from auth.jwt import revoke_token as revoke_token_memory
from auth.hashing import hash_password, verify_password
from db.database import get_session
from auth.dependencies import get_current_user, oauth2_scheme
from models.user import UserBase, UserCreate, UserResponse, User
from crud.user import get_user_by_email, get_user_by_username
from auth.redis import revoke_token as revoke_token_redis

router = APIRouter()

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = get_user_by_username(session, user.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    hashed_password = hash_password(user.password)
    new_user = User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        role=user.role  # rol user
    )
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = get_user_by_username(session, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_access_token({"sub": user.username}, role=user.role)
    refresh_token = create_refresh_token({"sub": user.username})
    user.refresh_token = refresh_token
    session.add(user)
    session.commit()
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(refresh_token: str, session: Session = Depends(get_session)):
    payload = verify_refresh_token(refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    user = session.query(User).filter(User.refresh_token == refresh_token).first()
    user = get_user_by_username(session, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    new_access_token = create_access_token({"sub": user.username}, role=user.role)
    return {"access_token": new_access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(current_user: dict = Depends(get_current_user), token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):
    user = get_user_by_username(session, current_user["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.refresh_token = None
    session.add(user)
    session.commit()

    # Revocar el token de acceso
    revoke_token_memory(token)
    revoke_token_redis(token)

    return {"message": "Successfully logged out"}

@router.post("/forgot-password")
def forgot_password(email: str = Form(...), session: Session = Depends(get_session)):
    user = get_user_by_email(session, email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generar token de recuperación
    token = create_access_token({"sub": user.email}, role="reset", expires_minutes=15)
    
    # Devolver el token directamente
    return {"message": "Use this token to reset your password", "token": token}

@router.post("/reset-password")
def reset_password(token: str = Form(...), new_password: str = Form(...), session: Session = Depends(get_session)):
    payload = verify_access_token(token)
    if not payload or payload.get("role") != "reset":
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    user = get_user_by_username(session, payload["sub"])
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Actualizar contraseña
    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()

    return RedirectResponse(url="/", status_code=303)
