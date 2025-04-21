from sqlmodel import Session, select
from models.entry import Entry
from models.author import Author
from crud.author import get_author_by_name

def create_entry(session: Session, entry: Entry):
    existing_entry = session.exec(select(Entry).where((Entry.title == entry.title) & (Entry.is_deleted == False))).first()
    if existing_entry:
        raise ValueError(f"An entry with title '{entry.title}' already exists.")
    session.add(entry)
    session.commit()
    session.refresh(entry)
    return entry

def get_entries(session: Session, order_by: str = None):
    if order_by == None or order_by == "title":
        return session.exec(select(Entry).where(Entry.is_deleted == False).order_by(order_by)).all()
    else:
        return []

def get_entry_by_id(session: Session, entry_id: int):
    return session.exec(select(Entry).where((Entry.id == entry_id) & (Entry.is_deleted == False))).first()

def get_entry_by_title(session: Session, title: str):
    statement = select(Entry).where((Entry.title == title) & (Entry.is_deleted == False))
    return session.exec(statement).first()

def update_entry(session: Session, entry_id: int, entry_data: dict):
    entry = session.exec(select(Entry).where(Entry.id == entry_id & Entry.is_deleted == False)).first()
    if not entry:
        return None
    for key, value in entry_data.items():
        setattr(entry, key, value)
    entry.id = entry_id  # Ensure the ID remains unchanged
    session.commit()
    session.refresh(entry)
    return entry

def update_entry_by_title(session: Session, title: str, entry_data: dict):
    statement = select(Entry).where((Entry.title == title) & (Entry.is_deleted == False))
    entry = session.exec(statement).first()
    if not entry:
        return None
    for key, value in entry_data.items():
        if key != "id":
            setattr(entry, key, value)
    session.commit()
    session.refresh(entry)
    return entry

def delete_entry(session: Session, entry_id: int):
    entry = session.exec(select(Entry).where((Entry.id == entry_id) & (Entry.is_deleted == False))).first()
    if entry:
        entry.is_deleted = True
        session.commit()
        session.refresh(entry)
    return entry

def delete_entry_by_title(session: Session, title: str):
    statement = select(Entry).where((Entry.title == title) & (Entry.is_deleted == False))
    entry = session.exec(statement).first()
    if entry:
        entry.is_deleted = True
        session.commit()
        session.refresh(entry)
    return entry

def get_entries_by_author_name(session: Session, author_name: str):
    author = get_author_by_name(session, author_name)
    if not author:
        return []
    statement = select(Entry).join(Author, Entry.author_id == Author.id).where((Entry.is_deleted == False) & (Author.name == author_name))
    return session.exec(statement).all()