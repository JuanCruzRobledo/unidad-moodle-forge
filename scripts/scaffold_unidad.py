# -*- coding: utf-8 -*-
"""
Crea la carpeta de una unidad nueva del aula virtual y crea/actualiza estado.yml
en la raiz de la materia.

Estructura creada por unidad (ver references/estructura-aula-real.md):
    Introduccion/
    Actividades/notebooklm/
    Practica/
    Microteaching/
    Autoevaluacion/
    EncuestaCierre/

Uso:
    python scaffold_unidad.py --materia "Programacion 3" --numero 1 \
        --nombre "Fundamentos Spring Boot" --actividades 4 \
        --carrera-variante prog3 --dest "E:/ruta/a/la/materia"

    # dest por defecto: carpeta actual
    # si estado.yml ya existe, se le agrega la unidad nueva sin tocar las demas
"""
import argparse
import os

import yaml

SUBCARPETAS = ["Introduccion", "Actividades", "Practica", "Microteaching",
               "Autoevaluacion", "EncuestaCierre"]

STATUS_PENDIENTE = "pendiente"


def slugify_carpeta(numero: int, nombre: str) -> str:
    return f"Unidad {numero} - {nombre}"


def crear_carpetas(materia_dir: str, carpeta_unidad: str) -> None:
    base = os.path.join(materia_dir, carpeta_unidad)
    for sub in SUBCARPETAS:
        os.makedirs(os.path.join(base, sub), exist_ok=True)
    os.makedirs(os.path.join(base, "Actividades", "notebooklm"), exist_ok=True)


def crear_carpetas_actividades(materia_dir: str, carpeta_unidad: str, cantidad: int) -> None:
    base = os.path.join(materia_dir, carpeta_unidad, "Actividades")
    for i in range(1, cantidad + 1):
        os.makedirs(os.path.join(base, f"actividad-{i}"), exist_ok=True)


def nueva_unidad_dict(numero: int, nombre: str, carpeta: str, cantidad_actividades: int) -> dict:
    return {
        "numero": numero,
        "nombre": nombre,
        "carpeta": carpeta,
        "introduccion": {"status": STATUS_PENDIENTE},
        "actividades": {
            "cantidad": cantidad_actividades,
            "items": [
                {
                    "numero": i,
                    "nombre": "",
                    "html_status": STATUS_PENDIENTE,
                    "preguntas_xml_status": STATUS_PENDIENTE,
                    "notebooklm": {"guion_status": STATUS_PENDIENTE, "link_pegado": False},
                }
                for i in range(1, cantidad_actividades + 1)
            ],
        },
        "practica": {
            "consigna_html_status": STATUS_PENDIENTE,
            "entrega_html_status": STATUS_PENDIENTE,
            "pdf_status": STATUS_PENDIENTE,
            "pdf_confirmado_por_usuario": False,
        },
        "microteaching": {"status": STATUS_PENDIENTE},
        "autoevaluacion": {
            "preguntas_esperadas": 10,
            "html_status": STATUS_PENDIENTE,
            "preguntas_xml_status": STATUS_PENDIENTE,
        },
        "encuesta_cierre": {"status": STATUS_PENDIENTE},
    }


def cargar_o_crear_estado(estado_path: str, materia: str, carrera_variante: str) -> dict:
    if os.path.exists(estado_path):
        with open(estado_path, encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    return {
        "materia": materia,
        "carrera_variante": carrera_variante,
        "prefijo_banco_preguntas": "",
        "unidades": [],
        "evaluaciones_curso": {
            "activa": False,
            "parciales": [],
            "recuperatorios": [],
        },
    }


def guardar_estado(estado_path: str, estado: dict) -> None:
    with open(estado_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(estado, f, allow_unicode=True, sort_keys=False)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--materia", required=True, help="Nombre de la materia")
    ap.add_argument("--numero", required=True, type=int, help="Numero de la unidad")
    ap.add_argument("--nombre", required=True, help="Nombre/tema de la unidad")
    ap.add_argument("--actividades", type=int, default=4, help="Cantidad de actividades a scaffoldear (default 4)")
    ap.add_argument("--carrera-variante", default="prog1", choices=["prog1", "prog2", "prog3"],
                     help="Variante de formato de entrega del TP a usar")
    ap.add_argument("--dest", default=".", help="Carpeta raiz de la materia (default: carpeta actual)")
    args = ap.parse_args()

    materia_dir = os.path.abspath(args.dest)
    os.makedirs(materia_dir, exist_ok=True)

    carpeta_unidad = slugify_carpeta(args.numero, args.nombre)
    crear_carpetas(materia_dir, carpeta_unidad)
    crear_carpetas_actividades(materia_dir, carpeta_unidad, args.actividades)

    estado_path = os.path.join(materia_dir, "estado.yml")
    estado = cargar_o_crear_estado(estado_path, args.materia, args.carrera_variante)

    ya_existe = any(u.get("numero") == args.numero for u in estado.get("unidades", []))
    if ya_existe:
        raise SystemExit(f"La unidad {args.numero} ya existe en estado.yml — no se modifico.")

    estado.setdefault("unidades", []).append(
        nueva_unidad_dict(args.numero, args.nombre, carpeta_unidad, args.actividades)
    )
    guardar_estado(estado_path, estado)

    print(f"Unidad creada: {os.path.join(materia_dir, carpeta_unidad)}")
    print(f"estado.yml actualizado: {estado_path}")


if __name__ == "__main__":
    main()
