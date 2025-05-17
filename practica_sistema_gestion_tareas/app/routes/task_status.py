
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.task_status import TaskStatus, TaskStatusBase
from db.database import get_session
from crud.task_status import create_task_status, delete_task_status, get_task_statuses, update_task_status

router = APIRouter()

@router.post("/", response_model=TaskStatus, status_code=201)
def create(task_status: TaskStatusBase, session: Session = Depends(get_session)):
    """
    Create a new status.
    """
    try:
        task_status_data = TaskStatus(**task_status.model_dump())
        return create_task_status(session, task_status_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/", response_model=list[TaskStatus], status_code=200)
def find_all(session: Session = Depends(get_session)):
    """
    Find all tasks status in the system.
    """
    try:
        return get_task_statuses(session)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/{task_status_id}", response_model=TaskStatus)
def update(
    task_status_id: int,
    task_status_data: dict = Body(
        ...,
        examples={
            "name": "Completado",
            "color": "green"
        }
    ),
    session: Session = Depends(get_session),
):
    """
    Permite actualizar los datos de una estado.
    """
    try:
        updated_task_status = update_task_status(session, task_status_id, task_status_data)
        if not updated_task_status:
            raise HTTPException(status_code=404, detail=f"TaskStatus with ID {task_status_id} not found")
        return updated_task_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{task_status_id}", response_model=TaskStatus)
def update(
    task_status_id: int,
    session: Session = Depends(get_session),
):
    try:
        deleted_task_status = delete_task_status(session, task_status_id)
        if not deleted_task_status:
            raise HTTPException(status_code=404, detail=f"Task with ID {task_status_id} not found")
        return deleted_task_status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
