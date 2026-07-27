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
      consigna_html_status: generado
      entrega_html_status: generado
      pdf_status: pendiente        # pendiente | generado -- NUNCA pasar a "generado" sin confirmación explícita del usuario sobre el HTML
      pdf_confirmado_por_usuario: false
    microteaching:
      status: pendiente
    autoevaluacion:
      preguntas_esperadas: 10
      html_status: pendiente
      preguntas_xml_status: pendiente
    encuesta_cierre:
      status: pendiente

evaluaciones_curso:          # Fase 7 — aparte, opcional, se activa solo si el usuario la pide
  activa: false
  parciales:
    - nombre: "Primer parcial"
      status: pendiente
  recuperatorios:
    - nombre: "Recuperatorio primer parcial"
      status: pendiente
```

## Reglas de uso

- `status` / `*_status` usan siempre los mismos tres valores: `pendiente`,
  `generado` (el agente ya escribió el archivo, pero el usuario no lo confirmó
  todavía), `confirmado` (el usuario dio el visto bueno).
- `pdf_status` en `practica` solo puede pasar a `generado` si
  `pdf_confirmado_por_usuario: true` está seteado primero — es la compuerta de
  aprobación de SKILL.md hecha dato, para que quede auditable qué pasó y cuándo.
- `notebooklm.link_pegado` queda en `false` hasta que el usuario devuelva la URL
  real del notebook — mientras tanto el HTML de la actividad tiene el placeholder
  `URL_IA_NOTEBOOKLM`.
- Cuando arrancás una sesión nueva, leé este archivo completo antes de preguntarle
  nada al usuario — la mayoría de "¿en qué quedamos?" se responde solo con esto.
