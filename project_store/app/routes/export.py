
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from sqlmodel import Session
from models.order import Order, OrderBase
from db.database import get_session
from auth.dependencies import require_role
from models.product import Product
from utils.api_dummy_products import fetch_products
from io import BytesIO
from jinja2 import Template
from xhtml2pdf import pisa
from pathlib import Path
import pandas as pd

router = APIRouter()

@router.get("/excel")
async def get_weather_excel(session: Session = Depends(get_session), 
                            current_user: dict = Depends(require_role(["admin", "cliente"]))):
    try:
        # Retrieve data
        # TODO
        data = None

        # Generate Excel file in memory
        buffer = BytesIO()
        df = pd.DataFrame(data)
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Weather")
        buffer.seek(0)
        # Send Excel file to client
        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=weather_data.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}

@router.get("/csv")
async def get_weather_csv(city: str):
    try:
        # Retrieve data
        # TODO
        data = None

        # Generate CSV file in memory
        buffer = BytesIO()
        df = pd.DataFrame(data)
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Send CSV file to client
        return Response(
            buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=weather_data.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@router.get("/pdf")
async def get_weather_pdf(request: Request, city: str):
    try:
        # Retrieve data
        # TODO
        data = None

        # Load HTML template from external file
        template_path = Path("views/pdf_template.html")
        html_template = template_path.read_text(encoding="utf-8")
        template = Template(html_template)
        rendered_html = template.render(data=data, city=city)
        
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
            headers={"Content-Disposition": "attachment; filename=weather_data.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}