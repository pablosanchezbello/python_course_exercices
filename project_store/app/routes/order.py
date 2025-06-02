
from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlmodel import Session
from models.order import Order, OrderBase, OrderResponse
from db.database import get_session
from crud.order import create_order, delete_order, get_order_by_id, get_orders_filtered, update_order
from auth.dependencies import require_role
from models.order_item import OrderItemResponse
from models.product import Product
from utils.api_dummy_products import fetch_product_by_id

router = APIRouter()

@router.post("/", response_model=Order, status_code=201)
def create(order: OrderBase, 
           session: Session = Depends(get_session), 
           current_user: dict = Depends(require_role(["admin", "cliente"]))):
    """
    Create a new order without products associated to it.
    """
    try:
        order_data = Order(**order.model_dump())
        order_data.user_id = current_user["user_id"]
        return create_order(session, order_data)
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.get("/", response_model=list[OrderResponse], status_code=200)
async def find_all(id: int = None, 
             skip: int = None, 
             limit: int = None, 
             session: Session = Depends(get_session), 
             current_user: dict = Depends(require_role(["admin", "cliente"]))):
    """
    Find all Orders in the system.
    Filter options as queryParams:
        * id: Filter by the ID in the list.
        * user_id: Filter by the Owner ID.
        * skip: Number of rows to omit (pagination).
        * limit: Maximum number of rows to return (pagination).
    """
    try:
        orders: List[Order] = []
        if current_user["role"] == "admin" :
            orders = get_orders_filtered(session, id=id, user_id=None, skip=skip, limit=limit)
        else :
            orders = get_orders_filtered(session, id=id, user_id=current_user["user_id"], skip=skip, limit=limit)
        result_orders = []
        for order in orders:
            items_result = []
            if order.items != None:
                for item in order.items:
                    product = await fetch_product_by_id(item.product_id)
                    items_result.append(OrderItemResponse(
                        product=product,
                        quantity=item.quantity
                    ))
            result_orders.append(OrderResponse(
                status=order.status,
                user_id=order.user_id,
                id= order.id,
                created_at=order.created_at,
                items=items_result
            ))
        return result_orders
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")


@router.get("/{order_id}", response_model=OrderResponse)
async def update(
    order_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "cliente"])),
):
    try:
        order = None
        if current_user["role"] == "admin" :
            order = get_order_by_id(session, order_id, None)
        else:
            order = get_order_by_id(session, order_id, current_user["user_id"])
        if order is None:
            raise HTTPException(status_code=400, detail=f"Order with ID {order_id} was not found.")
        result_items = []
        if (order.items != None):
            for item in order.items:
                product = await fetch_product_by_id(item.product_id)
                result_items.append(OrderItemResponse(
                    product=Product(
                        id=product['id'],
                        title=product['title'],
                        description=product['description'],
                        price=product['price']
                    ),
                    quantity=item.quantity
                ))
        return OrderResponse(
            status=order.status,
            user_id=order.user_id,
            id=order.id,
            created_at=order.created_at,
            items=result_items
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.put("/{order_id}", response_model=Order)
def update(
    order_id: int,
    order_data: OrderBase = Body(
        ...,
        examples={
            "status": "Order status (in progress, paid, delivered, cancelled)"
        }
    ),
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "cliente"])),
):
    """
    Update an existing order.
    """
    try:
        if current_user["role"] == "admin" :
            return update_order(session, order_id, order_data.model_dump())
        else:
            return update_order(session, order_id, order_data.model_dump(), current_user["user_id"])
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@router.delete("/{order_id}", response_model=Order)
def delete(
    order_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(require_role(["admin", "cliente"])),
):
    try:
        if current_user["role"] == "admin" :
            return delete_order(session, order_id, None)
        else:
            return delete_order(session, order_id, current_user["user_id"])
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
