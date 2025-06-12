
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.order import Order, OrderBase
from db.database import get_session
from auth.dependencies import require_role
from models.product import Product
from utils.api_dummy_products import fetch_products

router = APIRouter()

@router.get("/", response_model=list[Product], status_code=200)
async def find_all(q: str = None, 
             skip: int = None, 
             limit: int = None, 
             session: Session = Depends(get_session), 
             current_user: dict = Depends(require_role(["admin", "cliente"]))):
    """
    Find all Products.
    Filter options as queryParams:
        * q: Filter by query string.
        * skip: Number of rows to omit (pagination).
        * limit: Maximum number of rows to return (pagination).
    """
    try:
        products = await fetch_products(q, skip, limit)
        result = []
        for p in products:
            result.append(Product(
                id=p['id'],
                title=p['title'],
                description=p['description'],
                price=p['price']
            ))
        return result
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
