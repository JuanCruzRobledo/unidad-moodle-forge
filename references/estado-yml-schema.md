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
    introduccion:
      status: confirmado        # pendiente | generado | confirmado
    actividades:
      cantidad: 4
      items:
        - numero: 1
          nombre: "Inyección de dependencias"
          html_status: confirmado
          preguntas_xml_status: generado     # pendiente | generado | confirmado
          notebooklm:
            guion_status: generado
            link_pegado: false               # true cuando el usuario ya subió el notebook y pegó la URL real
        - numero: 2
          nombre: "Controllers y DTOs"
          html_status: pendiente
          preguntas_xml_status: pendiente
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
    importacion:                # Fase 8 — opcional, solo se llena cuando el usuario pide importar al aula real
      status: pendiente         # pendiente | en_progreso | completado
      curso_url: ""              # URL real del curso al que se importó (vacío si nunca se corrió)
      fecha: ""                  # fecha de la última corrida (YYYY-MM-DD)
      reporte: ""                # ruta al reporte-importacion.md generado (vacío si nunca se corrió)

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
  `URL_IA_NOTEBOOKLM`.
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
- `importacion.status` solo puede pasar a `en_progreso`/`completado` después de que
  se cumplieron las 5 precondiciones de la Fase 8 (`SKILL.md`) — no es un flag que
  se setea de antemano, es el registro de que la importación realmente ocurrió.
  `reporte` apunta siempre a un `reporte-importacion.md` real ya escrito en la
  carpeta de esa unidad — nunca se deja `completado` sin ese archivo.
