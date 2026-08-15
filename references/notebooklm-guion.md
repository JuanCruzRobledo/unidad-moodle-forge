# NotebookLM por actividad — spec, guion fuente y automatización por browser

**Rebranding (2026-08-10):** el producto se renombró a **"Gemini Notebook"**
(`notebook.google.com` — `notebooklm.google.com` redirige ahí). Esta referencia
sigue llamándolo NotebookLM porque es como lo conoce la cátedra, pero cualquier UI
que se describa acá corresponde a la marca nueva.

NotebookLM no tiene API pública, pero **si el usuario tiene disponible el MCP/tool de
browser automation (`claude-in-chrome` u otro)**, la skill SÍ puede automatizar la
creación completa del notebook: subir fuentes, generar los 5 materiales de Studio y
compartirlo — validado en vivo en Unidad 1/Actividad 1 (Metodología I). Si no hay
browser automation disponible, el camino sigue siendo el de siempre: la skill entrega
el **guion/fuente** listo para que el usuario lo pegue a mano y genere los 5
materiales él mismo.

## Gate: cuándo tiene sentido generar esto

Este paquete de fuentes lista archivos reales de la actividad (el PDF de
Lectura, el/los PDF(s) de Material de apoyo, y los 3 guiones de video). No tiene
sentido generarlo antes de que esos archivos existan — estarías documentando
fuentes que todavía no están. **No generar el guion de NotebookLM de una
actividad hasta que**, para esa misma actividad:

- `material_apoyo.prompts[]` tenga al menos un ítem `prompt_status: generado`
  (ver `prompt-gamma-material-apoyo.md`) — o esté explícitamente vacío porque
  esa actividad no tiene material de apoyo real.
- `lectura_pdf.documento_html_status: generado` como mínimo (ver
  `plantilla-pdf-lectura.md`) — no hace falta esperar al PDF confirmado, alcanza
  con que el documento ya esté escrito.
- Los 3 `videos[].guion_status` estén en `generado` (ver
  `automatizacion-videos-actividad.md`) — no hace falta que estén renderizados,
  el guion ya sirve como transcripción exacta.

Si el usuario pide el guion de NotebookLM antes de que se cumpla esto, avisale
qué falta en vez de generar un paquete de fuentes incompleto.

## Configuración exacta a usar por tipo de material (según la cátedra)

Nombres de opciones confirmados contra la UI real de Gemini Notebook (2026-08-10) —
la tabla vieja usaba nombres genéricos que ya no coinciden 1:1 con los controles
reales, se corrigió acá:

| Material | Control en Studio | Configuración a elegir |
|---|---|---|
| Resumen de video | "Resumen en video" | Formato **Explicación** · idioma español (Latinoamérica) · estilo visual **Clásico** |
| Resumen de audio | "Resumen en audio" | Formato **Resumen** (NO "Análisis detallado", que es más largo/conversacional) · idioma español (Latinoamérica) — con formato "Resumen" no aparece selector de duración, ya es corto por diseño |
| Infografía (BETA) | "Infografía" | Orientación **Horizontal** · idioma español (Latinoamérica) · nivel de detalle **Detallado** |
| Presentación (BETA) | "Presentación con diapositivas" | Formato **Presentación detallada** · idioma español (Latinoamérica) · duración **Predeterminada** |
| Tarjetas didácticas | "Tarjetas didácticas" | Cantidad **Estándar** · dificultad **Media** |

**La imagen de la tarjeta "Infografía" del widget de la actividad (`URL_IMAGEN_INFOGRAFIA`
en `plantillas-html.md`) sale de ACÁ — del material "Infografía" de Studio — nunca de
nanobanana ni de ningún otro modelo de imagen aparte.** Nanobanana queda reservado para
otro tipo de imágenes (banner de introducción de unidad, por ejemplo).

Después de generar la infografía, comprimirla antes de subirla al aula (los PNG que
exporta Studio pesan ~5 MB, muy pesados para que el modal cargue rápido). Validado con
Python + Pillow, sin depender de un sitio externo:

```python
from PIL import Image
im = Image.open("Evolución_del_desarrollo_con_IA.png").convert("RGB")
w, h = im.size
new_w = 1600
im = im.resize((new_w, int(h * new_w / w)), Image.LANCZOS)
im.save("infografia-actividad-N.jpg", "JPEG", quality=82, optimize=True)
```

Bajó ~5 MB a ~300 KB sin pérdida visible en la corrida real. Si no hay Python/Pillow
disponible, el fallback sigue siendo https://www.iloveimg.com/es/comprimir-imagen.

## Plantilla de guion fuente por actividad

Generá un archivo `guion-actividad-N.md` con esta estructura — es lo que el usuario
pega como fuente en NotebookLM (además de los PDFs/videos que ya tenga la actividad):

```markdown
# Guion fuente — Actividad [N]: [NOMBRE DE LA ACTIVIDAD]

## Tema
[Tema principal de la actividad, en 1-2 líneas]

## Conceptos clave a cubrir
- [Concepto 1]: [definición/explicación breve]
- [Concepto 2]: [definición/explicación breve]
- [Concepto 3]: [definición/explicación breve]

## Ejemplos de aplicación
[1-2 ejemplos concretos que ilustren los conceptos — código, casos de uso, o
ejercicios resueltos, según la materia]

## Errores comunes / puntos de confusión
[Lo que suele confundir a los estudiantes en este tema, para que el resumen de
audio/video y las tarjetas los aborden explícitamente]

## Fuentes adicionales
Subí estos archivos reales como fuente en el mismo notebook, además de este guion:
- `documento-lectura-actividad-N.pdf` (Lectura obligatoria de la actividad)
- [Cada PDF de Material de apoyo ya generado en Gamma y subido por el usuario —
  listar los nombres reales de `material_apoyo.prompts[]`]
- `guion-video-actividad-N-1.md`, `guion-video-actividad-N-2.md`,
  `guion-video-actividad-N-3.md` (transcripción exacta de cada video — el TTS de
  HyperFrames los lee literal, así que sirven como transcripción sin necesidad
  de transcribir el `.mp4` renderizado)
```

**Regla dura**: el contenido de "Conceptos clave", "Ejemplos" y "Errores comunes" se
completa a partir del material real que aportó el usuario (apuntes, programa,
PDFs) — nunca se inventa un tema que no esté respaldado por lo que el docente trajo.
Si falta ese material para una actividad puntual, preguntale al usuario antes de
generar el guion.

## Automatización opcional por browser (si hay `claude-in-chrome` u otro MCP de browser)

Validado en vivo de punta a punta (Unidad 1/Actividad 1, Metodología I). Flujo
completo:

1. **Generá primero el `guion-actividad-N.md`** con la plantilla de más abajo — es
   una de las fuentes reales, no un paso previo descartable.
2. Navegá a `notebook.google.com`, click en "Crear nuevo" (o "+ Crear cuaderno").
   Gemini Notebook autotitula el cuaderno a partir de las fuentes que subas — no
   hace falta titularlo a mano.
3. **Subí como fuentes** (botón "Subir archivos", `input[type=file]` real, usar la
   herramienta de upload directo con las rutas locales, no el picker nativo del SO):
   - `Actividades/notebooklm/guion-actividad-N.md`
   - `Actividades/actividad-N/documento-lectura-actividad-N.pdf`
   - Cada `Actividades/actividad-N/material-apoyo/material-apoyo-N-K.pdf` que ya
     esté generado.
4. **Gotcha confirmado — NO subas las URLs de YouTube como fuente, aunque los 3
   videos ya estén subidos y confirmados en Moodle.** Se probó explícitamente: las 3
   URLs reales fallaron al importar con el error de la propia UI *"No se puede
   importar este video. La transcripción no está disponible."* — son videos TTS de
   HyperFrames, YouTube no les generó subtítulos automáticos. En su lugar, subí los
   3 `Actividades/actividad-N/videos/guion-video-actividad-N-K.md` como fuente de
   texto (son la transcripción exacta, el TTS los lee literal) — es el mismo criterio
   que ya usaba el camino manual, simplemente confirmado como el único que funciona
   incluso con el video ya público.
5. **Generá los 5 materiales de Studio** con la configuración de la tabla de arriba,
   uno por uno (no hace falta esperar a que termine uno para lanzar el siguiente,
   corren en paralelo). Gotcha de UI: el panel Studio reordena las tarjetas cada vez
   que un ítem pasa a "generando" (lo sube al tope de la lista) — usá `find` por el
   nombre exacto del botón en cada click, nunca coordenadas de un screenshot
   anterior, o vas a terminar clickeando el ítem equivocado.
6. **No te quedes esperando a que terminen — cortá ahí y preguntale al usuario
   después.** Tiempos reales observados: Tarjetas didácticas e Infografía ~1 min.
   Audio ~7 min. Video ~5 min. Presentación (BETA) fue la más lenta, ~9-10 min. Hacer
   polling en loop (wait+screenshot repetido) durante varios minutos es un mal uso
   del turno — a criterio explícito del usuario: **una vez que los 5 botones ya
   fueron clickeados y confirmaste por screenshot que quedaron en estado
   "generando", cerrá ese hilo de trabajo** (reportá qué botones tocaste — igual que
   el resumen que le diste al usuario en la corrida real: "Resumen en audio
   (Resumen), Resumen en video (Explicación/Clásico), Infografía
   (Horizontal/Detallado), Presentación (detallada, default), Tarjetas didácticas
   (Estándar/Media default)" — y esperá a que el usuario confirme que ya
   terminaron, en vez de vos ir a chequear en loop.
   **Límite diario**: Studio tiene un límite de generaciones por día. Si algún
   botón tira un error de límite alcanzado al clickearlo, NO reintentes — dejá esa
   generación como pendiente, avisale al usuario cuál quedó sin poder lanzarse, y
   continuá esa actividad puntual otro día (no bloquea las demás actividades ya
   generadas ni el resto del flujo).
## Cuando el usuario confirma que los 5 materiales ya terminaron de generarse

7. **Compartir — requiere confirmación explícita del usuario antes de tocarlo**,
   porque cambia la visibilidad de un documento real de su cuenta de Google: botón
   "Compartir" → "Acceso desde el cuaderno" → cambiar de "Restringido" a **"Cualquier
   persona que tenga el vínculo"** → Guardar. No asumas el valor por defecto
   ("Restringido" = nadie más puede abrirlo con el link, inútil para alumnos).
8. **Descargá la imagen de Infografía** desde el ítem "Infografía" de Studio (abrilo →
   menú "⋮" → "Descargar") y comprimila (ver más arriba). Esta es la imagen real de
   `URL_IMAGEN_INFOGRAFIA` — no te olvides de este paso, es fácil pegar solo el link de
   NotebookLM y dejar la infografía en placeholder.
9. **Subí la imagen y el PDF al draft area del Label** (botón imagen del toolbar de
   TinyMCE / "Crear enlace" → "Subir un archivo", mismo patrón que §9d de
   `importacion-moodle.md`) y capturá los `src`/`href` `draftfile.php` reales.
10. **Pegá TODO junto** — la URL real del notebook (`https://notebook.google.com/notebook/<uuid>`)
    en `URL_IA_NOTEBOOKLM` y el `draftfile.php` de la infografía en `URL_IMAGEN_INFOGRAFIA` —
    reconstruyendo el HTML COMPLETO offline y pisándolo con `setContent()` en una sola
    pasada, tanto en el `actividad-N.html` local como en el Label real de Moodle (§9d de
    `importacion-moodle.md`; nunca insertar sueltos sobre el Label ya renderizado). De
    paso, si el widget de Infografía o el bloque "Código de apoyo" faltan en el Label
    real (daño de una sesión anterior), esta reconstrucción completa los repara sin
    esfuerzo extra. Moodle reescribe el `draftfile.php` a `pluginfile.php` permanente al
    guardar.
11. Marcá en `estado.yml`: `notebooklm.link_pegado: true` + `notebooklm.url: <link>` y
    `infografia.imagen_status: generado` + `infografia.fuente: notebooklm_studio` (ver
    `estado-yml-schema.md`).

## Atajo: el notebook y sus 5 materiales ya existen, solo falta bajar la infografía

Caso frecuente en retrofit (Fase 9): en una sesión anterior ya se creó el
notebook, se subieron las fuentes y se lanzaron los 5 materiales de Studio —
pero se cortó el hilo antes del paso 8 (descargar la infografía) o antes del
paso 10 (pegar todo en el HTML). Si eso ya pasó, **no repitas los pasos 1-7**:
andá directo al paso 8 con la URL del notebook ya existente (`notebooklm.url`
en `estado.yml`) — abrí ese notebook, entrá a Studio, abrí el ítem Infografía
por su nombre real (no el genérico "Infografía": Studio lo autotitula con el
tema, ej. "Anatomía de un Prompt Profesional") → menú "⋮" → "Descargar",
comprimila y seguí desde ahí. Esto aplica aunque el `link_pegado` de esa
actividad todavía esté en `false` — bajar la infografía no depende de que el
link ya esté pegado en Moodle, son pasos independientes del mismo paquete.

## Si no hay browser automation disponible

Generá igual el `guion-actividad-N.md` (plantilla de abajo) y pedile al usuario que
lo suba a mano como fuente en Gemini Notebook junto con el resto de los archivos
reales de la actividad, usando la tabla de configuración de arriba. Cuando te pase
la URL real (`https://notebook.google.com/notebook/<uuid>`), reemplazá el
placeholder `URL_IA_NOTEBOOKLM` de la tarjeta "Asistente IA" en el HTML de la
actividad correspondiente y marcá `notebooklm.link_pegado: true` en `estado.yml`.
