from sqlmodel import Session, select
from models.category import Category

def create_category(session: Session, category: Category):
    existing_category = session.exec(select(Category).where(Category.name == category.name)).first()
    if existing_category:
        raise ValueError(f"A category with name '{category.name}' already exists.")
    session.add(category)
    session.commit()
    session.refresh(category)
    return category

def get_categories(session: Session):
    return session.exec(select(Category)).all()

def get_category_by_id(session: Session, category_id: int):
    return session.get(Category, category_id)

def get_category_by_name(session: Session, name: str):
    statement = select(Category).where(Category.name == name)
    return session.exec(statement).first()

def update_category(session: Session, category_id: int, category_data: dict):
    category = session.get(Category, category_id)
    if not category:
        return None
    for key, value in category_data.items():
        setattr(category, key, value)
    category.id = category_id  # Ensure the ID remains unchanged
    session.commit()
    session.refresh(category)
    return category

def update_category_by_name(session: Session, name: str, category_data: dict):
    statement = select(Category).where(Category.name == name)
    category = session.exec(statement).first()
    if not category:
        return None
    for key, value in category_data.items():
        if key != "id":  # Prevent changing the ID
            setattr(category, key, value)
    session.commit()
    session.refresh(category)
    return category

def delete_category(session: Session, category_id: int):
    category = session.get(Category, category_id)
    if category:
        session.delete(category)
        session.commit()
    return category

def delete_category_by_name(session: Session, name: str):
    statement = select(Category).where(Category.name == name)
    category = session.exec(statement).first()
    if category:
        session.delete(category)
        session.commit()
    return category