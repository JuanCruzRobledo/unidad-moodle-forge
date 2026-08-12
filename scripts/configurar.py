# -*- coding: utf-8 -*-
"""
Configura esta skill para la maquina donde se instalo -- se corre UNA vez por
maquina, no por proyecto ni por unidad. Crea ".env" a partir de "env.example"
si todavia no existe, y pide de forma interactiva los datos de Gamma (API key
via getpass, nunca en texto plano ni por linea de comandos).

IMPORTANTE -- por que esto se corre en una terminal propia, no delegado al
agente: hay una politica global que le bloquea a Claude Code leer o editar
cualquier archivo ".env"/".env.*", asi que aunque se lo pidas no va a poder
tocarlo por vos. Esta separacion es a proposito: la API key nunca deberia
aparecer en una conversacion con el agente. Corre este script vos mismo:

    cd unidad-moodle-forge
    python scripts/configurar.py

Si se corre sin terminal interactiva (ej. lanzado por una herramienta), usa
--skip-key para saltear el paso de la API key y dejar instrucciones para
completarla a mano despues.
"""
import argparse
import os
import shutil
import sys
from getpass import getpass
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = SKILL_ROOT / ".env"
ENV_EXAMPLE_PATH = SKILL_ROOT / "env.example"


def asegurar_env() -> None:
    """Crea .env desde env.example si todavia no existe. No pisa uno existente."""
    if ENV_PATH.exists():
        return
    if not ENV_EXAMPLE_PATH.exists():
        sys.exit(f"No encontre {ENV_EXAMPLE_PATH} -- el repo de la skill esta incompleto.")
    shutil.copyfile(ENV_EXAMPLE_PATH, ENV_PATH)
    print(f"Cree {ENV_PATH} a partir de env.example.")


def leer_env() -> list[str]:
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        return f.readlines()


def escribir_valor(lineas: list[str], clave: str, valor: str) -> list[str]:
    """Reemplaza la linea 'CLAVE=...' si existe, o la agrega al final."""
    prefijo = f"{clave}="
    nuevas = []
    encontrada = False
    for linea in lineas:
        if linea.strip().startswith(prefijo):
            nuevas.append(f"{prefijo}{valor}\n")
            encontrada = True
        else:
            nuevas.append(linea)
    if not encontrada:
        nuevas.append(f"{prefijo}{valor}\n")
    return nuevas


def configurar_gamma(saltear_key: bool) -> None:
    lineas = leer_env()

    if saltear_key:
        print(
            "\n--skip-key: no toco GAMMA_API_KEY. Completala a mano en .env "
            "cuando quieras activar la automatizacion de Material de apoyo."
        )
        return

    print("\n--- Material de apoyo (Gamma) ---")
    respuesta = input(
        "¿Tenes cuenta paga de Gamma y queres automatizar la generacion del "
        "Material de apoyo? (y/N): "
    ).strip().lower()
    if respuesta != "y":
        print("Ok, queda en modo manual (GAMMA_AUTOMATIZADO=false) -- la skill te va a "
              "seguir entregando el prompt de texto para pegar en Gamma a mano.")
        return

    api_key = getpass("Pegá tu GAMMA_API_KEY (no se muestra en pantalla): ").strip()
    if not api_key:
        print("No ingresaste ninguna key -- dejo GAMMA_AUTOMATIZADO=false.")
        return

    theme_id = input(
        "Tema de Gamma a usar (opcional, Enter para dejar el default de tu "
        "workspace de gamma.app): "
    ).strip()

    lineas = escribir_valor(lineas, "GAMMA_API_KEY", api_key)
    lineas = escribir_valor(lineas, "GAMMA_AUTOMATIZADO", "true")
    lineas = escribir_valor(lineas, "GAMMA_THEME_ID", theme_id)

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lineas)

    print("Listo -- GAMMA_AUTOMATIZADO=true, key guardada en .env (no se versiona, "
          "no se le mostro al agente).")


def configurar_youtube(saltear_key: bool) -> None:
    lineas = leer_env()

    if saltear_key:
        print(
            "\n--skip-key: no toco YOUTUBE_AUTOMATIZADO. Completalo a mano en .env "
            "cuando quieras activar la subida automatizada de videos."
        )
        return

    print("\n--- Subida de videos (YouTube Data API v3) ---")
    print(
        "Este paso NO lo resuelve este script -- requiere que ya hayas creado un "
        "proyecto en Google Cloud Console, habilitado la YouTube Data API v3, "
        "configurado la pantalla de consentimiento OAuth y descargado un "
        "client_secret.json de un cliente tipo 'App de escritorio'. Ver el paso a "
        "paso completo en references/automatizacion-subida-youtube.md."
    )
    respuesta = input(
        "¿Ya tenés ese client_secret.json guardado como "
        "scripts/.youtube_client_secret.json y querés activar la subida "
        "automatizada? (y/N): "
    ).strip().lower()
    if respuesta != "y":
        print("Ok, queda en modo manual (YOUTUBE_AUTOMATIZADO=false) -- vos seguís "
              "subiendo los videos a mano y devolviendo la URL real.")
        return

    client_secret_path = SKILL_ROOT / "scripts" / ".youtube_client_secret.json"
    if not client_secret_path.exists():
        print(
            f"No encontré {client_secret_path} -- guardalo ahí primero (ver "
            "references/automatizacion-subida-youtube.md, paso 6-7) y volvé a "
            "correr este script."
        )
        return

    lineas = escribir_valor(lineas, "YOUTUBE_AUTOMATIZADO", "true")

    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(lineas)

    print(
        "Listo -- YOUTUBE_AUTOMATIZADO=true. La primera subida real va a abrir tu "
        "navegador para autorizar una sola vez (queda cacheado en "
        "scripts/.youtube_token.json)."
    )


def mostrar_resumen() -> None:
    print("\n--- Estado final de .env ---")
    for linea in leer_env():
        limpia = linea.strip()
        if not limpia or limpia.startswith("#"):
            continue
        if limpia.startswith("GAMMA_API_KEY="):
            valor = limpia.split("=", 1)[1]
            print(f"GAMMA_API_KEY={'(configurada)' if valor else '(vacia)'}")
        else:
            print(limpia)
    print(
        "\nImagenes de infografia y NotebookLM siguen en manual/false -- todavia "
        "no tienen automatizacion implementada en la skill. Este script no los toca."
    )


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--skip-key", action="store_true",
                     help="No pedir la API key de Gamma (para corridas no interactivas)")
    args = ap.parse_args()

    asegurar_env()
    configurar_gamma(saltear_key=args.skip_key)
    configurar_youtube(saltear_key=args.skip_key)
    mostrar_resumen()


if __name__ == "__main__":
    main()
