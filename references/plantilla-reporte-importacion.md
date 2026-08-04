# Plantilla — `reporte-importacion.md`

Se genera/actualiza al final de cada corrida de la Fase 8 (Importación), siempre —
aunque la corrida se haya cortado a mitad de camino. Va en la **raíz de la carpeta
de la unidad importada** (ej. `Metodologia I/Unidad 1 - Marco funcional/
reporte-importacion.md`). Si ya existe uno de una corrida anterior sobre la misma
unidad, actualizalo (agregá una entrada nueva con fecha, no borres el historial
previo).

Completá cada sección con lo que realmente pasó en esa corrida — si una sección no
aplica (ej. no hubo incoherencias), dejala con "Ninguna detectada en esta corrida",
no la borres del documento.

---

```markdown
# Reporte de importación — Unidad N: <Nombre de la unidad>

**Curso:** <URL del curso> (id=<courseid>)
**Fecha de la corrida:** <YYYY-MM-DD>
**Corrida:** completa | cortada (motivo: <...>)

## 1. Resumen de lo importado

| Sub-sección | Estado | Detalle |
|---|---|---|
| Introducción (raíz) | importado / parcial / no iniciado | <qué se pegó/creó> |
| Actividades | importado / parcial / no iniciado | <cuántas actividades, cuestionarios importados> |
| Práctica | importado / parcial / no iniciado | <Archivo PDF, Label, Tarea> |
| Microteaching | importado / parcial / no iniciado / fuera de alcance | |
| Autoevaluación | importado / parcial / no iniciado | <cuestionario + preguntas> |
| Encuesta de cierre | importado / parcial / no iniciado | |

## 2. Contenido faltante / placeholders sin resolver

Todo lo que quedó en el aula real con un placeholder de la skill (`URL_...`) sin
reemplazar por un recurso real. Sé específico: dónde está, qué falta.

- [ ] <ej. Imagen del banner de Inicio (`URL_DE_LA_IMAGEN`) — módulo/campo: Descripción de la sección>
- [ ] <ej. Video de introducción (`URL_DEL_VIDEO_YOUTUBE`) — Label "01-video-introduccion">
- [ ] <ej. Actividad 1: 3 links de video, PDF de lectura, Asistente NotebookLM, código de apoyo>
- [ ] <ej. Imagen de infografía de cada actividad (`URL_IMAGEN_INFOGRAFIA`) — 1 por actividad>

## 3. Carpetas o módulos dejados vacíos/ocultos a propósito

Con el motivo — para que quede claro que es una decisión tomada, no un olvido.

- <ej. Carpeta "Material de apoyo – Actividad 2 (pendiente)": vacía porque la skill
  no generó ningún archivo descargable para ese lugar en esta unidad.>
- <ej. Módulo "Comparar solución en Colab" (Práctica): oculto en vez de borrado, sin
  equivalente en el material de Metodología — por si se reusa esa estructura más
  adelante.>

## 4. Incoherencias detectadas

Cualquier cosa que no cierre entre el material local y el estado real del curso:
contenido duplicado, nombres de sección que no coinciden, módulos del template
viejo sin equivalente, discrepancias de conteo (actividades, preguntas), etc.

- <ej. La sub-sección Práctica tenía 2 copias completas de los 5 módulos (bug de
  contenido duplicado al reciclar la unidad de otra materia) — se conservó 1 copia
  y se borró la otra, confirmado con el usuario.>

## 5. Próximos pasos recomendados

- <ej. Generar y subir la imagen de banner de la unidad.>
- <ej. Grabar el video de introducción usando `guion-video-introduccion.md`.>
- <ej. Confirmar con el usuario si Microteaching entra en esta importación.>
```
