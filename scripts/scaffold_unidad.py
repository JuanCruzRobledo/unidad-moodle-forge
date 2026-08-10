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

Componentes opcionales (ver Fase 0 de SKILL.md -- el agente pregunta esto por
AskUserQuestion SOLO para una unidad nueva, nunca al retomar una existente):
    --con-actividad-ludica / --sin-actividad-ludica
    --con-microteaching / --sin-microteaching
    --con-material-apoyo / --sin-material-apoyo
    --con-videos-actividad / --sin-videos-actividad
    --con-autoevaluacion / --sin-autoevaluacion
    --con-encuesta-cierre / --sin-encuesta-cierre
    Todos default --con-* (True): usar el script sin estos flags se comporta
    exactamente igual que antes de que existieran.
"""
import argparse
import os

import yaml

SUBCARPETAS = ["Introduccion", "Actividades", "Practica", "Microteaching",
               "Autoevaluacion", "EncuestaCierre"]

STATUS_PENDIENTE = "pendiente"

# Componentes opcionales de una unidad -- ver Fase 0 de SKILL.md: para una unidad
# NUEVA (no al retomar una existente) el agente le pregunta al usuario via
# AskUserQuestion cuales de estos incluir, y pasa la respuesta como estos flags.
# Todos parten en True por retrocompatibilidad (una unidad vieja sin este bloque
# se comporta igual que antes).
COMPONENTES_OPCIONALES = [
    "actividad_ludica",
    "microteaching",
    "material_apoyo",
    "videos_actividad",
    "autoevaluacion",
    "encuesta_cierre",
]


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


def nueva_unidad_dict(numero: int, nombre: str, carpeta: str, cantidad_actividades: int,
                       incluir: dict) -> dict:
    return {
        "numero": numero,
        "nombre": nombre,
        "carpeta": carpeta,
        "incluir": dict(incluir),
        "introduccion": {
            "status": STATUS_PENDIENTE,
            # Imagen de URL_DE_LA_IMAGEN en 00-descripcion-seccion.html, generada con
            # el MCP gemini-nanobanana-mcp -- ver references/imagen-banner-introduccion.md.
            # Se genera junto con el resto de la Fase 1, no depende de la cadena de
            # dependencias de Actividades.
            "imagen_banner": {
                "status": STATUS_PENDIENTE,
                "ruta": "",
                "subida_por_usuario": False,
            },
            # Se genera al CIERRE del flujo de unidad (despues de Actividades/
            # Practica/Autoevaluacion), no en la Fase 1 -- ver SKILL.md.
            "video_guion_status": STATUS_PENDIENTE,
        },
        "actividades": {
            "cantidad": cantidad_actividades,
            "items": [
                {
                    "numero": i,
                    "nombre": "",
                    "html_status": STATUS_PENDIENTE,
                    "preguntas_xml_status": STATUS_PENDIENTE,
                    "material_apoyo": {"prompts": []},
                    "lectura_pdf": {
                        "documento_html_status": STATUS_PENDIENTE,
                        "pdf_status": STATUS_PENDIENTE,
                        "pdf_confirmado_por_usuario": False,
                    },
                    "videos": [
                        {
                            "numero": k,
                            "guion_status": STATUS_PENDIENTE,
                            "render_status": STATUS_PENDIENTE,
                            "url_subida": False,
                        }
                        for k in range(1, 4)
                    ],
                    "notebooklm": {"guion_status": STATUS_PENDIENTE, "link_pegado": False},
                }
                for i in range(1, cantidad_actividades + 1)
            ],
        },
        "practica": {
            "consigna_html_status": STATUS_PENDIENTE,
            "entrega_html_status": STATUS_PENDIENTE,
            "documento_html_status": STATUS_PENDIENTE,
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
        "importacion": {
            "status": STATUS_PENDIENTE,
            "curso_url": "",
            "seccion_raiz": None,
            "fecha_inicio": "",
            "fecha_ultima_corrida": "",
            "reporte": "",
            "subsecciones": {
                "introduccion": STATUS_PENDIENTE,
                "actividades": {
                    "status": STATUS_PENDIENTE,
                    "items": [
                        {"numero": i, "importado": STATUS_PENDIENTE}
                        for i in range(1, cantidad_actividades + 1)
                    ],
                },
                "practica": STATUS_PENDIENTE,
                "microteaching": STATUS_PENDIENTE,
                "autoevaluacion": STATUS_PENDIENTE,
                "encuesta_cierre": STATUS_PENDIENTE,
            },
        },
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

    # Componentes opcionales -- ver Fase 0 de SKILL.md. Todos default True: si el
    # agente no pregunta nada (unidad vieja, uso sin AskUserQuestion), el
    # comportamiento es identico al de antes de este flag.
    for comp in COMPONENTES_OPCIONALES:
        flag = comp.replace("_", "-")
        ap.add_argument(f"--con-{flag}", dest=comp, action="store_true", default=True)
        ap.add_argument(f"--sin-{flag}", dest=comp, action="store_false")

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

    incluir = {comp: getattr(args, comp) for comp in COMPONENTES_OPCIONALES}
    estado.setdefault("unidades", []).append(
        nueva_unidad_dict(args.numero, args.nombre, carpeta_unidad, args.actividades, incluir)
    )
    guardar_estado(estado_path, estado)

    print(f"Unidad creada: {os.path.join(materia_dir, carpeta_unidad)}")
    print(f"estado.yml actualizado: {estado_path}")


if __name__ == "__main__":
    main()
