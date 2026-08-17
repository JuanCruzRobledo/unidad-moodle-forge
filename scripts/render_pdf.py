# -*- coding: utf-8 -*-
"""
Convierte a PDF un documento HTML ya confirmado por el usuario, usando un
navegador headless (Playwright + Chromium) en vez de un motor tipo LaTeX: el
contenido de las plantillas usa estilos inline, flexbox, <details> e iframes, y un
render de navegador reproduce exactamente lo que se ve en pantalla.

Dos usos distintos, ver references/plantilla-pdf-practica.md:

1. Documento de Practica/TP con membrete institucional (el que se sube como
   recurso descargable en la pestana "Practica" de Moodle): pasa --materia y
   se le agrega automaticamente encabezado institucional ("TECNICATURA
   UNIVERSITARIA EN PROGRAMACION", opcionalmente con una imagen -- ver mas
   abajo) y pie de pagina (barra de color con el nombre de la materia + numero
   de pagina) en cada hoja, via header_template/footer_template de Playwright
   -- la unica forma de lograr un encabezado/pie que se repita en todas las
   paginas (el CSS de impresion normal de un navegador no soporta esto).
2. Conversion simple sin membrete (uso legacy / casos especiales): omiti
   --materia y se comporta como una conversion HTML -> PDF a secas.

Imagen del encabezado (logo institucional u otra): OPCIONAL, y por default el
encabezado va SIN imagen -- solo el texto "TECNICATURA UNIVERSITARIA EN
PROGRAMACION". Se puede configurar de dos formas, en este orden de prioridad:

    1. --logo <ruta>            (override puntual de esta corrida)
    2. PDF_HEADER_LOGO en .env  (default persistente para esta maquina,
                                  ver env.example / scripts/configurar.py)

Si ninguna de las dos esta presente, no se agrega ninguna imagen. El logo
institucional real (assets/logo-utn-tup.jpg) sigue disponible en el repo por
si se quiere volver a activar -- ya no es el default automatico.

NO llamar a este script antes de que el usuario haya confirmado explicitamente
que el documento esta bien (ver SKILL.md, Fase 3, y estado.yml ->
practica.pdf_confirmado_por_usuario).

Requiere:
    pip install playwright python-dotenv
    playwright install chromium

Uso:
    python render_pdf.py --entrada documento-practica.html --salida documento-practica.pdf \
        --materia "Metodologia I"

    # con imagen en el encabezado, puntual para esta corrida:
    python render_pdf.py --entrada documento-practica.html --salida documento-practica.pdf \
        --materia "Metodologia I" --logo assets/logo-utn-tup.jpg

    # sin membrete (legacy):
    python render_pdf.py --entrada consigna-tp.html --salida consigna-tp.pdf
"""
import argparse
import base64
import os
import sys

from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SKILL_DIR = os.path.dirname(SCRIPT_DIR)

load_dotenv(os.path.join(SKILL_DIR, ".env"))

HEADER_TEMPLATE_CON_LOGO = """
<div style="font-size:9px; width:100%; margin:0 28px; display:flex;
justify-content:space-between; align-items:flex-start;
font-family: Calibri, Arial, sans-serif; color:#1a1a1a;">
  <div style="font-weight:700; line-height:1.35; padding-top:8px; letter-spacing:0.3px;">
    TECNICATURA UNIVERSITARIA<br>EN PROGRAMACION
  </div>
  <img src="data:image/jpeg;base64,__LOGO_B64__" style="height:34px; margin-top:4px;">
</div>
"""

HEADER_TEMPLATE_SIN_LOGO = """
<div style="font-size:9px; width:100%; margin:0 28px;
font-family: Calibri, Arial, sans-serif; color:#1a1a1a;">
  <div style="font-weight:700; line-height:1.35; padding-top:8px; letter-spacing:0.3px;">
    TECNICATURA UNIVERSITARIA<br>EN PROGRAMACION
  </div>
</div>
"""

FOOTER_TEMPLATE = """
<div style="width:100%; font-family: Calibri, Arial, sans-serif;
-webkit-print-color-adjust: exact; print-color-adjust: exact;">
  <div style="text-align:right; font-size:8px; color:#333; margin:0 28px 2px 0;">
    <span class="pageNumber"></span>
  </div>
  <div style="background-color:#4F81BD; color:#ffffff; text-align:center;
  font-size:10px; padding:6px 0; width:100%;
  -webkit-print-color-adjust: exact; print-color-adjust: exact;">
    __MATERIA__
  </div>
</div>
"""


def _logo_base64(logo_path: str) -> str:
    with open(logo_path, "rb") as f:
        return base64.b64encode(f.read()).decode("ascii")


def render(entrada_html: str, salida_pdf: str, materia, logo_path: str) -> None:
    ruta_absoluta = os.path.abspath(entrada_html)
    if not os.path.exists(ruta_absoluta):
        sys.exit(f"No existe el archivo: {ruta_absoluta}")

    con_membrete = bool(materia)
    pdf_kwargs = dict(
        path=salida_pdf,
        format="A4",
        print_background=True,
    )

    if con_membrete:
        if logo_path:
            if not os.path.exists(logo_path):
                sys.exit(f"No existe el logo configurado: {logo_path}")
            header = HEADER_TEMPLATE_CON_LOGO.replace("__LOGO_B64__", _logo_base64(logo_path))
        else:
            header = HEADER_TEMPLATE_SIN_LOGO
        footer = FOOTER_TEMPLATE.replace("__MATERIA__", materia)
        pdf_kwargs.update(
            display_header_footer=True,
            header_template=header,
            footer_template=footer,
            margin={"top": "100px", "bottom": "80px", "left": "56px", "right": "56px"},
        )
    else:
        pdf_kwargs["margin"] = {"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"}

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{ruta_absoluta}")
        page.pdf(**pdf_kwargs)
        browser.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", required=True, help="HTML confirmado a convertir")
    ap.add_argument("--salida", required=True, help="Ruta del PDF de salida")
    ap.add_argument("--materia", default=None,
                     help="Nombre de la materia para el membrete (header/footer institucional). "
                          "Si se omite, convierte sin membrete (modo legacy).")
    ap.add_argument("--logo", default=None,
                     help="Ruta a una imagen para el encabezado (opcional, override puntual de "
                          "esta corrida). Si se omite, se usa PDF_HEADER_LOGO de .env; si tampoco "
                          "está configurado, el encabezado va sin imagen (default).")
    args = ap.parse_args()

    logo_path = args.logo or os.environ.get("PDF_HEADER_LOGO") or None
    render(args.entrada, args.salida, args.materia, logo_path)
    print(f"PDF generado: {os.path.abspath(args.salida)}")


if __name__ == "__main__":
    main()
