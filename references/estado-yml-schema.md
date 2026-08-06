# Esquema de `estado.yml`

Vive en la raíz de la carpeta de la materia (junto a las carpetas `Unidad N - .../`).
Lo crea/actualiza `scripts/scaffold_unidad.py`; el agente lo lee al arrancar (Fase 0
de SKILL.md) y lo actualiza a mano (Read/Edit) a medida que confirma cada
sub-sección — no hace falta un script aparte para actualizarlo, es un archivo de
datos simple.

## Estructura

```yaml
materia: "Programación 3"
carrera_variante: prog3   # prog1 | prog2 | prog3 -> define qué variante de entrega de TP usar
prefijo_banco_preguntas: "SPRING"  # prefijo de códigos de pregunta para esta materia, ver formato-preguntas-moodle-xml.md

unidades:
  - numero: 1
    nombre: "Fundamentos Spring Boot"
    carpeta: "Unidad 1 - Fundamentos Spring Boot"
    incluir:                    # ver Fase 0 de SKILL.md -- se pregunta SOLO al crear una unidad nueva
      actividad_ludica: true
      microteaching: false      # ej: la materia no usa esta sub-sección en el aula real
      material_apoyo: true
      videos_actividad: true
      autoevaluacion: true
      encuesta_cierre: true
    introduccion:
      status: confirmado        # pendiente | generado | confirmado
      video_guion_status: pendiente   # guion-video-introduccion.md -- se genera AL CIERRE del flujo
                                       # de la unidad (después de Actividades/Práctica/Autoevaluación),
                                       # nunca en la Fase 1, para que el guion sea coherente con el
                                       # contenido ya cerrado de toda la unidad
    actividades:
      cantidad: 4
      items:
        - numero: 1
          nombre: "Inyección de dependencias"
          html_status: confirmado
          preguntas_xml_status: generado     # pendiente | generado | confirmado
          material_apoyo:             # carpeta Moodle "Material de apoyo – Actividad N"
            prompts:                  # 1 o más, según lo que necesite la actividad -- ver
                                       # references/prompt-gamma-material-apoyo.md
              - nombre: "Profundización: inyección de dependencias con casos reales"
                prompt_status: generado    # pendiente | generado -- el entregable de la skill ES el
                                            # texto del prompt, nunca un PDF (Gamma no tiene API)
                pdf_subido_por_usuario: false  # true cuando el usuario confirma que ya generó el PDF
                                                # en Gamma y lo subió a la carpeta de Moodle
          lectura_pdf:                # tarjeta "Lectura PDF" -- documento-lectura-actividad-N.html
            documento_html_status: pendiente
            pdf_status: pendiente     # mismo gate que practica.pdf_status: nunca "generado" sin
                                       # pdf_confirmado_por_usuario en true primero
            pdf_confirmado_por_usuario: false
          videos:                     # 3 videos de la actividad (URL_VIDEO_1/2/3) -- ver
                                       # references/automatizacion-videos-actividad.md
            - numero: 1
              guion_status: pendiente     # pendiente | generado -- guion-video-actividad-N-1.md
              render_status: pendiente    # pendiente | generado -- el .mp4 ya se renderizó con
                                           # la skill hyperframes (se genera ON DEMAND, nunca en lote)
              url_subida: false           # true cuando el usuario subió el .mp4 a YouTube y pegó
                                           # la URL real en el HTML
            - numero: 2
              guion_status: pendiente
              render_status: pendiente
              url_subida: false
            - numero: 3
              guion_status: pendiente
              render_status: pendiente
              url_subida: false
          notebooklm:
            guion_status: generado    # el paquete de fuentes NO se genera hasta que material_apoyo
                                       # y lectura_pdf estén como mínimo "generado" y los 3 videos
                                       # tengan guion_status "generado" -- ver references/notebooklm-guion.md
            link_pegado: false               # true cuando el usuario ya subió el notebook y pegó la URL real
        - numero: 2
          nombre: "Controllers y DTOs"
          html_status: pendiente
          preguntas_xml_status: pendiente
          material_apoyo:
            prompts: []
          lectura_pdf:
            documento_html_status: pendiente
            pdf_status: pendiente
            pdf_confirmado_por_usuario: false
          videos:
            - numero: 1
              guion_status: pendiente
              render_status: pendiente
              url_subida: false
            - numero: 2
              guion_status: pendiente
              render_status: pendiente
              url_subida: false
            - numero: 3
              guion_status: pendiente
              render_status: pendiente
              url_subida: false
          notebooklm:
            guion_status: pendiente
            link_pegado: false
    practica:
      consigna_html_status: generado    # bloque breve en la pagina de Moodle, ver plantillas-html.md
      entrega_html_status: generado     # bloque de formato de entrega en la pagina de Moodle
      documento_html_status: generado   # documento-practica.html: la consigna completa con membrete, ver plantilla-pdf-practica.md
      pdf_status: pendiente        # pendiente | generado -- NUNCA pasar a "generado" sin confirmación explícita del usuario sobre documento-practica.html
      pdf_confirmado_por_usuario: false
    microteaching:
      status: pendiente
    autoevaluacion:
      preguntas_esperadas: 10
      html_status: pendiente
      preguntas_xml_status: pendiente
    encuesta_cierre:
      status: pendiente
    importacion:                # Fase 8 — opcional, se llena solo cuando el usuario pide importar al aula real.
      status: pendiente         # pendiente | en_progreso | completado -- SIEMPRE derivado de subsecciones de abajo, nunca se setea a mano suelto
      curso_url: ""              # URL real del curso al que se importó (vacío si nunca se corrió)
      seccion_raiz: null         # section= de la unidad en el curso real (el mapeo confirmado en la precondición 4 de Fase 8)
      fecha_inicio: ""           # fecha de la primera corrida sobre esta unidad (YYYY-MM-DD)
      fecha_ultima_corrida: ""   # fecha de la corrida más reciente, se pisa cada vez
      reporte: ""                # ruta a reporte-importacion.md (vacío si nunca se corrió)
      subsecciones:               # granularidad por pestaña -- esto es lo que permite retomar "por dónde quedó"
        introduccion: pendiente        # pendiente | importado
        actividades:
          status: pendiente            # pendiente | en_progreso | completado -- derivado de items de abajo
          items:
            - numero: 1
              importado: pendiente     # pendiente | importado -- incluye Label + Cuestionario + preguntas de ESA actividad
            - numero: 2
              importado: pendiente
        practica: pendiente
        microteaching: pendiente
        autoevaluacion: pendiente
        encuesta_cierre: pendiente

evaluaciones_curso:          # Fase 7 — aparte, opcional, se activa solo si el usuario la pide
  activa: false
  parciales:
    - nombre: "Primer parcial"
      consigna_html_status: pendiente    # presentacion-evaluacion-<nombre>.html (banner + tarjeta "Importante")
      pdf_status: pendiente               # documento-evaluacion-<nombre>.html -> PDF, ver plantilla-evaluacion.md
      pdf_confirmado_por_usuario: false   # gate: pdf_status NUNCA pasa a generado sin esto en true
      entrega_status: pendiente           # entrega-evaluacion-<nombre>.html (tarjeta de descripción del assign)
      certificado_status: pendiente       # customcert (u equivalente del LMS) ya configurado y gateado, no HTML
      foro_status: pendiente              # foro de consultas nativo, sin HTML propio
  recuperatorios:
    - nombre: "Recuperatorio primer parcial"
      consigna_html_status: pendiente
      pdf_status: pendiente
      pdf_confirmado_por_usuario: false
      entrega_status: pendiente
      certificado_status: pendiente
      foro_status: pendiente

trabajo_practico_integrador:   # Fase 7 — curso-level, ver plantilla-tpi-standalone.md
  activo: false
  consigna_html_status: pendiente    # presentacion-tpi.html (banner + tarjeta de descarga + video)
  pdf_status: pendiente              # documento-tpi.html -> PDF
  pdf_confirmado_por_usuario: false  # mismo gate que en practica y evaluaciones_curso
  metodo_entrega_status: pendiente   # metodo-entrega-tpi.html
  entrega_status: pendiente          # assign de entrega del TPI
  certificado_status: pendiente      # si el TPI emite certificado propio; na si no aplica
  foro_status: pendiente             # foro de consultas del TPI
```

## Reglas de uso

- **`incluir` se pregunta una sola vez, solo al crear una unidad NUEVA** (Fase 0
  de SKILL.md, vía `AskUserQuestion`), nunca al retomar una unidad existente. Si
  una unidad vieja no tiene este bloque, se asume que todos los componentes
  aplican (retrocompatibilidad — el default del script y de la skill es
  siempre `true`). Un componente en `false` significa que esa fase se saltea
  por completo para esa unidad — no se pregunta de nuevo ni se generan sus
  placeholders.
- **Orden de dependencias por actividad** (no generar un paso sin que el
  anterior esté al menos `generado`, salvo que `incluir` lo desactive):
  `actividad-N.html` → `material_apoyo` (prompt de Gamma) → `lectura_pdf`
  (documento + confirmación + PDF) → `videos` (guion + render on-demand) →
  `notebooklm` (paquete de fuentes). El `video_guion_status` de `introduccion`
  se genera último, al cierre de toda la unidad.
- `status` / `*_status` usan siempre los mismos tres valores: `pendiente`,
  `generado` (el agente ya escribió el archivo, pero el usuario no lo confirmó
  todavía), `confirmado` (el usuario dio el visto bueno).
- `pdf_status` en `practica` solo puede pasar a `generado` si
  `pdf_confirmado_por_usuario: true` está seteado primero — es la compuerta de
  aprobación de SKILL.md hecha dato, para que quede auditable qué pasó y cuándo.
  La confirmación es sobre `documento-practica.html` (el documento con
  membrete, ver `plantilla-pdf-practica.md`), no sobre `consigna-practica.html`
  (el bloque de la página de Moodle).
- `notebooklm.link_pegado` queda en `false` hasta que el usuario devuelva la URL
  real del notebook — mientras tanto el HTML de la actividad tiene el placeholder
  `URL_IA_NOTEBOOKLM`. El `notebooklm.guion_status` de una actividad no debería
  pasar a `generado` hasta que `material_apoyo` y `lectura_pdf` de esa misma
  actividad estén como mínimo `generado` y sus 3 `videos` tengan `guion_status:
  generado` — el paquete de fuentes de NotebookLM lista esos archivos reales
  (ver `references/notebooklm-guion.md`), así que generarlo antes sería
  documentar fuentes que todavía no existen.
- `lectura_pdf.pdf_status` usa el mismo gate que `practica.pdf_status`: nunca
  pasa a `generado` sin `lectura_pdf.pdf_confirmado_por_usuario: true` seteado
  primero, y la confirmación es sobre `documento-lectura-actividad-N.html` (ver
  `references/plantilla-pdf-lectura.md`).
- `material_apoyo.prompts[].prompt_status` pasa a `generado` en cuanto la skill
  escribe el texto del prompt — no depende de ninguna confirmación del usuario
  (no hay PDF que renderizar de este lado, es un entregable de texto). `
  pdf_subido_por_usuario` es aparte y queda en `false` hasta que el usuario
  confirme que corrió el prompt en Gamma y subió el PDF resultante a la carpeta
  real de Moodle.
- `videos[].render_status` pasa a `generado` cuando la skill ya renderizó el
  `.mp4` con la skill `hyperframes` (siempre on-demand, nunca en lote para
  varias actividades/unidades a la vez — ver
  `references/automatizacion-videos-actividad.md`). `url_subida` es aparte y
  quiere decir que el usuario ya subió ese `.mp4` a YouTube y devolvió la URL
  real para reemplazar el placeholder `URL_VIDEO_N`.
- El mismo gate de `pdf_status` aplica en `evaluaciones_curso.parciales[]`,
  `evaluaciones_curso.recuperatorios[]` y `trabajo_practico_integrador`: nunca
  pasa a `generado` sin `pdf_confirmado_por_usuario: true` seteado primero, y la
  confirmación es siempre sobre el `documento-*.html` con membrete (ver
  `plantilla-evaluacion.md` / `plantilla-tpi-standalone.md`), no sobre el bloque
  de presentación que va en la página de Moodle.
- `certificado_status` documenta si el módulo de certificado del LMS (no HTML)
  ya está configurado y con su regla de disponibilidad gateada a la Entrega
  correspondiente — si el usuario todavía no lo armó en el LMS, se anota
  `pendiente` y se le avisa, no se inventa contenido de certificado.
- Cuando arrancás una sesión nueva, leé este archivo completo antes de preguntarle
  nada al usuario — la mayoría de "¿en qué quedamos?" se responde solo con esto.
- **`importacion.subsecciones` es la unidad real de progreso de la Fase 8** — se
  actualiza **apenas termina de pegarse/crearse esa pestaña en el aula**, no al
  final de toda la corrida. Así, si la sesión se corta a mitad de camino (o el
  usuario para a propósito para seguir otro día), la próxima corrida de Fase 8 lee
  `estado.yml`, ve qué pestañas ya están `importado` y arranca directo desde la
  primera que sigue en `pendiente` — sin volver a preguntar ni re-pegar contenido ya
  subido. Para `actividades`, la granularidad baja hasta el nivel de cada actividad
  individual (`items[].importado`): si se cortó a mitad de la Actividad 2, la 1
  queda `importado` y no se re-toca al retomar.
- **`importacion.status` (a nivel unidad) es siempre derivado, nunca se setea a
  mano suelto**: `pendiente` si ninguna subsección está `importado`; `en_progreso`
  si hay alguna `importado` pero no todas; `completado` solo cuando **todas** las
  subsecciones (y todos los items de `actividades`) están `importado` **y** ya
  existe `reporte-importacion.md`. Recalculalo cada vez que marques una subsección.
- `curso_url` y `seccion_raiz` se completan la primera vez que se corre la Fase 8
  sobre esa unidad (después de pasar la precondición 1 y 4) y se reutilizan tal
  cual en corridas posteriores sobre la misma unidad — no se vuelven a preguntar
  salvo que el usuario diga que cambió el curso/mapeo.
  `reporte` apunta siempre a un `reporte-importacion.md` real ya escrito en la
  carpeta de esa unidad — nunca se deja `completado` sin ese archivo.
