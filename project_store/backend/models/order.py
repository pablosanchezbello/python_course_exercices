from datetime import datetime, timezone
from sqlmodel import Relationship, SQLModel, Field
from typing import TYPE_CHECKING, Optional
from models.order_item import OrderItemResponse

# Importación condicional para evitar errores de importación circular en tiempo de ejecución.
# TYPE_CHECKING es True solo durante el análisis estático (ej. mypy o IDEs),
# por lo tanto, estas importaciones no se ejecutan en tiempo real.
if TYPE_CHECKING:
    from models.order_item import OrderItem

class OrderBase(SQLModel):
    status: str = Field(default="in progress", description="Order status (in progress, paid, delivered, cancelled)")
    user_id: int = Field(foreign_key="user.id", description="Reference to the user who placed the order")


class Order(OrderBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the order was created"
    )
    items: list["OrderItem"] = Relationship(back_populates="order")  # Relación con Villain

class OrderResponse(OrderBase):
    id: int
    created_at: datetime
    items: list["OrderItemResponse"]

# model_rebuild() es necesario cuando se usan referencias de tipo como string (ej. "OrderItemResponse")
# para que Pydantic pueda resolverlas correctamente al generar esquemas (OpenAPI, validación, etc.)
OrderResponse.model_rebuild()