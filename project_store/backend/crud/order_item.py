from sqlmodel import Session, select
from models.order_item import OrderItem
from sqlmodel import func

def _create_order_item(session: Session, order_item: OrderItem):
    session.add(order_item)
    session.commit()
    session.refresh(order_item)
    return order_item

def create_order_item(session: Session, order_item: OrderItem):
    existing_order_item = session.exec(select(OrderItem).where((OrderItem.order_id == order_item.order_id) & (OrderItem.product_id == order_item.product_id))).first()
    if not existing_order_item:
        return _create_order_item(session, order_item)
    else:
        existing_order_item.quantity = existing_order_item.quantity + order_item.quantity
        session.commit()
        session.refresh(existing_order_item)
        return existing_order_item

def update_order_item(session: Session, order_item: OrderItem):
    existing_order_item = session.exec(select(OrderItem).where((OrderItem.order_id == order_item.order_id) & (OrderItem.product_id == order_item.product_id))).first()
    if not existing_order_item:
        return _create_order_item(session, order_item)
    elif order_item.quantity <= 0:
        return delete_order_item_by_order_id_and_product_id(session, existing_order_item.order_id, existing_order_item.product_id)
    else:
        existing_order_item.quantity = order_item.quantity
        session.commit()
        session.refresh(existing_order_item)
        return existing_order_item

def delete_order_item_by_order_id_and_product_id(session: Session, order_id: int, product_id: int):
    order_item = session.exec(select(OrderItem).where((OrderItem.order_id == order_id) & (OrderItem.product_id == product_id))).first()
    if order_item:
        session.delete(order_item)
        session.commit()
    return order_item

def get_order_items_by_order_id(session: Session, order_id: int):
    return session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()

def get_order_items_by_product_id(session: Session, product_id: int):
    return session.exec(select(OrderItem).where(OrderItem.product_id == product_id)).all()

def get_order_item_by_order_id_and_product_id(session: Session, order_id: int, product_id: int):
    return session.exec(select(OrderItem).where((OrderItem.order_id == order_id) & (OrderItem.product_id == product_id))).first()

def products_ranking(session: Session):
    result = session.exec(
        select(
            OrderItem.product_id,
            func.sum(OrderItem.quantity).label("total_quantity")
        )
        .group_by(OrderItem.product_id)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(10)
    ).all()
    # Add rank position to each result
    ranked_result = [
        {"rank": idx + 1, "product_id": row[0], "total_quantity": row[1]}
        for idx, row in enumerate(result)
    ]
    return ranked_result