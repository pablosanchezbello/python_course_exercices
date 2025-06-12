
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from db.database import get_session
from auth.dependencies import require_role
from models.order_item import OrderItem
from crud.order_item import create_order_item, delete_order_item_by_order_id_and_product_id, get_order_item_by_order_id_and_product_id, update_order_item
from crud.order import get_order_by_id

router = APIRouter()

@router.post("/", response_model=OrderItem, status_code=201)
def create(task: OrderItem, 
           session: Session = Depends(get_session),
           current_user: dict = Depends(require_role(["admin", "cliente"]))):
    """
    Create a new Order Item.
    """
    try:
        order_item = OrderItem(**task.model_dump())
        return create_order_item(session, order_item)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.put("/", response_model=OrderItem)
def update(
    order_id: int, # Captured from pre-path defined in main.py
    order_item_data: dict = Body(
        ...,
        examples={
            "order_id": "ID of the order",
            "product_id": "ID of the product",
            "quantity": "Quantity of the product ordered"
        }
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "cliente"])),
):
    """
    Permite actualizar los datos de un Order Item.
    """
    try:
        product_id = order_item_data["product_id"]
        order_item_updateable = get_order_item_by_order_id_and_product_id(session, order_id, product_id)
        if order_item_updateable:
            order = get_order_by_id(session, order_id, current_user["user_id"])
            if current_user["role"] == "cliente" and order.user_id != current_user["user_id"]:
                raise HTTPException(status_code=403, detail=f"Order Item not permitted")
            order_item_data["order_id"] = order_id
            order_item_obj = OrderItem(**order_item_data)
            updated_order_item = update_order_item(session, order_item_obj)
            return updated_order_item
        else:
            raise HTTPException(status_code=404, detail=f"OrderItem with Order ID {order_id} and Product ID {product_id} not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{product_id}", response_model=OrderItem)
def delete(
    order_id: int,
    product_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "cliente"])),
):
    """
    Permite eliminar un Order Item.
    """
    try:
        order_item_to_delete = get_order_item_by_order_id_and_product_id(session, order_id, product_id)
        if order_item_to_delete:
            order = get_order_by_id(session, order_item_to_delete.order_id, current_user["user_id"])
            if current_user["role"] == "cliente" and order.user_id != current_user["user_id"]:
                raise HTTPException(status_code=403, detail=f"Order with ID {order_id} not permitted")
            deleted_order_item = delete_order_item_by_order_id_and_product_id(session, order_id, product_id)
            return deleted_order_item    
        else:
            raise HTTPException(status_code=404, detail=f"Order with ID {order_id} and Product ID {product_id} not found")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
