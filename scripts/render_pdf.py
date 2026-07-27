# -*- coding: utf-8 -*-
"""
Convierte un archivo HTML ya confirmado por el usuario a PDF fiel, usando un
navegador headless (Playwright + Chromium) en vez de un motor tipo LaTeX: el
contenido de las plantillas usa estilos inline, flexbox, <details> e iframes, y un
render de navegador reproduce exactamente lo que se ve en Moodle.

NO llamar a este script antes de que el usuario haya confirmado explicitamente que
el HTML esta bien (ver SKILL.md, Fase 3, y estado.yml -> practica.pdf_confirmado_por_usuario).

Requiere:
    pip install playwright
    playwright install chromium

Uso:
    python render_pdf.py --entrada consigna-tp.html --salida consigna-tp.pdf
"""
import argparse
import os
import sys

from playwright.sync_api import sync_playwright


def render(entrada_html: str, salida_pdf: str) -> None:
    ruta_absoluta = os.path.abspath(entrada_html)
    if not os.path.exists(ruta_absoluta):
        sys.exit(f"No existe el archivo: {ruta_absoluta}")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file:///{ruta_absoluta}")
        page.pdf(
            path=salida_pdf,
            format="A4",
            print_background=True,
            margin={"top": "20px", "bottom": "20px", "left": "20px", "right": "20px"},
        )
        browser.close()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", required=True, help="HTML confirmado a convertir")
    ap.add_argument("--salida", required=True, help="Ruta del PDF de salida")
    args = ap.parse_args()

    render(args.entrada, args.salida)
    print(f"PDF generado: {os.path.abspath(args.salida)}")


if __name__ == "__main__":
    main()
