from sqlmodel import Session, select
from models.author import Author

def create_author(session: Session, author: Author):
    existing_author = session.exec(select(Author).where((Author.email == author.email) & (Author.is_deleted == False))).first()
    if existing_author:
        raise ValueError(f"An author with email '{author.email}' already exists.")
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

def get_authors(session: Session, order_by: str = None):
    if order_by == None or order_by == "name":
        return session.exec(select(Author).where(Author.is_deleted == False).order_by(order_by)).all()
    else:
        return []

def get_author_by_id(session: Session, author_id: int):
    return session.exec(select(Author).where((Author.id == author_id) & (Author.is_deleted == False))).first()

def get_author_by_name(session: Session, name: str):
    statement = select(Author).where((Author.name == name) & (Author.is_deleted == False))
    return session.exec(statement).first()

def update_author(session: Session, author_id: int, author_data: dict):
    author = session.exec(select(Author).where((Author.id == author_id) & (Author.is_deleted == False))).first()
    if not author:
        return None
    for key, value in author_data.items():
        setattr(author, key, value)
    author.id = author_id  # Ensure the ID remains unchanged
    session.commit()
    session.refresh(author)
    return author

def update_author_by_name(session: Session, name: str, author_data: dict):
    statement = select(Author).where((Author.name == name) & (Author.is_deleted == False))
    author = session.exec(statement).first()
    if not author:
        return None
    for key, value in author_data.items():
        if key != "id":
            setattr(author, key, value)
    session.commit()
    session.refresh(author)
    return author

def delete_author(session: Session, author_id: int):
    author = session.get(Author, author_id)
    if author:
        author.is_deleted = True
        session.commit()
        session.refresh(author)
    return author

def delete_author_by_name(session: Session, name: str):
    statement = select(Author).where(Author.name == name)
    author = session.exec(statement).first()
    if author:
        author.is_deleted = True
        session.commit()
        session.refresh(author)
    return author