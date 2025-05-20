
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.task import Task, TaskBase
from db.database import get_session
from crud.task import create_task, delete_task, get_task_by_id, get_task_filtered, get_task_filtered_by_username, update_task
from auth.dependencies import require_role
from crud.todo_list import get_todo_list_by_id

router = APIRouter()

@router.post("/", response_model=Task, status_code=201)
def create(task: TaskBase, 
           session: Session = Depends(get_session),
           current_user: dict = Depends(require_role(["admin", "user"]))):
    """
    Create a new task.
    """
    try:
        task_data = Task(**task.model_dump())
        return create_task(session, task_data)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=list[Task], status_code=200)
def find_all(todo_list_id: int = None, 
             is_completed: bool = None, 
             skip: int = None, 
             limit: int = None, 
             session: Session = Depends(get_session),
             current_user: dict = Depends(require_role(["admin", "user", "viewer"])),):
    """
    Find all tasks in the system.
    Filter options as queryParams:
        * todo_list_id: Filtra las tareas pertenecientes a una lista específica.
        * is_completed: Filtra las tareas según su estado de finalización (true o false).
        * skip: Número de registros a omitir (paginación).
        * limit: Número máximo de registros a devolver (paginación).

    """
    try:
        if current_user["role"] == "user":
            return get_task_filtered_by_username(session, username=current_user["sub"],todo_list_id=todo_list_id, is_completed=is_completed, skip=skip, limit=limit)
        else:
            return get_task_filtered(session, todo_list_id=todo_list_id, is_completed=is_completed, skip=skip, limit=limit)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{task_id}", response_model=Task)
def update(
    task_id: int,
    task_data: dict = Body(
        ...,
        examples={
            "title": "Comprar leche y pan",
            "description": "Ir al supermercado y comprar leche y pan",
            "is_completed": "true",
            "status_id": "2"
        }
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "user"])),
):
    """
    Permite actualizar los datos de una tarea, incluyendo su estado (status_id).
    """
    try:
        task_updateable = get_task_by_id(task_id)
        if task_updateable:
            todo_list = get_todo_list_by_id(session, task_updateable.todo_list_id)
            if current_user["role"] == "user" and todo_list.owner_username != current_user["sub"]:
                raise HTTPException(status_code=403, detail=f"Task with ID {task_id} not permitted")
            updated_task = update_task(session, task_id, task_data)
            return updated_task
        else:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{task_id}", response_model=Task)
def update(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "user"])),
):
    try:
        task_to_delete = get_task_by_id(task_id)
        if task_to_delete:
            todo_list = get_todo_list_by_id(session, task_to_delete.todo_list_id)
            if current_user["role"] == "user" and todo_list.owner_username != current_user["sub"]:
                raise HTTPException(status_code=403, detail=f"Task with ID {task_id} not permitted")
            deleted_task = delete_task(session, task_id)
            return deleted_task    
        else:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
