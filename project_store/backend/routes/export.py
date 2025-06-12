
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session
from models.order import Order, OrderBase, OrderResponse
from db.database import get_session
from auth.dependencies import require_role
from models.product import Product
from utils.api_dummy_products import fetch_products
from io import BytesIO
from jinja2 import Template
from xhtml2pdf import pisa
from pathlib import Path
import pandas as pd
from routes.order import find_all

router = APIRouter()

@router.get("/excel")
async def get_excel(session: Session = Depends(get_session), 
                    current_user: dict = Depends(require_role(["admin", "cliente"]))):
    try:
        # Retrieve data
        data = await find_all(session=session, current_user=current_user)
        row_data = _convert_to_row_data(data)

        # Generate Excel file in memory
        buffer = BytesIO()
        df = pd.DataFrame(row_data)
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Orders")
        buffer.seek(0)
        # Send Excel file to client
        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=orders_data.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}

@router.get("/csv")
async def get_csv(session: Session = Depends(get_session), 
                  current_user: dict = Depends(require_role(["admin", "cliente"]))):
    try:
        # Retrieve data
        data = await find_all(session=session, current_user=current_user)
        row_data = _convert_to_row_data(data)

        # Generate CSV file in memory
        buffer = BytesIO()
        df = pd.DataFrame(row_data)
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Send CSV file to client
        return Response(
            buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=orders_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@router.get("/pdf")
async def get_pdf(session: Session = Depends(get_session), 
                  current_user: dict = Depends(require_role(["admin", "cliente"]))):
    try:
        # Retrieve data
        data = await find_all(session=session, current_user=current_user)
        row_data = _convert_to_row_data_for_pdf(data)

        # Load HTML template from external file
        template_path = Path("views/pdf_template.html")
        html_template = template_path.read_text(encoding="utf-8")
        template = Template(html_template)
        rendered_html = template.render(order_data=row_data)
        
        # Convert HTML to PDF with xhtml2pdf
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_buffer)
        if pisa_status.err:
            return {"error": "Error al generar el PDF"}
        pdf_buffer.seek(0)
        
        # Send PDF file to the client
        return Response(
            pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=orders_data.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}
    
def _convert_to_row_data(orders: list[OrderResponse]):
    result = []
    for order in orders:
        for item in order.items:
            result.append({
                "order_id": order.id,
                "product_id": item.product.id,
                "title": item.product.title,
                "quantity": item.quantity,
                "price": item.product.price
            })
    return result

def _convert_to_row_data_for_pdf(orders: list[OrderResponse]):
    result = []
    for order in orders:
        result_items = []
        for item in order.items:
            result_items.append({
                "id": item.product.id,
                "title": item.product.title,
                "quantity": item.quantity,
                "price": item.product.price
            })
        result.append({
            "order_id": order.id,
            "products": result_items
        })
    return result