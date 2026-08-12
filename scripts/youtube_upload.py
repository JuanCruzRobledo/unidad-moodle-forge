# -*- coding: utf-8 -*-
"""
Sube un video a YouTube via la YouTube Data API v3 (videos.insert), a partir
de un .mp4 ya renderizado (por ejemplo, con la skill hyperframes).

Requiere:
    pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
    Un client_secret.json descargado de Google Cloud Console (credencial OAuth
    tipo "Desktop app") -- ver references/automatizacion-subida-youtube.md
    para el paso a paso completo del setup (proyecto, API habilitada, pantalla
    de consentimiento, scope, cliente OAuth).

Primera corrida (una vez por maquina, o cada vez que se amplia el scope): abre
el navegador para que el usuario autorice con su cuenta de YouTube, y guarda
el refresh token en scripts/.youtube_token.json (nunca en el chat, nunca
versionado). Corridas siguientes reusan ese token sin volver a pedir nada,
salvo que se revoque.

Uso:
    python youtube_upload.py \
        --video-file "Actividades/actividad-1/videos/video-actividad-1-1.mp4" \
        --title "Qué es Prompt Engineering: diseñar en vez de preguntar" \
        --description "Material de catedra, [materia] - TUP, UTN." \
        --privacy-status unlisted \
        --playlist-id PLxxxxxxxxxxxx

Regla dura de titulo (ver references/automatizacion-subida-youtube.md): el
titulo real en YouTube es SOLO el tema, sin el prefijo "Video N -" ni el
nombre de la materia -- eso queda en el texto del link del HTML, no en el
titulo del video.

Regla dura de playlist: --playlist-id es siempre una decision del usuario,
nunca un default hardcodeado por este script ni por la skill. Preguntale
antes de la primera subida de una tanda si quiere organizar en una playlist.
"""
import argparse
import os
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ["https://www.googleapis.com/auth/youtube"]
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TOKEN_PATH = os.path.join(SCRIPT_DIR, ".youtube_token.json")
DEFAULT_CLIENT_SECRET_PATH = os.path.join(SCRIPT_DIR, ".youtube_client_secret.json")


def obtener_credenciales(client_secret_path: str, token_path: str) -> Credentials:
    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secret_path):
                sys.exit(
                    f"No encontre {client_secret_path}. Descargalo de Google Cloud "
                    "Console (credencial OAuth tipo 'Desktop app', ver "
                    "references/automatizacion-subida-youtube.md) y guardalo ahi, "
                    "o pasa la ruta real con --client-secret."
                )
            flow = InstalledAppFlow.from_client_secrets_file(client_secret_path, SCOPES)
            print("Abriendo el navegador para autorizar el acceso a tu cuenta de YouTube...")
            creds = flow.run_local_server(port=0)

        with open(token_path, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"Token guardado en {token_path} (se reutiliza en corridas futuras).")

    return creds


def subir_video(video_path: str, titulo: str, descripcion: str, tags,
                 categoria_id: str, privacidad: str, client_secret_path: str,
                 token_path: str, playlist_id: str = None) -> str:
    if not os.path.exists(video_path):
        sys.exit(f"No encontre el archivo de video: {video_path}")

    creds = obtener_credenciales(client_secret_path, token_path)
    youtube = build("youtube", "v3", credentials=creds)

    body = {
        "snippet": {
            "title": titulo,
            "description": descripcion,
            "tags": tags or [],
            "categoryId": categoria_id,
        },
        "status": {
            "privacyStatus": privacidad,
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"  ... subiendo, {int(status.progress() * 100)}%")

    video_id = response["id"]
    url = f"https://youtu.be/{video_id}"
    print(f"Subida completa: {url}")

    if playlist_id:
        youtube.playlistItems().insert(
            part="snippet",
            body={
                "snippet": {
                    "playlistId": playlist_id,
                    "resourceId": {"kind": "youtube#video", "videoId": video_id},
                }
            },
        ).execute()
        print(f"Agregado a la playlist {playlist_id}.")

    return url


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--video-file", required=True, help="Ruta al .mp4 ya renderizado")
    ap.add_argument("--title", required=True, help="Titulo del video en YouTube (solo el tema, sin prefijo 'Video N -')")
    ap.add_argument("--description", default="", help="Descripcion del video")
    ap.add_argument("--tags", nargs="*", default=None, help="Tags separados por espacio")
    ap.add_argument("--category-id", default="27", help="ID de categoria de YouTube (default: 27, Educacion)")
    ap.add_argument("--playlist-id", default=None, help="ID de playlist de YouTube a la que agregar el video despues de subirlo (opcional -- nunca asumas un default, preguntale al usuario)")
    ap.add_argument("--privacy-status", default="unlisted", choices=["public", "unlisted", "private"],
                     help="Visibilidad del video (default: unlisted, igual que se sube hoy a mano)")
    ap.add_argument("--client-secret", default=DEFAULT_CLIENT_SECRET_PATH,
                     help=f"Ruta al client_secret.json (default: {DEFAULT_CLIENT_SECRET_PATH})")
    ap.add_argument("--token-path", default=DEFAULT_TOKEN_PATH,
                     help=f"Ruta donde guardar/leer el token OAuth (default: {DEFAULT_TOKEN_PATH})")
    args = ap.parse_args()

    subir_video(
        video_path=args.video_file,
        titulo=args.title,
        descripcion=args.description,
        tags=args.tags,
        categoria_id=args.category_id,
        privacidad=args.privacy_status,
        client_secret_path=args.client_secret,
        token_path=args.token_path,
        playlist_id=args.playlist_id,
    )


if __name__ == "__main__":
    main()
