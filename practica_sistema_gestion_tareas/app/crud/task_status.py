from sqlmodel import Session, select
from models.task_status import TaskStatus
from exceptions.status_task_in_use import StatusTaskInUseException

def create_task_status(session: Session, task_status: TaskStatus):
    existing_task_status = session.exec(select(TaskStatus).where(TaskStatus.name == task_status.name)).first()
    if existing_task_status:
        raise ValueError(f"A task_status with name '{task_status.name}' already exists.")
    session.add(task_status)
    session.commit()
    session.refresh(task_status)
    return task_status

def get_task_statuses(session: Session):
    return session.exec(select(TaskStatus)).all()

def get_task_status_by_id(session: Session, task_status_id: int):
    return session.get(TaskStatus, task_status_id)

def get_task_status_by_name(session: Session, name: str):
    statement = select(TaskStatus).where(TaskStatus.name == name)
    return session.exec(statement).first()

def update_task_status(session: Session, task_status_id: int, task_status_data: dict):
    task_status = session.get(TaskStatus, task_status_id)
    if not task_status:
        return None
    for key, value in task_status_data.items():
        setattr(task_status, key, value)
    session.commit()
    session.refresh(task_status)
    return task_status

def update_task_status_by_name(session: Session, name: str, task_status_data: dict):
    statement = select(TaskStatus).where(TaskStatus.name == name)
    task_status = session.exec(statement).first()
    if not task_status:
        return None
    for key, value in task_status_data.items():
        setattr(task_status, key, value)
    session.commit()
    session.refresh(task_status)
    return task_status

def delete_task_status(session: Session, task_status_id: int):
    from crud.task import get_tasks_by_task_status_name
    task_status = session.get(TaskStatus, task_status_id)
    if task_status:
        in_use_status = get_tasks_by_task_status_name(session, task_status.name)
        if in_use_status != None and len(in_use_status) > 0:
            raise StatusTaskInUseException()
        session.delete(task_status)
        session.commit()
    return task_status

def delete_task_status_by_name(session: Session, name: str):
    from crud.task import get_tasks_by_task_status_name
    statement = select(TaskStatus).where(TaskStatus.name == name)
    task_status = session.exec(statement).first()
    if task_status:
        in_use_status = get_tasks_by_task_status_name(session, task_status.name)
        if in_use_status != None and len(in_use_status) > 0:
            raise StatusTaskInUseException()
        session.delete(task_status)
        session.commit()
    return task_status