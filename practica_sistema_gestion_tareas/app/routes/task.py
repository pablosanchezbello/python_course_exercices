
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.task import Task, TaskBase
from db.database import get_session
from crud.task import create_task, delete_task, get_task_filtered, update_task

router = APIRouter()

@router.post("/", response_model=Task, status_code=201)
def create(task: TaskBase, session: Session = Depends(get_session)):
    """
    Create a new task.
    """
    try:
        task_data = Task(**task.model_dump())
        return create_task(session, task_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=list[Task], status_code=200)
def find_all(todo_list_id: int = None, is_completed: bool = None, skip: int = None, limit: int = None, session: Session = Depends(get_session)):
    """
    Find all tasks in the system.
    Filter options as queryParams:
        * todo_list_id: Filtra las tareas pertenecientes a una lista específica.
        * is_completed: Filtra las tareas según su estado de finalización (true o false).
        * skip: Número de registros a omitir (paginación).
        * limit: Número máximo de registros a devolver (paginación).

    """
    try:
        return get_task_filtered(session, todo_list_id=todo_list_id, is_completed=is_completed, skip=skip, limit=limit)
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
):
    """
    Permite actualizar los datos de una tarea, incluyendo su estado (status_id).
    """
    try:
        updated_task = update_task(session, task_id, task_data)
        if not updated_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        return updated_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{task_id}", response_model=Task)
def update(
    task_id: int,
    session: Session = Depends(get_session),
):
    try:
        deleted_task = delete_task(session, task_id)
        if not deleted_task:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
        return deleted_task
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
