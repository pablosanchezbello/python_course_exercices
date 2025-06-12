from sqlmodel import Session, select
from models.user import User

def create_user(session: Session, user: User):
    existing_user = session.exec(select(User).where(User.email == user.email)).first()
    if existing_user:
        raise ValueError(f"An user with email '{user.email}' already exists.")
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session):
    return session.exec(select(User).where(User.username != "anonymous")).all()

def get_user_by_id(session: Session, user_id: int):
    return session.exec(select(User).where((User.id == user_id) & (User.username != "anonymous"))).first()

def get_user_by_username(session: Session, username: str):
    statement = select(User).where((User.username == username) & (User.username != "anonymous"))
    return session.exec(statement).first()

def get_user_by_email(session: Session, email: str):
    statement = select(User).where((User.email == email) & (User.username != "anonymous"))
    return session.exec(statement).first()

def get_users_filtered(session: Session, id: int, username: str, email: str, skip: int, limit: int):
    statement = select(User)
    statement = statement.where(User.username != "anonymous")
    if id is not None:
        statement = statement.where(User.id == id)
    if username is not None:
        statement = statement.where(User.username == username)
    if email is not None:
        statement = statement.where(User.email == email)
    if skip is not None and skip >= 0:
        statement = statement.offset(skip)
    if limit is not None and limit >= 0:
        statement = statement.limit(limit)
    return session.exec(statement).all()

def update_user(session: Session, user_id: int, user_data: dict):
    user = session.exec(select(User).where((User.id == user_id) & (User.username != "anonymous"))).first()
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user

def update_user_by_username(session: Session, username: str, user_data: dict):
    statement = select(User).where((User.username == username) & (User.username != "anonymous"))
    user = session.exec(statement).first()
    if not user:
        return None
    for key, value in user_data.items():
        setattr(user, key, value)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int):
    user = session.exec(select(User).where((User.id == user_id) & (User.username != "anonymous"))).first()
    if user:
        session.delete(user)
        session.commit()
    return user

def delete_user_by_username(session: Session, username: str):
    statement = select(User).where((User.username == username) & (User.username != "anonymous"))
    user = session.exec(statement).first()
    if user:
        session.delete(user)
        session.commit()
    return user