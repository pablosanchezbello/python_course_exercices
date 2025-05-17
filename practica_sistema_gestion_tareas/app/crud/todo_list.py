from sqlmodel import Session, select
from models.todo_list import TodoList
from models.user import User
from crud.user import get_user_by_username

def create_todo_list(session: Session, todo_list: TodoList):
    existing_todo_list = session.exec(select(TodoList).where(TodoList.title == todo_list.title)).first()
    if existing_todo_list:
        raise ValueError(f"A TodoList with title '{todo_list.title}' already exists.")
    session.add(todo_list)
    session.commit()
    session.refresh(todo_list)
    return todo_list

def get_todo_lists(session: Session):
    return session.exec(select(TodoList)).all()

def get_todo_list_by_id(session: Session, todo_list_id: int):
    return session.get(TodoList, todo_list_id)

def get_todo_list_by_title(session: Session, title: str):
    statement = select(TodoList).where(TodoList.title == title)
    return session.exec(statement).first()

def get_todo_list_filtered(session: Session, id: int, owner_id: int, username: str, email: str, skip: int, limit: int):
    statement = select(TodoList)
    if id is not None:
        statement = statement.where(TodoList.id == id)
    if owner_id is not None:
        statement = statement.where(TodoList.owner_id == owner_id)
    if username is not None:
        statement = statement.where(TodoList.username == username)
    if email is not None:
        statement = statement.where(TodoList.email == email)
    if skip is not None and skip >= 0:
        statement = statement.offset(skip)
    if limit is not None and limit >= 0:
        statement = statement.limit(limit)
    return session.exec(statement).all()

def update_todo_list(session: Session, todo_list_id: int, todo_list_data: dict):
    todo_list = session.get(TodoList, todo_list_id)
    if not todo_list:
        return None
    for key, value in todo_list_data.items():
        setattr(todo_list, key, value)
    session.commit()
    session.refresh(todo_list)
    return todo_list

def update_todo_list_by_title(session: Session, title: str, todo_list_data: dict):
    statement = select(TodoList).where(TodoList.title == title)
    todo_list = session.exec(statement).first()
    if not todo_list:
        return None
    for key, value in todo_list_data.items():
        setattr(todo_list, key, value)
    session.commit()
    session.refresh(todo_list)
    return todo_list

def delete_todo_list(session: Session, todo_list_id: int):
    todo_list = session.get(TodoList, todo_list_id)
    if todo_list:
        session.delete(todo_list)
        session.commit()
    return todo_list

def delete_todo_list_by_title(session: Session, title: str):
    statement = select(TodoList).where(TodoList.title == title)
    todo_list = session.exec(statement).first()
    if todo_list:
        session.delete(todo_list)
        session.commit()
    return todo_list

def get_todo_list_by_user_username(session: Session, user_username: str):
    user = get_user_by_username(session, user_username)
    if not user:
        return []
    statement = select(TodoList).where(TodoList.owner_id == user.id)
    return session.exec(statement).all()
