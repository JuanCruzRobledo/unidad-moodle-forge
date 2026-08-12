# Automatización opcional de la subida de videos a YouTube

## Qué resuelve esto

`automatizacion-videos-actividad.md` ya cubre cómo se **genera** el `.mp4` de
cada video (actividad o introducción). Lo que faltaba era el paso siguiente:
subirlo a YouTube y devolver la URL real que reemplaza `URL_VIDEO_K` /
`URL_DEL_VIDEO_YOUTUBE`. Por default esto lo sigue haciendo el usuario a mano
(subir en youtube.com, copiar el link, pegártelo) — pero existe un camino
**opcional** validado en vivo (Metodología I, Unidad 1 y 2) vía la **YouTube
Data API v3**, para cuando el usuario quiere automatizarlo.

Mismo criterio que Gamma (`prompt-gamma-material-apoyo.md`) y NotebookLM por
browser (`notebooklm-guion.md`): el camino manual sigue siendo el default de la
skill — no todos los que la instalen van a tener ganas de crear un proyecto de
Google Cloud — y el camino automatizado es un atajo opcional que se activa
explícitamente.

## Setup (una vez por máquina, no por unidad)

Requiere que el usuario cree sus propias credenciales OAuth — la skill no
puede hacer esto por él, son pasos dentro de su cuenta de Google:

1. Crear un proyecto en [Google Cloud Console](https://console.cloud.google.com/projectcreate).
2. Habilitar la **YouTube Data API v3** para ese proyecto
   (`console.cloud.google.com/apis/library/youtube.googleapis.com`).
3. Configurar la pantalla de consentimiento OAuth (Google Auth Platform):
   tipo de usuario **Externos**, nombre de la app y correo de contacto (los
   propios del usuario), estado de publicación **Prueba** — no hace falta
   verificar la app para uso personal.
4. En **Acceso a los datos**, agregar el scope
   `https://www.googleapis.com/auth/youtube` (alcance completo: cubre subir,
   borrar/editar metadata y gestionar playlists — no uses solo
   `youtube.upload`, se queda corto para playlists y para poder corregir un
   error de subida sin tener que reautenticar de nuevo).
5. En **Público → Usuarios de prueba**, agregar el email del usuario.
6. En **Clientes**, crear un ID de cliente de OAuth tipo **App de escritorio**
   y descargar el JSON (botón "Descargar JSON" del diálogo de confirmación —
   nunca copiar el secreto a mano al chat).
7. Guardar ese archivo como `.youtube_client_secret.json` en la carpeta
   `scripts/` (incluida en el mismo bloqueo de seguridad que `.env*`, así que
   nunca lo leas vos con tus herramientas de archivo una vez guardado).

**Cuidado al hacer este setup con browser automation**: el diálogo de "Se creó
el cliente de OAuth" de Google Cloud Console muestra el secreto **en texto
plano en la pantalla**. Si tomás un screenshot de esa pantalla para verificar
que el flujo funcionó, el secreto queda visible en la conversación. Preferí
usar `find`/`read_page` para localizar el botón "Descargar JSON" sin necesidad
de un screenshot de esa pantalla puntual: descargalo directo, movelo con Bash
sin leer su contenido, y si ya tomaste el screenshot avisale al usuario que el
secreto quedó expuesto en la sesión (no es grave si es una conversación
privada del propio usuario, pero es honesto avisarlo — la mitigación, si el
usuario la quiere, es resetear el secreto desde Cloud Console).

## Primera corrida: autorización única

La primera vez que se corre `scripts/youtube_upload.py` (o cada vez que se
amplía el scope), abre el navegador del propio usuario para que autorice con
su cuenta de YouTube — va a ver el cartel de "Google no verificó esta app"
porque es una app propia en modo Prueba, no un problema real; el usuario debe
click "Avanzado → Ir a [nombre de la app] (no seguro)". Confirmalo vos con el
usuario antes de asumir que ya pasó — no dabas por hecho que autorizó sin que
te lo confirme. El token queda cacheado en `scripts/.youtube_token.json` y se
reusa en corridas futuras sin volver a pedir nada, salvo que se revoque o que
haga falta un scope nuevo (en ese caso, borrar el token viejo y volver a
correr para que pida consentimiento con el scope ampliado).

## Uso

```bash
python scripts/youtube_upload.py \
    --video-file "Actividades/actividad-2/videos/video-actividad-2-1.mp4" \
    --title "Anatomía de un prompt: los cuatro componentes" \
    --description "Material de cátedra, [materia] - TUP, UTN." \
    --privacy-status unlisted \
    --playlist-id PLxxxxxxxxxxxx
```

`--playlist-id` es opcional (ver regla dura de playlists más abajo).
`--privacy-status` default `unlisted` — es el mismo criterio que ya usaba el
camino manual, no lo cambies a `public` sin que el usuario lo pida.

## Regla dura: el título real NO lleva el prefijo "Video N –" ni el nombre de la materia

Confirmado contra un canal real con videos ya subidos (Unidad 1 completa, 10
videos): el texto que la actividad muestra en el HTML
(`references/plantillas-html.md`, tarjeta de video) tiene el formato "Video N
– [tema]" porque ahí hace falta numerar los 3 links dentro de la tarjeta — pero
el **título real del video en YouTube** es solo `[tema]`, sin el prefijo "Video
N –" y sin anteponer el nombre de la materia. Ejemplo real: el link dice
"Video 1 – Evolución histórica: de las tarjetas perforadas al desarrollo
asistido por IA" pero el título del video en YouTube es literalmente
"Evolución histórica: de las tarjetas perforadas al desarrollo asistido por
IA". Sacá el `[tema]` del propio texto del link en `actividad-N.html`
(la parte después de "Video N – ") o del guion (`# Guion — Video K de la
Actividad N: [tema puntual de este video]`).

## Regla dura: la organización en playlists NUNCA se asume ni se hardcodea

La skill **no tiene** un criterio propio de "una playlist por unidad", "todo
en una sola playlist" ni ningún otro patrón — es una decisión del usuario,
puede cambiar de unidad a unidad, y no se repite de memoria de una corrida a
la otra. Antes de subir el primer video de una tanda (actividad o unidad
nueva), preguntá con `AskUserQuestion` si van a una playlist y, si la
respuesta es sí, si es una playlist existente (pedí el ID/link) o una nueva
(pedí el nombre, o proponé uno basado en el tema de la unidad y esperá
confirmación). Si el usuario no quiere usar playlists, subí sin
`--playlist-id` y no vuelvas a preguntar en esa misma unidad.

Para inspeccionar playlists existentes del canal (útil para decidir si ya hay
una que corresponda) sin necesidad de abrir el navegador:

```python
youtube.playlists().list(part='snippet,contentDetails', mine=True, maxResults=25).execute()
```

## Regla dura: nunca subir en lote sin que el usuario lo haya pedido para esa tanda puntual

Mismo espíritu que la Regla dura de `automatizacion-videos-actividad.md`
("on-demand, nunca en lote") — acá aplica a la subida, no al render: subí un
video o el lote que el usuario pidió explícitamente ("subí los 3 que faltan de
la Actividad 2"), no barras automáticamente todos los `.mp4` con
`render_status: generado` y `url_subida: false` que encuentres en el
filesystem sin que te lo hayan pedido para esa corrida.

## Cuota

La cuota gratis de la API es 10.000 unidades/día; `videos.insert` cuesta 1.600
(≈6 subidas/día), `playlistItems.insert` cuesta ~50 (prácticamente gratis en
comparación). Si el usuario tiene más de ~6 videos pendientes en una sola
sesión, avisale que se va a cortar por cuota y va a hacer falta otra tanda al
día siguiente (o pedir un aumento de cuota a Google, que para uso personal
suele aprobarse en pocos días) — no falles en silencio ni reintentes en loop
si la API devuelve error de cuota agotada.

## Después de subir

Marcá en `estado.yml`: `videos[K].url_subida: true` + `videos[K].url: <link
real>` (mismos campos que ya usa el camino manual, ver
`estado-yml-schema.md`) y reemplazá el placeholder `URL_VIDEO_K` /
`URL_DEL_VIDEO_YOUTUBE` en el HTML correspondiente. Si se agregó a una
playlist, no hace falta un campo aparte en `estado.yml` — el ID de la playlist
alcanza con quedar mencionado en el reporte/():contexto de la corrida si el
usuario lo va a necesitar después.

## Si algo salió mal: borrar un video subido por error

```python
youtube.videos().delete(id='<video_id>').execute()
```

Requiere el scope completo `youtube` (no alcanza con `youtube.upload`). Nunca
borres un video sin confirmación explícita del usuario — a diferencia de subir
(reversible: se puede volver a subir), borrar es una acción real sobre el
canal del usuario.
