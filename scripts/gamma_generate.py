# -*- coding: utf-8 -*-
"""
Genera "Material de apoyo" con la API de Gamma a partir del bloque "PROMPT
LISTO PARA GAMMA" que ya escribe esta skill en cada Actividades/actividad-N/
material-apoyo/prompt-gamma-N-K.md. Ver references/prompt-gamma-material-apoyo.md
seccion "Generacion automatizada opcional (API de Gamma)" para el flujo
completo -- este script es opcional, el entregable por default de la skill
sigue siendo el texto del prompt para pegar a mano en Gamma.

Usa POST /v1.0/generations (NO /v1.0/generations/from-template): ese segundo
endpoint solo funciona bien con plantillas de UNA sola pagina (la doc oficial
de Gamma lo dice explicito), asi que con una plantilla real de varias paginas
termina generando documentos cortos, sin portada real, y puede arrastrar
contenido viejo de la plantilla que no se puede corregir por prompt. Este
endpoint no admite un "gammaId" de plantilla -- controla el estilo visual con
"themeId" (opcional) y la extension con numCards/textOptions.

Requiere:
    pip install requests
    Variable de entorno GAMMA_API_KEY seteada -- NUNCA hardcodeada en este
    archivo ni pasada por linea de comandos en texto plano.
    Una cuenta Gamma paga (Pro/Ultra/Team/Business) -- el plan free no tiene
    acceso a la API.

Uso:
    python gamma_generate.py \
        --prompt-file "Actividades/actividad-2/material-apoyo/prompt-gamma-2-1.md" \
        --titulo "Material de apoyo - Actividad 2" \
        --salida "Actividades/actividad-2/material-apoyo/material-apoyo-2-1.pdf"

Calibra --num-cards / --text-amount al volumen real del contenido fuente (ver
la referencia de la skill): ~10/detailed para material nucleo bien
desarrollado, ~5-6/medium para material acotado u opcional. No hay un default
de --theme-id a proposito -- si se omite, Gamma usa el tema default del
workspace del usuario; pasalo solo si el usuario te dio un tema puntual (por
ejemplo, obtenido con GET /v1.0/gammas/{gammaId} sobre una plantilla propia).
"""
import argparse
import os
import re
import sys
import time

import requests

API_BASE = "https://public-api.gamma.app"
GENERATE_ENDPOINT = f"{API_BASE}/v1.0/generations"
STATUS_ENDPOINT = f"{API_BASE}/v1.0/generations/{{generation_id}}"

PROMPT_HEADER_RE = re.compile(
    r"##[^\n]*PROMPT LISTO PARA GAMMA[^\n]*\n(.*?)\n---",
    re.DOTALL,
)


def extraer_prompt(prompt_md_path: str) -> str:
    """Extrae SOLO el bloque copiable del .md -- nunca la seccion de trazabilidad interna."""
    with open(prompt_md_path, "r", encoding="utf-8") as f:
        contenido = f.read()

    match = PROMPT_HEADER_RE.search(contenido)
    if not match:
        sys.exit(
            "No encontre el bloque '## PROMPT LISTO PARA GAMMA ... ---' en "
            f"{prompt_md_path}. Revisa que el archivo siga el formato de "
            "references/prompt-gamma-material-apoyo.md."
        )
    texto = match.group(1).strip()
    # El bloque puede empezar con una nota "> ..." de trazabilidad de sesion -- no va a Gamma.
    lineas = [l for l in texto.split("\n") if not l.strip().startswith(">")]
    return "\n".join(lineas).strip()


def crear_generacion(input_text: str, api_key: str, titulo=None, num_cards=10,
                      text_amount="detailed", theme_id=None,
                      audience=None, export_as="pdf") -> str:
    body = {
        "inputText": input_text,
        "textMode": "generate",
        "format": "document",
        "numCards": num_cards,
        "cardSplit": "auto",
        "textOptions": {
            "amount": text_amount,
            "tone": "técnico pero accesible, con ejemplos concretos",
            "language": "es",
        },
        "imageOptions": {"source": "themeAccent"},
        "exportAs": export_as,
    }
    if titulo:
        body["title"] = titulo
    if theme_id:
        body["themeId"] = theme_id
    if audience:
        body["textOptions"]["audience"] = audience

    resp = requests.post(
        GENERATE_ENDPOINT,
        headers={"Content-Type": "application/json", "X-API-KEY": api_key},
        json=body,
        timeout=30,
    )
    if resp.status_code >= 400:
        sys.exit(f"Error creando la generacion ({resp.status_code}): {resp.text}")

    data = resp.json()
    if data.get("warnings"):
        print(f"Advertencia de Gamma: {data['warnings']}")
    return data["generationId"]


def esperar_generacion(generation_id: str, api_key: str, intervalo=5, timeout=300) -> dict:
    transcurrido = 0
    while transcurrido < timeout:
        resp = requests.get(
            STATUS_ENDPOINT.format(generation_id=generation_id),
            headers={"X-API-KEY": api_key},
            timeout=30,
        )
        if resp.status_code >= 400:
            sys.exit(f"Error consultando la generacion ({resp.status_code}): {resp.text}")

        data = resp.json()
        status = data.get("status")
        if status == "completed":
            return data
        if status == "failed":
            error = data.get("error", {})
            sys.exit(f"La generacion fallo: {error.get('message', 'sin detalle')}")

        print(f"  ... generando ({status}), esperando {intervalo}s")
        time.sleep(intervalo)
        transcurrido += intervalo

    sys.exit(f"Timeout de {timeout}s esperando la generacion {generation_id}")


def descargar_export(export_url: str, salida_path: str) -> None:
    resp = requests.get(export_url, timeout=60)
    resp.raise_for_status()
    os.makedirs(os.path.dirname(os.path.abspath(salida_path)) or ".", exist_ok=True)
    with open(salida_path, "wb") as f:
        f.write(resp.content)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt-file", required=True,
                     help="Ruta al prompt-gamma-N-K.md ya generado por la skill")
    ap.add_argument("--titulo", default=None, help="Titulo del documento generado (opcional)")
    ap.add_argument("--num-cards", type=int, default=10, help="Cantidad objetivo de tarjetas/paginas (default: 10; bajar para material acotado)")
    ap.add_argument("--text-amount", default="detailed", choices=["brief", "medium", "detailed", "extensive"],
                     help="Densidad de texto por tarjeta (default: detailed)")
    ap.add_argument("--theme-id", default=None,
                     help="Tema de Gamma a aplicar (opcional). Si se omite, Gamma usa el tema default del workspace del usuario.")
    ap.add_argument("--audience", default="estudiantes de la Tecnicatura Universitaria en Programación (TUP, UTN)",
                     help="Audiencia objetivo para textOptions.audience")
    ap.add_argument("--export-as", default="pdf", choices=["pdf", "pptx", "png"])
    ap.add_argument("--salida", required=True, help="Ruta donde guardar el archivo exportado")
    ap.add_argument("--intervalo", type=int, default=5, help="Segundos entre polls de estado (default: 5)")
    ap.add_argument("--timeout", type=int, default=300, help="Timeout total en segundos (default: 300)")
    args = ap.parse_args()

    api_key = os.environ.get("GAMMA_API_KEY")
    if not api_key:
        sys.exit(
            "No encontre la variable de entorno GAMMA_API_KEY. Seteala primero "
            "(ver references/prompt-gamma-material-apoyo.md seccion 'Generación "
            "automatizada opcional') y abri una terminal nueva para que la tome."
        )

    input_text = extraer_prompt(args.prompt_file)
    print(f"Prompt extraido ({len(input_text)} caracteres) de {args.prompt_file}")

    generation_id = crear_generacion(
        input_text, api_key, titulo=args.titulo, num_cards=args.num_cards,
        text_amount=args.text_amount, theme_id=args.theme_id,
        audience=args.audience, export_as=args.export_as,
    )
    print(f"Generacion creada: {generation_id}")

    resultado = esperar_generacion(generation_id, api_key, args.intervalo, args.timeout)

    creditos = resultado.get("credits", {})
    print(f"Generacion completa. Gamma: {resultado.get('gammaUrl')}")
    print(f"Creditos usados: {creditos.get('deducted')} (quedan: {creditos.get('remaining')})")

    export_url = resultado.get("exportUrl")
    if export_url:
        descargar_export(export_url, args.salida)
        print(f"Archivo descargado: {os.path.abspath(args.salida)}")
    else:
        print("Gamma no devolvio exportUrl -- revisa gammaUrl y descargalo a mano.")


if __name__ == "__main__":
    main()
