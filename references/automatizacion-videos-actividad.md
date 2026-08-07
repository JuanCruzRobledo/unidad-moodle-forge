# Automatización de los 3 videos por actividad (URL_VIDEO_1/2/3)

## Qué resuelve esto

Cada actividad trae 3 links de video (`references/plantillas-html.md` § Cuerpo de
cada actividad) que hasta ahora quedaban siempre como placeholder
(`URL_VIDEO_1/2/3`) — la skill nunca tuvo un mecanismo para producirlos. Esta
referencia define cómo se generan de verdad, apoyándose en la skill
`hyperframes` (composición de video + narración TTS ya instalada en este
entorno), en vez de dejarlos como "guion para que el docente grabe".

## Por qué HyperFrames y no el video nativo de NotebookLM

NotebookLM puede generar un "Resumen de video" a partir de sus fuentes (uno de
los 5 tipos de salida que ya usa `notebooklm-guion.md`). Se evaluó usarlo acá y
se descartó como mecanismo principal: NotebookLM **sintetiza** una narración con
sus propias palabras a partir de las fuentes — no existe forma de darle un guion
exacto para que lo lea al pie de la letra — así que es estructuralmente más
propenso a parafrasear, resumir de más, o desviarse del contenido real que un
guion escrito a mano. En cambio, en HyperFrames el guion **es literalmente** el
texto que se le pasa al motor de TTS (`npx hyperframes tts`): cero síntesis, cero
margen para que el "narrador" invente o generalice. Por eso HyperFrames es la
opción que de verdad respeta el guion sin alucinar.

## Regla dura: on-demand, nunca en lote

Cada video se genera **cuando el usuario pide avanzar esa actividad puntual**
("generame el video 1 de la Actividad 2 de la Unidad 3"), nunca como parte
automática de un barrido masivo sobre unidades/actividades pendientes. Renderizar
video real consume tiempo de cómputo y revisión — no se dispara sin que el
usuario lo esté pidiendo en ese momento.

## Estilo de composición: liviano, no producción pesada

Usar una composición simple de **slides narradas** (texto/imagen estático por
segmento + narración TTS + subtítulos), no animaciones complejas ni transiciones
elaboradas. El objetivo es un video claro y fiel al guion, no una pieza de
producción audiovisual — mantiene acotado el tiempo de render y de curación de
contenido por unidad (3 actividades × 3 videos = 9 por unidad, no es poco).

## Flujo por video

1. **Guion** (`Actividades/actividad-N/videos/guion-video-actividad-N-K.md`,
   K = 1, 2 o 3): mismo principio de fidelidad al material real que ya aplica
   `notebooklm-guion.md` y el guion de Introducción — nunca inventar contenido.
   Estructura sugerida:

   ```markdown
   # Guion — Video K de la Actividad N: [tema puntual de este video]

   ## Duración estimada
   [1-3 minutos — un video de actividad es corto y puntual, no una clase completa]

   ## Guion narrado (texto exacto para el TTS)
   [El texto completo, tal cual se va a narrar. Esto es lo que se le pasa a
   `npx hyperframes tts` — no un resumen del guion, el guion en sí.]

   ## Slides / segmentos
   - [00:00–00:15] [Qué se muestra en pantalla mientras se narra este tramo]
   - [00:15–00:40] [...]

   ## Fuente real
   [De dónde sale el contenido: ejercicios-resueltos.html § ..., cuadernillo
   Tutorial ..., ítem del programa.]
   ```

2. **Marcar** `videos[K].guion_status: generado` en `estado.yml`. Este guion ya
   sirve como transcripción exacta para el paquete de fuentes de NotebookLM
   (ver `notebooklm-guion.md`) — no hace falta transcribir el video después de
   renderizado, el guion ES la transcripción porque el TTS lo lee literal.

3. **Render con HyperFrames** (solo cuando el usuario lo pide explícitamente
   para ese video puntual):
   ```bash
   npx hyperframes init "video-u<N>-a<N>-<K>" --example blank --non-interactive
   # componer las slides narradas en la composición (ver skill `hyperframes`
   # para la sintaxis de composición HTML)
   npx hyperframes tts "$(cat guion-video-actividad-N-K.md)" --voice <voz> \
     --output narracion.wav
   npx hyperframes lint
   npx hyperframes render --quality standard --output video-actividad-N-K.mp4
   ```
   Usar `--quality draft` para iterar rápido y recién `standard` (o `high` si
   el usuario lo pide) para la versión final. Elegir una voz en español latino
   consistente entre los 3 videos de una misma actividad (`npx hyperframes tts
   --list` para ver las voces disponibles) — no mezclar voces distintas dentro
   de la misma actividad sin que el usuario lo pida.

4. **Marcar** `videos[K].render_status: generado` cuando el `.mp4` ya está
   renderizado y el usuario lo revisó (se reproduce bien, respeta el guion,
   audio sincronizado).

5. El `.mp4` **nunca se sube a YouTube automáticamente** — la skill no tiene
   ese paso. El usuario lo sube a mano y devuelve la URL real, que reemplaza el
   placeholder `URL_VIDEO_K` en `actividad-N.html`. Recién ahí `url_subida:
   true`.

## Checklist antes de dar un video por terminado

- ¿El guion sale 1:1 del material real de esa actividad, sin relleno genérico?
- ¿La narración renderizada coincide palabra por palabra con el guion (no hubo
  edición manual del audio que lo desvíe)?
- ¿La duración es razonable para un video de actividad (1-3 min), no una clase
  entera?
- ¿La voz es consistente con los otros videos de la misma actividad/unidad?

## Nota — override local de duración

Este documento define el **default de la skill** (1-3 min, video corto y
puntual, contenido = lo que ya está confirmado en la actividad). Un workspace
puntual puede decidir un objetivo de duración distinto (y habilitar research
verificado como insumo de contenido, no solo excepción) — eso es una decisión
local del proyecto, no un cambio al default de la skill, y por eso se documenta
en el `CLAUDE.md` de ese workspace, no acá. Antes de generar un video, revisar
si el `CLAUDE.md` del proyecto define un override de duración/research para
videos de actividad.
