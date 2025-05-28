import os
from fastapi import FastAPI, Response
from fastapi.responses import FileResponse
import uvicorn
import pandas as pd
from io import BytesIO
from jinja2 import Template
from xhtml2pdf import pisa
from utils.api_client import fetch_characters  # Importar la función desde el archivo auxiliar
from pathlib import Path

app = FastAPI()

@app.get("/rick-and-morty")
async def get_characters():
    try:
        characters = await fetch_characters()
        return characters
    except Exception as e:
        return {"error": str(e)}

@app.get("/rick-and-morty/excel")
async def get_characters_excel():
    try:
        characters = await fetch_characters()
        # Generar el archivo Excel en memoria
        buffer = BytesIO()
        df = pd.DataFrame(characters)
        with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
            df.to_excel(writer, index=False, sheet_name="Personajes")
        buffer.seek(0)
        # Enviar el archivo Excel al cliente
        return Response(
            buffer.getvalue(),
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            headers={"Content-Disposition": "attachment; filename=rick_and_morty_characters_ranking.xlsx"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/rick-and-morty/csv")
async def get_characters_csv():
    try:
        characters = await fetch_characters()
        # Generar el archivo CSV en memoria
        buffer = BytesIO()
        df = pd.DataFrame(characters)
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        # Enviar el archivo CSV al cliente
        return Response(
            buffer.getvalue(),
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=rick_and_morty_characters_ranking.csv"}
        )
    except Exception as e:
        return {"error": str(e)}

@app.get("/rick-and-morty/pdf")
async def get_characters_pdf():
    try:
        characters = await fetch_characters()
        # Cargar la plantilla HTML desde el archivo externo
        template_path = Path("views/pdf_template.html")
        html_template = template_path.read_text(encoding="utf-8")
        template = Template(html_template)
        rendered_html = template.render(characters=characters)
        
        # Convertir el HTML a PDF con xhtml2pdf
        pdf_buffer = BytesIO()
        pisa_status = pisa.CreatePDF(rendered_html, dest=pdf_buffer)
        if pisa_status.err:
            return {"error": "Error al generar el PDF"}
        pdf_buffer.seek(0)
        
        # Enviar el archivo PDF al cliente
        return Response(
            pdf_buffer.getvalue(),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=rick_and_morty_characters_ranking.pdf"}
        )
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
