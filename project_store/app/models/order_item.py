from typing import TYPE_CHECKING, Optional
from pydantic import BaseModel
from sqlmodel import Relationship, SQLModel, Field
from models.product import Product

# Importación condicional para evitar errores de importación circular en tiempo de ejecución.
# TYPE_CHECKING es True solo durante el análisis estático (ej. mypy o IDEs),
# por lo tanto, estas importaciones no se ejecutan en tiempo real.
if TYPE_CHECKING:
    from models.order import Order


class OrderItem(SQLModel, table=True):
    order_id: int = Field(foreign_key="order.id", primary_key=True, description="ID of the associated order")
    product_id: int = Field(primary_key=True, description="ID of the product from the external DummyJSON API")
    quantity: int = Field(..., gt=0, description="Quantity of the product ordered")
    order: Optional["Order"] = Relationship(back_populates="items")

class OrderItemResponse(BaseModel):
    product: Product
    quantity: int

# model_rebuild() es necesario cuando se usan referencias de tipo como string (ej. "OrderItemResponse")
# para que Pydantic pueda resolverlas correctamente al generar esquemas (OpenAPI, validación, etc.)
OrderItemResponse.model_rebuild()