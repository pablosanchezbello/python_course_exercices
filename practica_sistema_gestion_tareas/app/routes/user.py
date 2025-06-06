
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.user import User, UserCreate, UserResponse
from db.database import get_session
from crud.user import create_user, delete_user, get_users_filtered, update_user
from auth.dependencies import require_role


router = APIRouter()

@router.get("/", response_model=list[UserResponse], status_code=200)
def find_all(id: int = None, 
             username: str = None, 
             email: str = None, 
             skip: int = None, 
             limit: int = None, 
             session: Session = Depends(get_session),
             current_user: dict = Depends(require_role(["admin"])),):
    """
    Find all users in the system.
    Filter options as queryParams:
        * id: Filtra por el ID del usuario.
        * username: Filtra por el nombre de usuario.
        * email: Filtra por el correo electrónico.
        * skip: Número de registros a omitir (paginación).
        * limit: Número máximo de registros a devolver (paginación).
    """
    try:
        return get_users_filtered(session, id=id, username=username, email=email, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.post("/", response_model=UserResponse, status_code=201)
def create(user: UserCreate, 
           session: Session = Depends(get_session),
           current_user: dict = Depends(require_role(["admin"])),):
    """
    Create a new user in the system.
    """
    try:
        user_data = User(**user.model_dump())
        return create_user(session, user_data)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    user_data: dict = Body(
        ...,
        examples={
            "username": "updated_user_name",
            "email": "updated_email@example.com",
            "password": "Password for the user"
        }
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin"])),
):
    try:
        updated_user = update_user(session, user_id, user_data)
        if not updated_user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return updated_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{user_id}", response_model=UserResponse)
def update(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin"])),
):
    try:
        deleted_user = delete_user(session, user_id)
        if not deleted_user:
            raise HTTPException(status_code=404, detail=f"User with ID {user_id} not found")
        return deleted_user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
