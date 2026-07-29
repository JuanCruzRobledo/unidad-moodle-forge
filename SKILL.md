---
name: unidad-moodle-forge
description: >-
  Genera el material didactico completo de una unidad para el aula virtual Moodle de TUP (tup.sied.utn.edu.ar) a partir del programa de la materia o apuntes: HTML de cada sub-seccion (Introduccion, Actividades, Practica, Microteaching, Autoevaluacion, Encuesta de cierre), preguntas en formato XML de Moodle para importar (5 por actividad, 10 en autoevaluacion), guiones para generar los Notebooks LM de cada actividad, la consigna y el PDF del Trabajo Practico Integrador, y -al final del proceso- el material de Evaluaciones (parciales/recuperatorios) a nivel curso. Usa esta skill SIEMPRE que el usuario pida armar/generar el material de una unidad para el campus/aula virtual: 'arma la unidad 3 de Programacion 3', 'genera el contenido Moodle de la unidad de CSS', 'necesito las preguntas XML y el HTML de la actividad 2', 'hace el TP integrador y su PDF', 'segui armando el material donde quedo' -aunque no nombre la skill. Mantiene un archivo de estado (estado.yml) por materia para retomar la generacion unidad por unidad y saber que falta. NO usar para corregir entregas de alumnos (corregir/corregir-notas-planilla), ni para responder consultas en el campus (responder-alumnos), ni para generar informes de pendientes (informe-pendientes-curso).
license: Apache-2.0
---

# Unidad Moodle Forge

Convierte el programa de una materia (o los apuntes que le pases) en el material completo de una unidad del aula virtual, calcando la estructura real del campus TUP: no la que "se supone" que tiene una unidad, sino la que confirmamos recorriéndolo en vivo. El principio que ordena todo: **generar es barato, pero publicar contenido pedagógico mal fundamentado es caro** — por eso cada bloque parte de material real que aportó el usuario (nunca se inventan resultados de aprendizaje o consignas de la nada), y los pasos irreversibles o que dependen de una herramienta externa (PDF, NotebookLM) esperan confirmación explícita antes de ejecutarse.

## Cuándo aplica

El usuario es docente/tutor de una materia en el campus TUP y quiere producir el contenido de una unidad completa (o retomar una a medio hacer) a partir de: el programa de la materia, apuntes propios, un PDF de cátedra, o simplemente el nombre del tema. No tiene por qué traer todo listo — puede pedir "armá la unidad 2 de CSS" y vos completás con el patrón ya validado contra el aula real, pidiendo solo lo que no se pueda derivar razonablemente (ej. el tema puntual de cada actividad si no lo aportó).

## Workflow — 7 fases + 1 final opcional

```
0. Relevar estado     → qué unidad/sub-sección falta (lee estado.yml)
1. Introducción       → HTML: banner+resultados, video, sección foro, hoja de ruta
2. Actividades        → HTML por actividad + XML (5 preguntas c/u) + guion NotebookLM
3. Práctica (TP)      → documento PDF con membrete *bajo aprobación* → entrega HTML → consigna breve HTML (Moodle)
4. Microteaching      → HTML banner + contenido
5. Autoevaluación     → HTML + XML (10 preguntas)
6. Encuesta de cierre → HTML (casi fijo entre unidades)
7. (final, opcional)  → Evaluaciones curso-level (parciales/recuperatorios)
```

Las fases 1 a 6 son por unidad y se repiten unidad tras unidad. La fase 7 es **aparte**: solo se dispara cuando el usuario la pide explícitamente y después de que las unidades estén encaminadas — no se mezcla con el material de unidad porque vive en una sección de curso distinta (`Evaluaciones`, no `Autoevaluación`).

**Nunca generes el PDF de la Práctica sin que el usuario haya confirmado antes que el documento (`documento-practica.html`) está bien.** El PDF es una conversión fiel de ese documento (no un HTML aparte que puede quedar desincronizado) — generarlo antes de la confirmación duplica el trabajo si el documento cambia. Este documento **no es** el bloque `consigna-practica.html` que va en la página de Moodle — son dos archivos distintos, ver Fase 3.

## Fase 0 — Relevar estado

Antes de escribir nada, buscá `estado.yml` en la raíz de la carpeta de la materia (ver esquema completo en `references/estado-yml-schema.md`). Si no existe, es la primera unidad: creala con `scripts/scaffold_unidad.py`. Si existe, leelo para saber qué sub-secciones de qué unidad ya están `generado`, `confirmado` o `pendiente` — así no repetís trabajo ni perdés el hilo entre sesiones. Preguntale al usuario solo por lo que el estado no resuelve (ej. "¿confirmás que el HTML de la Práctica quedó bien para generar el PDF?").

## Fase 1 — Introducción de la unidad

Es la página raíz de la sección de la unidad en Moodle (no una sub-sección aparte — así es como vive en el aula real). Usá el bloque de `references/plantillas-html.md` § Introducción: banner con resultados de aprendizaje (completá 3-5 resultados concretos a partir del material que trajo el usuario), video colapsable (dejá `URL_DEL_VIDEO_YOUTUBE` como placeholder si no hay video todavía), sección con link al foro de la unidad, y la hoja de ruta con la tabla de tiempos Pomodoro (la tabla de tiempos se completa recién al final, cuando ya generaste todas las actividades y sabés cuántos minutos estimar).

## Fase 2 — Actividades

Por cada actividad (normalmente 3-4, confirmá la cantidad con el usuario si no la trajo): generá el bloque HTML (`references/plantillas-html.md` § Cuerpo de actividad) con sus 3 tarjetas (Infografía con modal+script, Lectura PDF, Asistente IA), y el XML de exactamente 5 preguntas para importar al banco de Moodle (`scripts/generar_pregunta_xml.py` + `references/formato-preguntas-moodle-xml.md`; seguí la convención de códigos de pregunta vista en el aula real, ej. `TEMA 1`.. `TEMA 5`). Generá también el guion de NotebookLM (`references/notebooklm-guion.md`) — **nunca crees el notebook vos**: NotebookLM no tiene API pública, así que tu entregable es el guion/fuente listo para pegar, y el link de la tarjeta queda como placeholder hasta que el usuario lo suba a mano y te devuelva la URL real.

Si el tema se presta, sumá una Actividad Lúdica (mismo archivo de referencia, bloque separado) — es opcional, no todas las unidades la tienen.

## Fase 3 — Práctica / Trabajo Práctico

Acá se generan **tres archivos distintos**, no uno solo, y **en este orden** — no es
arbitrario: el formato de entrega (punto 2) describe qué se entrega, y eso recién se
sabe con precisión una vez que la consigna completa (punto 1) está escrita; el
resumen para la página de Moodle (punto 3) linkea al PDF ya generado, así que
necesita que el PDF ya exista.

1. **`documento-practica.html`** — PRIMERO. El documento completo con membrete institucional que el alumno descarga como PDF desde la pestaña Práctica. Es un documento sobrio (sin tarjetas ni degradés del resto del aula), con estructura tipo TP real de cátedra: Objetivo general, Marco teórico (opcional), y el cuerpo de la consigna — que puede ser un **Caso Práctico** con pasos numerados (TP de código/procedimental), **preguntas de análisis por sección temática** (TP de reflexión/teoría), o una combinación de ambos según lo que pida el TP real — cerrando con Consideraciones y Conclusiones esperadas. Ver `references/plantilla-pdf-practica.md` para la plantilla completa y cuándo usar cada bloque. Mostraselo al usuario y **esperá su confirmación explícita antes de correr `scripts/render_pdf.py`** sobre ese archivo, pasando `--materia "<nombre de la materia>"` para que agregue el membrete (logo UTN + institución en el encabezado, barra de color + número de página en el pie, repetidos en cada hoja vía `header_template`/`footer_template` de Playwright — no se duplican a mano en el HTML). Recién ahí generás el PDF fiel. Actualizá `estado.yml` marcando `documento_html_status` y, tras la confirmación, `pdf_status` como generado.
2. **`entrega-practica.html`** — SEGUNDO, ya con la consigna confirmada a mano. El bloque de formato de entrega, usando la variante correcta según la carrera/materia: Python de archivo único (Programación 1), o estructura de paquetes en Java (Programación 2/3) — las 3 variantes están en `references/plantillas-html.md` § Trabajo Práctico. Necesita la consigna ya escrita porque describe qué archivo(s) exactos entrega el alumno (nombre del TP, cantidad de fichas/archivos, etc.), no se puede redactar bien antes.
3. **`consigna-practica.html`** — TERCERO. El bloque `<details>` que va en la página de Moodle (banner + resumen breve del TP). Con el documento PDF (punto 1) ya generado, este bloque es un resumen corto con un link de descarga al PDF, no la letra completa del TP.

## Fase 4 — Microteaching

Bloque de banner + contenido con el link al video de microteaching y al repositorio de código si aplica (`references/plantillas-html.md` § Microteaching). Es la sección más liviana — no tiene NotebookLM ni preguntas.

## Fase 5 — Autoevaluación

Mismo patrón que Actividades pero con **exactamente 10 preguntas** en el XML (`scripts/generar_pregunta_xml.py`), reutilizando o extendiendo el banco de preguntas de las actividades de la misma unidad (en el aula real comparten banco: los códigos de autoevaluación son un superset de los de actividades). El banner y la descripción son casi fijos entre unidades — solo cambia el nombre de la unidad.

## Fase 6 — Encuesta de cierre

Bloque fijo (`references/plantillas-html.md` § Encuesta de cierre) — el contenido no cambia entre unidades salvo el nombre de la unidad en el banner. No hace falta pedirle nada al usuario acá.

## Fase 7 — Evaluaciones (curso-level, opcional y al final)

Solo si el usuario la pide explícitamente. Vive fuera de la carpeta de unidades (es una sección de curso aparte, con parciales/recuperatorios/certificados) — no la generes de oficio ni la mezcles con el material de unidad. Documentá su propio estado en `estado.yml` bajo una clave separada.

## Reglas duras

- **Nunca inventes contenido pedagógico de la nada.** Resultados de aprendizaje, consignas y preguntas siempre parten del material que aportó el usuario (programa, apuntes, PDFs). Si falta información concreta, preguntala — no rellenes con genérico solo para completar la plantilla.
- **Fidelidad 1:1 con la plantilla oficial.** El prompt oficial del PDF de plantillas es explícito: "reescribí el contenido respetando exactamente su estructura, estilos e IDs, sin eliminar, resumir ni fusionar información". Aplicá esa misma regla vos: no simplifiques ni fusiones bloques de la plantilla al completarlos.
- **La estructura de tabs/carpetas calca la jerarquía real confirmada**, no la que se asume a priori — 5 sub-secciones hijas (Actividades, Práctica, Microteaching, Autoevaluación, Encuesta de cierre) más la Introducción viviendo en la raíz de la unidad. Ver `references/estructura-aula-real.md` para el detalle y las inconsistencias reales que NO hay que replicar.
- **NotebookLM nunca se automatiza.** Entregable = guion fuente, nunca un link inventado.
- **El PDF de la Práctica nunca se genera sin aprobación explícita del documento (`documento-practica.html`)** que lo origina.
- **El PDF de la Práctica no es una captura de la página de Moodle.** Es un documento con membrete institucional (ver `references/plantilla-pdf-practica.md`), no el HTML con tarjetas/degradés de `consigna-practica.html`.

## Componentes de la skill

| Archivo | Para qué |
|---|---|
| `scripts/scaffold_unidad.py` | Crea la carpeta de una unidad nueva (6 sub-carpetas) y crea/actualiza `estado.yml` en la raíz de la materia |
| `scripts/generar_pregunta_xml.py` | Convierte un YAML simple de preguntas a XML de Moodle importable |
| `scripts/render_pdf.py` | Convierte un HTML ya confirmado a PDF fiel (Playwright + Chromium); con `--materia` agrega membrete institucional (header/footer repetidos) |
| `references/plantillas-html.md` | Los bloques HTML oficiales de cada sub-sección, listos para completar |
| `references/plantilla-pdf-practica.md` | Plantilla del documento con membrete que se convierte en el PDF descargable de la Práctica |
| `references/estructura-aula-real.md` | Jerarquía real confirmada del aula + inconsistencias a no replicar |
| `references/formato-preguntas-moodle-xml.md` | Schema de pregunta Moodle XML + convención de códigos |
| `references/notebooklm-guion.md` | Spec de configuración de NotebookLM por tipo de material + plantilla de guion |
| `references/estado-yml-schema.md` | Esquema del archivo de estado por materia |
| `assets/plantilla-oficial-extraida.txt` | Texto completo de la plantilla oficial (fuente original, trazabilidad) |
| `assets/logo-utn-tup.jpg` | Logo institucional UTN/TUP, extraído de un TP real de cátedra, usado en el membrete del PDF |
