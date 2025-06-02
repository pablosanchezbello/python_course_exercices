from sqlmodel import Session, select
from models.order import Order
from models.user import User
from crud.user import get_user_by_id

def create_order(session: Session, order: Order):
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

def get_orders(session: Session):
    return session.exec(select(Order)).all()

def get_order_by_id(session: Session, id: int, user_id: int):
    statement = select(Order)
    if id is not None:
        statement = statement.where(Order.id == id)
    if user_id is not None:
        statement = statement.where(Order.user_id == user_id)
    return session.exec(statement).first()

def get_orders_filtered(session: Session, id: int, user_id: int, skip: int, limit: int):
    statement = select(Order)
    if id is not None:
        statement = statement.where(Order.id == id)
    if user_id is not None:
        statement = statement.where(Order.user_id == user_id)
    if skip is not None and skip >= 0:
        statement = statement.offset(skip)
    if limit is not None and limit >= 0:
        statement = statement.limit(limit)
    return session.exec(statement).all()

def update_order(session: Session, order_id: int, order_data: dict):
    order = session.get(Order, order_id)
    if not order:
        return None
    if not order_data['status'] in ['in progress', 'paid', 'delivered', 'cancelled']:
        raise ValueError("Invalid order status. Possible values are: 'in progress', 'paid', 'delivered', 'cancelled'.")
    for key, value in order_data.items():
        setattr(order, key, value)
    session.commit()
    session.refresh(order)
    return order

def delete_order(session: Session, order_id: int, user_id: int):
    order = get_order_by_id(session, order_id, user_id)
    if order:
        anonymous_user = session.exec(select(User).where(User.username == "anonymous")).first()
        if anonymous_user:
            order.user_id = anonymous_user.id
            order.owner_username = anonymous_user.username
            session.commit()
    return order

def get_order_by_user_id(session: Session, user_id: int):
    user = get_user_by_id(session, user_id)
    if not user:
        return []
    statement = select(Order).where(Order.user_id == user.id)
    return session.exec(statement).all()
