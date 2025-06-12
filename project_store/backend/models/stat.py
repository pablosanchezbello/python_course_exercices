from pydantic import BaseModel
from sqlmodel import Field

class AggregatedStat(BaseModel):
    user_id: int = Field(..., description="ID of the user")
    order_count: int = Field(..., description="Number of orders")

class RankedStat(BaseModel):
    product_id: int = Field(..., description="ID of the product")
    total_quantity: int = Field(..., description="Total quantity")
    rank: int = Field(..., description="Rank based on the number of orders")