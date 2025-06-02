from pydantic import BaseModel
from sqlmodel import Field

class Product(BaseModel):
    id: int = Field(..., description="ID of the product")
    title: str = Field(..., description="Title of the product")
    description: str = Field(..., description="Description of the product")
    price: float = Field(..., description="Price of the product")
