
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.todo_list import TodoList, TodoListBase
from db.database import get_session
from crud.todo_list import create_todo_list, delete_todo_list, get_todo_list_by_id, get_todo_list_filtered, update_todo_list
from auth.dependencies import require_role

router = APIRouter()

@router.post("/", response_model=TodoList, status_code=201)
def create(todo_list: TodoListBase, session: Session = Depends(get_session), current_user: dict = Depends(require_role(["admin", "user"]))):
    """
    Create a new list.
    """
    try:
        todo_list_data = TodoList(**todo_list.model_dump())
        return create_todo_list(session, todo_list_data)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[TodoList], status_code=200)
def find_all(id: int = None, owner_id: int = None, username: str = None, email: str = None, skip: int = None, limit: int = None, session: Session = Depends(get_session), 
             current_user: dict = Depends(require_role(["admin", "user", "viewer"]))):
    """
    Find all todoLists in the system.
    Filter options as queryParams:
        * id: Filtra por el ID de la lista.
        * owner_id: Filtra por el ID del propietario.
        * username: Filtra por el nombre de usuario del propietario.
        * email: Filtra por el correo electrónico del propietario.
        * skip: Número de registros a omitir (paginación).
        * limit: Número máximo de registros a devolver (paginación).
    """
    try:
        if current_user["role"] == "admin" or current_user["role"] == "viewer" :
            return get_todo_list_filtered(session, id=id, owner_id=owner_id, username=username, email=email, skip=skip, limit=limit)
        if current_user["role"] == "user":
            return get_todo_list_filtered(session, id=id, owner_id=owner_id, username=current_user["sub"], email=email, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.put("/{todo_list_id}", response_model=TodoList)
def update(
    todo_list_id: int,
    todo_list_data: dict = Body(
        ...,
        examples={
            "title": "Title of the TodoList",
            "description": "Description of the TodoList"
        }
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "user"])),
):
    try:
        todo_list_to_be_updated = get_todo_list_by_id(session, todo_list_id)
        if current_user["role"] == "user" and (not todo_list_to_be_updated or todo_list_to_be_updated.owner_username != current_user["sub"]):
            raise HTTPException(status_code=403, detail=f"TodoList with ID {todo_list_id} not permitted")
        updated_todo_list = update_todo_list(session, todo_list_id, todo_list_data)
        if not updated_todo_list:
            raise HTTPException(status_code=404, detail=f"TodoList with ID {todo_list_id} not found")
        return updated_todo_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{todo_list_id}", response_model=TodoList)
def update(
    todo_list_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "user"])),
):
    try:
        todo_list_to_delete = get_todo_list_by_id(session, todo_list_id)
        if current_user["role"] == "user" and (not todo_list_to_delete or todo_list_to_delete.owner_username != current_user["sub"]):
            raise HTTPException(status_code=403, detail=f"TodoList with ID {todo_list_id} not permitted")
        deleted_todo_list = delete_todo_list(session, todo_list_id)
        if not deleted_todo_list:
            raise HTTPException(status_code=404, detail=f"TodoList with ID {todo_list_id} not found")
        return deleted_todo_list
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
