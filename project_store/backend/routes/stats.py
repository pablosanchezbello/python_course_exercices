
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from db.database import get_session
from auth.dependencies import require_role
from crud.order import get_orders_by_users
from models.stat import AggregatedStat, RankedStat
from crud.order_item import products_ranking

router = APIRouter()

@router.get("/by-user", response_model=list[AggregatedStat], status_code=200)
async def find_by_user(session: Session = Depends(get_session), 
                          current_user: dict = Depends(require_role(["admin"]))):
    """
    Find aggregated stats by user.
    """
    try:
        result = get_orders_by_users(session)
        return result
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
    
@router.get("/product-rank", response_model=list[RankedStat], status_code=200)
async def find_by_user(session: Session = Depends(get_session), 
                          current_user: dict = Depends(require_role(["admin"]))):
    """
    Find TOP 10 product rank.
    """
    try:
        result = products_ranking(session)
        return result
    except HTTPException as e:
        raise e
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
