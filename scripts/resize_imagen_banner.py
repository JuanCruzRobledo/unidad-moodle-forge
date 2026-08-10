# -*- coding: utf-8 -*-
"""
Fuerza la imagen de banner de Introduccion (Fase 1) a 600x600 px exactos.

Los modelos de generacion de imagen (via el MCP nanobanana) no respetan de
forma confiable un aspect ratio pedido solo por texto en el prompt -- ver
references/imagen-banner-introduccion.md. Este script es el paso post-
generacion que garantiza el tamano final, sin depender de que el modelo lo
haga bien solo: recorta al cuadrado mas grande centrado (si la imagen no es
ya cuadrada) y despues redimensiona a 600x600 con remuestreo LANCZOS.

Uso:
    python resize_imagen_banner.py --entrada RUTA.png
        # sobrescribe el mismo archivo

    python resize_imagen_banner.py --entrada RUTA_ORIGINAL.png --salida RUTA_FINAL.png
        # deja el original intacto, escribe el resultado aparte
"""
import argparse

from PIL import Image

TAMANO = (600, 600)


def recortar_centrado_a_cuadrado(img: Image.Image) -> Image.Image:
    ancho, alto = img.size
    if ancho == alto:
        return img
    lado = min(ancho, alto)
    izquierda = (ancho - lado) // 2
    arriba = (alto - lado) // 2
    return img.crop((izquierda, arriba, izquierda + lado, arriba + lado))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--entrada", required=True, help="Ruta de la imagen generada por nanobanana")
    ap.add_argument("--salida", default=None, help="Ruta de salida (default: sobrescribe --entrada)")
    args = ap.parse_args()

    salida = args.salida or args.entrada

    with Image.open(args.entrada) as img:
        img = img.convert("RGB") if img.mode not in ("RGB", "RGBA") else img
        img = recortar_centrado_a_cuadrado(img)
        img = img.resize(TAMANO, Image.LANCZOS)
        img.save(salida, "PNG")

    print(f"OK: {salida} -> {TAMANO[0]}x{TAMANO[1]}px")


if __name__ == "__main__":
    main()
