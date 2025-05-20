from sqlmodel import Session, select
from models.task import Task
from models.task_status import TaskStatus
from crud.task_status import get_task_status_by_name
from models.todo_list import TodoList

def create_task(session: Session, task: Task):
    existing_task = session.exec(select(Task).where(Task.title == task.title)).first()
    if existing_task:
        raise ValueError(f"A task with title '{task.title}' already exists.")
    session.add(task)
    session.commit()
    session.refresh(task)
    return task

def get_tasks(session: Session):
    return session.exec(select(Task)).all()

def get_task_by_id(session: Session, task_id: int):
    return session.get(Task, task_id)

def get_task_by_title(session: Session, title: str):
    statement = select(Task).where(Task.title == title)
    return session.exec(statement).first()

def get_task_filtered(session: Session, todo_list_id: int, is_completed: bool, skip: int, limit: int):
    statement = select(Task)
    if todo_list_id is not None:
        statement = statement.where(Task.todo_list_id == todo_list_id)
    if is_completed is not None:
        statement = statement.where(Task.is_completed == is_completed)
    if skip is not None and skip >= 0:
        statement = statement.offset(skip)
    if limit is not None and limit >= 0:
        statement = statement.limit(limit)
    return session.exec(statement).all()

def get_task_filtered_by_username(session: Session, username: str, todo_list_id: int, is_completed: bool, skip: int, limit: int):
    statement = select(Task).join(TodoList, TodoList.id == Task.todo_list_id).where(TodoList.owner_username == username)
    if todo_list_id is not None:
        statement = statement.where(Task.todo_list_id == todo_list_id)
    if is_completed is not None:
        statement = statement.where(Task.is_completed == is_completed)
    if skip is not None and skip >= 0:
        statement = statement.offset(skip)
    if limit is not None and limit >= 0:
        statement = statement.limit(limit)
    return session.exec(statement).all()

def update_task(session: Session, task_id: int, task_data: dict):
    task = session.get(Task, task_id)
    if not task:
        return None
    for key, value in task_data.items():
        setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task

def update_task_by_title(session: Session, title: str, task_data: dict):
    statement = select(Task).where(Task.title == title)
    task = session.exec(statement).first()
    if not task:
        return None
    for key, value in task_data.items():
        setattr(task, key, value)
    session.commit()
    session.refresh(task)
    return task

def delete_task(session: Session, task_id: int):
    task = session.get(Task, task_id)
    if task:
        session.delete(task)
        session.commit()
    return task

def delete_task_by_title(session: Session, title: str):
    statement = select(Task).where(Task.title == title)
    task = session.exec(statement).first()
    if task:
        session.delete(task)
        session.commit()
    return task

def get_tasks_by_task_status_name(session: Session, task_status_name: str):
    task_status = get_task_status_by_name(session, task_status_name)
    if not task_status:
        return []
    statement = select(Task).where(Task.status_id == task_status.id)
    return session.exec(statement).all()