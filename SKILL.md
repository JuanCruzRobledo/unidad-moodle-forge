---
name: unidad-moodle-forge
description: >-
  Genera el material didactico completo de una unidad para el aula virtual Moodle de TUP (tup.sied.utn.edu.ar) a partir del programa de la materia o apuntes: un archivo HTML por cada bloque real de cada sub-seccion (Introduccion, Actividades, Practica, Microteaching, Autoevaluacion, Encuesta de cierre) -nunca un unico HTML con varios bloques pegados-, preguntas en formato XML de Moodle para importar (5 por actividad, 10 en autoevaluacion), guiones para generar los Notebooks LM de cada actividad, la consigna y el PDF del Trabajo Practico Integrador, y -al final del proceso- el material de Evaluaciones (parciales/recuperatorios) a nivel curso. Ademas, bajo pedido explicito del usuario y con confirmacion previa, puede IMPORTAR ese material al aula real de Moodle via browser automation (crear/editar secciones, Labels, Cuestionarios, Tareas y Encuestas) dejando un reporte de pendientes/incoherencias al terminar. Usa esta skill SIEMPRE que el usuario pida armar/generar el material de una unidad para el campus/aula virtual, o subir/importar ese material ya generado al aula real: 'arma la unidad 3 de Programacion 3', 'genera el contenido Moodle de la unidad de CSS', 'necesito las preguntas XML y el HTML de la actividad 2', 'hace el TP integrador y su PDF', 'segui armando el material donde quedo', 'importa la unidad 2 al aula real', 'subi este material a Moodle' -aunque no nombre la skill. Mantiene un archivo de estado (estado.yml) por materia para retomar la generacion (y la importacion) unidad por unidad y saber que falta. NO usar para corregir entregas de alumnos (corregir/corregir-notas-planilla), ni para responder consultas en el campus (responder-alumnos), ni para generar informes de pendientes (informe-pendientes-curso).
license: Apache-2.0
---

# Unidad Moodle Forge

Convierte el programa de una materia (o los apuntes que le pases) en el material completo de una unidad del aula virtual, calcando la estructura real del campus TUP: no la que "se supone" que tiene una unidad, sino la que confirmamos recorriéndolo en vivo. El principio que ordena todo: **generar es barato, pero publicar contenido pedagógico mal fundamentado es caro** — por eso cada bloque parte de material real que aportó el usuario (nunca se inventan resultados de aprendizaje o consignas de la nada), y los pasos irreversibles o que dependen de una herramienta externa (PDF, NotebookLM) esperan confirmación explícita antes de ejecutarse.

## Cuándo aplica

El usuario es docente/tutor de una materia en el campus TUP y quiere producir el contenido de una unidad completa (o retomar una a medio hacer) a partir de: el programa de la materia, apuntes propios, un PDF de cátedra, o simplemente el nombre del tema. No tiene por qué traer todo listo — puede pedir "armá la unidad 2 de CSS" y vos completás con el patrón ya validado contra el aula real, pidiendo solo lo que no se pueda derivar razonablemente (ej. el tema puntual de cada actividad si no lo aportó).

## Workflow — 7 fases + 2 extensiones opcionales

```
0. Relevar estado     → qué unidad/sub-sección falta (lee estado.yml)
1. Introducción       → 4 HTML separados: 00-descripcion-seccion, video, banner-foro, hoja-de-ruta
2. Actividades        → 00-descripcion-seccion + por actividad: actividad-N.html + cuestionario-actividad-N.html
                         + XML (5 preguntas c/u) + guion NotebookLM
3. Práctica (TP)      → documento PDF con membrete *bajo aprobación* → entrega HTML → consigna HTML (+ 00-descripcion-seccion)
4. Microteaching      → 3 HTML separados: 00-descripcion-seccion, tarjeta intro, contenido+enlaces
5. Autoevaluación     → 2 HTML separados (00-descripcion-seccion + descripción) + XML (10 preguntas)
6. Encuesta de cierre → 2 HTML separados (00-descripcion-seccion + descripción)
7. (final, opcional)  → Evaluaciones y Trabajo Práctico Integrador (curso-level)
8. (opcional, bajo pedido explícito) → Importación del material generado al aula real de Moodle
```

Las fases 1 a 6 son por unidad y se repiten unidad tras unidad. La fase 7 es **aparte**:
solo se dispara cuando el usuario la pide explícitamente y después de que las
unidades estén encaminadas — no se mezcla con el material de unidad porque vive en
secciones de curso distintas (`Evaluaciones` y `Trabajo Practico Integrador`, no
`Autoevaluación` ni `Práctica`). La fase 8 es **todavía más aparte**: opera sobre
material que ya está `generado`/`confirmado` en el filesystem y lo sube al aula real
vía browser automation — nunca se dispara sola, siempre bajo pedido explícito del
usuario y después de pasar las precondiciones de seguridad (ver Fase 8).

**Regla de generación que aplica a las Fases 1-6**: nunca generes un único HTML con
varios bloques (`<div>`) de nivel superior pegados uno atrás del otro. Cada bloque de
`references/plantillas-html.md` es un componente independiente en Moodle (una
sección/sub-sección, un Label, o la descripción de un cuestionario) — generalo como
su propio archivo, siguiendo el nombre que indica esa referencia junto a cada bloque
(`→`). Esto no es un capricho de organización: así es como se mapea 1:1 contra el
aula real (ver `references/estructura-aula-real.md`), y es lo que la Fase 8 necesita
para poder pegar cada archivo en el lugar correcto sin tener que adivinar dónde corta
un bloque y empieza el siguiente.

**Nunca generes el PDF de la Práctica sin que el usuario haya confirmado antes que el documento (`documento-practica.html`) está bien.** El PDF es una conversión fiel de ese documento (no un HTML aparte que puede quedar desincronizado) — generarlo antes de la confirmación duplica el trabajo si el documento cambia. Este documento **no es** el bloque `consigna-practica.html` que va en la página de Moodle — son dos archivos distintos, ver Fase 3.

## Fase 0 — Relevar estado

Antes de escribir nada, buscá `estado.yml` en la raíz de la carpeta de la materia (ver esquema completo en `references/estado-yml-schema.md`). Si no existe, es la primera unidad: creala con `scripts/scaffold_unidad.py`. Si existe, leelo para saber qué sub-secciones de qué unidad ya están `generado`, `confirmado` o `pendiente` — así no repetís trabajo ni perdés el hilo entre sesiones. Preguntale al usuario solo por lo que el estado no resuelve (ej. "¿confirmás que el HTML de la Práctica quedó bien para generar el PDF?").

**Heurística de clasificación (por texto, sin necesidad de scrapear nada en cada corrida)**: al leer el programa de la materia, cada unidad/bloque cae en uno de tres destinos según su título u objetivo:

- Contiene "Evaluación Integradora", "Examen", "Parcial" → va a la pestaña **Evaluaciones** (Fase 7, `references/plantilla-evaluacion.md`).
- Contiene "Proyecto Integrador", "Trabajo Integrador", "Defensa Final" → va a la pestaña **Trabajo Práctico Integrador** (Fase 7, `references/plantilla-tpi-standalone.md`).
- Todo lo demás → flujo normal de unidad (Fases 1-6).

Esto es puro análisis del texto del programa — no requiere volver a recorrer el aula real cada vez que arranca una unidad nueva.

## Fase 1 — Introducción de la unidad

Es la página raíz de la sección de la unidad en Moodle (no una sub-sección aparte — así es como vive en el aula real). Generá los **4 bloques de `references/plantillas-html.md` § Introducción como 4 archivos separados** dentro de `Introduccion/`, en este orden:

1. `00-descripcion-seccion.html` — banner con resultados de aprendizaje (completá 3-5 resultados concretos a partir del material que trajo el usuario). Es la Descripción de la sección raíz de la unidad, no un Label.
2. `01-video-introduccion.html` — video colapsable (dejá `URL_DEL_VIDEO_YOUTUBE` como placeholder si no hay video todavía).
3. `02-banner-foro.html` — sección con link al foro de la unidad.
4. `03-hoja-de-ruta.html` — hoja de ruta con la tabla de tiempos Pomodoro (la tabla de tiempos se completa recién al final, cuando ya generaste todas las actividades y sabés cuántos minutos estimar).

## Fase 2 — Actividades

Generá `Actividades/00-descripcion-seccion.html` una sola vez por unidad (`references/plantillas-html.md` § Banner principal de la sección de Actividades) — es la Descripción de la sub-sección, no un Label.

Por cada actividad (normalmente 3-4, confirmá la cantidad con el usuario si no la trajo), generá **dos archivos separados**, no uno solo:

1. `Actividades/actividad-N/actividad-N.html` — el bloque `<details>` (`references/plantillas-html.md` § Cuerpo para cada actividad) con sus 3 tarjetas (Infografía con modal+script, Lectura PDF, Asistente IA). Este es el Label de la actividad — **no le pegues el bloque de Cuestionario abajo**, va aparte (siguiente punto).
2. `Actividades/actividad-N/cuestionario-actividad-N.html` — el bloque "Cuestionario de la Actividad" (`references/plantillas-html.md` § Descripción para cada cuestionario). No es un Label: es el contenido que va en el campo Descripción del `mod_quiz` de esa actividad.

Generá también el XML de exactamente 5 preguntas para importar al banco de Moodle (`scripts/generar_pregunta_xml.py` + `references/formato-preguntas-moodle-xml.md`; seguí la convención de códigos de pregunta vista en el aula real, ej. `TEMA 1`.. `TEMA 5`). Generá también el guion de NotebookLM (`references/notebooklm-guion.md`) — **nunca crees el notebook vos**: NotebookLM no tiene API pública, así que tu entregable es el guion/fuente listo para pegar, y el link de la tarjeta queda como placeholder hasta que el usuario lo suba a mano y te devuelva la URL real.

Si el tema se presta, sumá una Actividad Lúdica como `Actividades/actividad-ludica.html` (mismo archivo de referencia, bloque separado, un único Label — no trae Cuestionario aparte) — es opcional, no todas las unidades la tienen.

## Fase 3 — Práctica / Trabajo Práctico

Acá se generan **cuatro archivos distintos**, no uno solo, y **en este orden** — no es
arbitrario: el formato de entrega (punto 3) describe qué se entrega, y eso recién se
sabe con precisión una vez que la consigna completa (punto 2) está escrita; el
resumen para la página de Moodle (punto 4) linkea al PDF ya generado, así que
necesita que el PDF ya exista.

0. **`Practica/00-descripcion-seccion.html`** — el banner "Trabajo Práctico – [Unidad]" (`references/plantillas-html.md` § Banner principal de la sección). Es la Descripción de la sub-sección Práctica, no un Label — podés generarlo apenas sepas el nombre de la unidad, no depende de los otros tres.
1. **`documento-practica.html`** — PRIMERO. El documento completo con membrete institucional que el alumno descarga como PDF desde la pestaña Práctica. Es un documento sobrio (sin tarjetas ni degradés del resto del aula), con estructura tipo TP real de cátedra: Objetivo general, Marco teórico (opcional), y el cuerpo de la consigna — que puede ser un **Caso Práctico** con pasos numerados (TP de código/procedimental), **preguntas de análisis por sección temática** (TP de reflexión/teoría), o una combinación de ambos según lo que pida el TP real — cerrando con Consideraciones y Conclusiones esperadas. Ver `references/plantilla-pdf-practica.md` para la plantilla completa y cuándo usar cada bloque. Mostraselo al usuario y **esperá su confirmación explícita antes de correr `scripts/render_pdf.py`** sobre ese archivo, pasando `--materia "<nombre de la materia>"` para que agregue el membrete (logo UTN + institución en el encabezado, barra de color + número de página en el pie, repetidos en cada hoja vía `header_template`/`footer_template` de Playwright — no se duplican a mano en el HTML). Recién ahí generás el PDF fiel. Actualizá `estado.yml` marcando `documento_html_status` y, tras la confirmación, `pdf_status` como generado.
2. **`entrega-practica.html`** — SEGUNDO, ya con la consigna confirmada a mano. El bloque de formato de entrega, usando la variante correcta según la carrera/materia: Python de archivo único (Programación 1), o estructura de paquetes en Java (Programación 2/3) — las 3 variantes están en `references/plantillas-html.md` § Trabajo Práctico. Necesita la consigna ya escrita porque describe qué archivo(s) exactos entrega el alumno (nombre del TP, cantidad de fichas/archivos, etc.), no se puede redactar bien antes. Este archivo va en la Descripción de la Tarea (`mod_assign`) de entrega.
3. **`consigna-practica.html`** — TERCERO. El bloque `<details>` que va en la página de Moodle (resumen breve del TP) — **solo ese `<details>`, sin el banner** (el banner ya salió aparte en el punto 0). Con el documento PDF (punto 1) ya generado, este bloque es un resumen corto con un link de descarga al PDF, no la letra completa del TP. Es un Label independiente.

## Fase 4 — Microteaching

Generá los **3 bloques de `references/plantillas-html.md` § Microteaching como 3 archivos separados** dentro de `Microteaching/`:

1. `00-descripcion-seccion.html` — banner de la sub-sección (Descripción, no Label).
2. `01-material-microteaching.html` — tarjeta introductoria ("Material de la Microteaching").
3. `02-contenido-enlaces.html` — contenido con el link al video de microteaching y al repositorio de código si aplica.

Es la sección más liviana — no tiene NotebookLM ni preguntas.

## Fase 5 — Autoevaluación

Generá `Autoevaluacion/00-descripcion-seccion.html` (banner, Descripción de la sub-sección) y `Autoevaluacion/01-autoevaluacion.html` (descripción del cuestionario, Label — casi fija entre unidades, solo cambia el nombre de la unidad) como **dos archivos separados**. Mismo patrón que Actividades para las preguntas, pero con **exactamente 10 preguntas** en el XML (`scripts/generar_pregunta_xml.py`), reutilizando o extendiendo el banco de preguntas de las actividades de la misma unidad (en el aula real comparten banco: los códigos de autoevaluación son un superset de los de actividades).

## Fase 6 — Encuesta de cierre

Generá `EncuestaCierre/00-descripcion-seccion.html` (banner, Descripción de la sub-sección) y `EncuestaCierre/01-encuesta-cierre.html` (descripción de la encuesta, va en la Descripción del `mod_feedback` existente) como **dos archivos separados** — el contenido no cambia entre unidades salvo el nombre de la unidad en el banner. No hace falta pedirle nada al usuario acá.

## Fase 7 — Evaluaciones y Trabajo Práctico Integrador (curso-level, opcional y al final)

Solo si el usuario la pide explícitamente, o si la heurística de clasificación de
Fase 0 detectó una unidad/bloque que corresponde a alguna de las dos. Viven fuera
de la carpeta de unidades (son secciones de curso aparte) — no las generes de
oficio ni las mezcles con el material de unidad. Documentá su propio estado en
`estado.yml` bajo las claves separadas `evaluaciones_curso` y
`trabajo_practico_integrador` (ver `references/estado-yml-schema.md`).

Las dos siguen el mismo flujo mínimo de 3 pasos, con su propia plantilla:

1. **Consigna → PDF con membrete.** Escribí el documento completo
   (`documento-tpi.html` o `documento-evaluacion-<nombre>.html`), mostraselo al
   usuario, y **recién con su confirmación explícita** corré
   `scripts/render_pdf.py --materia "<materia>"` — mismo mecanismo y misma
   regla dura que la Práctica de unidad (`plantilla-pdf-practica.md`). Nunca
   generes el PDF sin ese OK.
2. **Presentación en Moodle.** El bloque HTML que va en la página de la
   sección: banner + tarjeta de descarga con link al PDF ya generado (+ tabla
   de fechas de examen si es Evaluaciones). Ver plantillas abajo.
3. **Entrega / certificado / foro.** La tarjeta de descripción del `assign` de
   entrega (con las reglas de formato), y la nota de que el certificado (si
   aplica) es un módulo nativo del LMS gateado a que esa entrega esté marcada
   como realizada — no HTML que redacte la cátedra. El foro de consultas es
   nativo, sin HTML propio.

**Evaluaciones** (parciales, recuperatorios, Integrador de nota): usá
`references/plantilla-evaluacion.md`. Modela una instancia canónica
(consigna → tarjeta "Importante" con video de referencia opcional → entrega →
certificado gateado → foro) que se clona por cada parcial real de la materia —
no le agregues variantes por mesa de examen/grupo salvo que el usuario las pida.

**Trabajo Práctico Integrador** (proyecto final del curso): usá
`references/plantilla-tpi-standalone.md`. Mismo espíritu que la Práctica de
unidad pero a escala de curso: consigna completa en PDF, bloque de "Método de
Entrega" separado de la consigna, y foro/rúbrica nativos sin HTML propio.

Ambas plantillas están contrastadas contra HTML real relevado en vivo (curso
Programación 3, TUP) — ver `assets/tpi-evaluaciones-html-real.txt` para el
detalle completo, incluida la sección de qué se descartó a propósito (variantes
por mesa de examen, recursos específicos de una materia, contenido legacy sin
estilo) para no confundir ruido operativo real con el estándar a replicar.

## Fase 8 — Importación al aula real de Moodle (opcional, bajo pedido explícito)

**Nunca se dispara sola.** Solo arranca cuando el usuario pide explícitamente subir/
importar/publicar el material ya generado en el aula real ("importá la unidad 2",
"subí esto a Moodle", "quiero que el aula quede tal cual el material"). No es un
paso automático al final de las Fases 1-7 — el material queda en el filesystem hasta
que el usuario pide este paso aparte.

No hay atajo de API real para esto (Moodle no expone un endpoint que arme
secciones/Labels/Cuestionarios de punta a punta — ver la investigación del propio
workspace del usuario si la tiene, típicamente `INVESTIGACION-API-MOODLE.md`), así
que la Fase 8 opera por **browser automation** (Claude in Chrome) sobre la sesión ya
logueada del usuario en Moodle, replicando los atajos de URL/JS confirmados en
`references/importacion-moodle.md`. Cargá esa referencia completa antes de tocar
nada — tiene el detalle técnico de cada paso; acá va solo el orden y las
precondiciones.

### Precondiciones obligatorias — cortar si alguna no se cumple

No avances con NINGUNA acción de escritura sobre el aula hasta tener las 5:

1. **Pedí la URL exacta del curso** a modificar. Nunca la asumas ni la adivines a
   partir de conversaciones previas — un aula equivocada es contenido real de otra
   materia/comisión pisado por error.
2. **Confirmá explícitamente con el usuario que su cuenta tiene rol de gestor/editor**
   (Teacher con permisos de edición) en ese curso. La skill no puede verificar
   permisos por API — se lo preguntás y tomás su palabra, pero si en la práctica no
   aparece el botón "Activar edición" o similar, cortá y avisá en vez de forzar.
3. **Avisá EXPLÍCITAMENTE, en texto claro, antes de tocar nada**: esta acción
   MODIFICA EL AULA REAL — crea, edita, oculta y potencialmente borra contenido
   existente. Moodle no tiene un "deshacer" real más allá de logs/papelera que no
   siempre alcanza. Pedí una confirmación explícita del usuario ("sí, dale" /
   "confirmo") antes de arrancar. Si existe un curso de prueba/sandbox (el usuario
   suele tener uno, ej. un `campustest` documentado en su propia bitácora de
   importación del workspace), **recomendá practicar ahí primero** antes de tocar el
   curso de producción real — no lo exijas si el usuario ya lo descartó, pero
   ofrecelo.
4. **Confirmá el mapeo explícito** unidad-local ↔ sección-real: qué carpeta local
   (`Unidad N - <Nombre>/`) corresponde a qué `section=N` del curso. Nunca lo
   asumas por orden numérico/alfabético sin chequear contra el nombre real de la
   sección en el curso.
5. **Relevá la estructura real ANTES de tocar nada**: contá los módulos reales de
   cada sub-sección a importar (técnica de `fetch` + regex de
   `id="module-(\d+)"`, ver `references/importacion-moodle.md`) para detectar de
   entrada contenido duplicado u otras sorpresas, y decidí junto al usuario qué
   hacer si aparece algo inesperado — no asumas.

### Reglas duras específicas de esta fase

- **Nunca toques ni borres una copia "roja" de referencia** si el curso usa esa
  convención (copia editable + copia de referencia que el usuario duplica a mano
  más adelante). Si no está claro cuál copia es cuál, preguntá antes de tocar nada.
- **Preferí OCULTAR antes que BORRAR** contenido del curso sin equivalente en el
  material generado — nunca borres de una sin confirmación explícita.
- **Nunca asumas qué hacer ante contenido duplicado.** Preguntá la primera vez que
  aparezca en una unidad; una vez que el usuario define el criterio para un caso
  (expandir plantilla vs. contenido único), aplicalo consistentemente al resto sin
  volver a preguntar por cada sub-sección.
- **Pegá HTML siempre vía `tinymce.get('<id>').setContent(html)`**, nunca tipeando
  en el diálogo "Código fuente" del editor (el auto-cierre de etiquetas corrompe el
  HTML). Verificá el id del editor correcto antes de setear contenido en
  formularios con 2+ editores TinyMCE en la misma página (Tarea: `id_introeditor`
  vs `id_activityeditor`; Encuesta: `id_introeditor` vs
  `id_page_after_submit_editor`) — nunca asumas `tinymce.activeEditor`.
- El archivo `00-descripcion-seccion.html` de cada sub-sección (Fases 1-6) va al
  campo Descripción de esa sección (`course/editsection.php`), **no a un Label**.
- El archivo `cuestionario-actividad-N.html` de cada actividad va a la Descripción
  del `mod_quiz` correspondiente (con "Mostrar descripción en la página del curso"
  activado), **no al Label de la actividad**.
- **Nunca subas ni generes el PDF de la Práctica sin que `estado.yml` ya tenga
  `pdf_confirmado_por_usuario: true`** para esa unidad — si no está, cortá esa
  sub-sección y pedí la confirmación antes de seguir.
- Los placeholders sin resolver (`URL_...`) se suben tal cual, no se inventan
  valores para completarlos — quedan documentados en el reporte final.
- **Nunca saques el widget de infografía (botón + modal + `<script>`) del HTML de
  una actividad al pegarlo.** Aunque Moodle elimine el `<script>` al guardar el
  Label (lo hace, es esperado), el bloque va completo tal cual — lo único que suele
  faltar de verdad es la imagen (`URL_IMAGEN_INFOGRAFIA`), y eso se anota en el
  reporte como pendiente, no se resuelve borrando el widget.
- **Si te trabás con algo que el browser automation no resuelve fácil** (un editor
  que reescribe el HTML al pegarlo, un modal que no carga, un check de "cambios sin
  guardar" que no cierra), **avisá y pedí una mano al usuario en vez de forzar un
  intento a ciegas contra el aula real** — no reintentes la misma acción en loop.
- **No asumas la configuración de los Cuestionarios** (intentos permitidos, nota
  para aprobar) — si el usuario ya definió un criterio para esa materia (ej. "90% para
  aprobar Autoevaluación"), aplicalo; si no lo definió, dejá los valores por defecto
  de Moodle y confirmá con el usuario en vez de inventar un número.

### Flujo

1. Precondiciones (arriba) — no sigas sin las 5.
2. Releé `estado.yml` de la unidad a importar. Solo se importan sub-secciones que
   estén `confirmado` (o `generado` con un OK explícito del usuario en el momento,
   si todavía no llegaron a `confirmado`).
3. Por cada sub-sección de la unidad, en orden (Introducción/raíz → Actividades →
   Práctica → Microteaching → Autoevaluación → Encuesta de cierre): pegá
   `00-descripcion-seccion.html` en el campo Descripción de esa sección; creá o
   editá un Label por cada `NN-*.html` restante, en el mismo orden en que están
   numerados; para Actividades, creá/editá el `mod_quiz` de cada actividad,
   importá sus 5 preguntas del XML correspondiente (`question/bank/importquestions/
   import.php`) y pegá `cuestionario-actividad-N.html` en su Descripción; para
   Práctica, subí `documento-practica.pdf` como Archivo, pegá `consigna-practica.html`
   en el Label que lo describe y `entrega-practica.html` en la Descripción de la
   Tarea; para Autoevaluación, creá/editá el `mod_quiz` e importá las 10 preguntas;
   para Encuesta de cierre, editá la encuesta (`mod_feedback`) existente sin tocar
   sus preguntas propias.
4. Confirmá visualmente cada sub-sección contra el material fuente antes de pasar a
   la siguiente.
5. Al terminar toda la unidad — o al cortar por cualquier motivo (bloqueo, falta de
   confirmación, error irrecuperable) — generá el reporte (siguiente punto). Nunca
   termines una corrida de importación sin dejarlo, aunque haya quedado a mitad de
   camino.

### Reporte final (obligatorio, no opcional)

Usá `references/plantilla-reporte-importacion.md`, completala y guardala como
`reporte-importacion.md` en la **raíz de la carpeta de la unidad importada** (ej.
`Metodologia I/Unidad 1 - Marco funcional/reporte-importacion.md`) — si ya existe uno
de una corrida anterior, actualizalo en vez de perder el historial. Tiene que listar,
como mínimo: qué sub-secciones se importaron y cuáles quedaron pendientes/cortadas;
todo placeholder sin resolver que quedó en el aula (links, videos, PDFs, imágenes de
banner/infografía); carpetas o recursos dejados vacíos u ocultos a propósito, con el
motivo (ej. "Material de apoyo – Actividad 2 (pendiente)" sin archivos porque la
skill no generó ninguno para ese lugar); incoherencias detectadas entre el material
local y el estado real del curso (contenido duplicado, nombres que no coinciden,
módulos del template viejo sin equivalente); y una lista de próximos pasos para el
usuario. Actualizá también el bloque `importacion` de esa unidad en `estado.yml`
(ver `references/estado-yml-schema.md`).

## Reglas duras

- **Nunca inventes contenido pedagógico de la nada.** Resultados de aprendizaje, consignas y preguntas siempre parten del material que aportó el usuario (programa, apuntes, PDFs). Si falta información concreta, preguntala — no rellenes con genérico solo para completar la plantilla.
- **Fidelidad 1:1 con la plantilla oficial.** El prompt oficial del PDF de plantillas es explícito: "reescribí el contenido respetando exactamente su estructura, estilos e IDs, sin eliminar, resumir ni fusionar información". Aplicá esa misma regla vos: no simplifiques ni fusiones bloques de la plantilla al completarlos.
- **La estructura de tabs/carpetas calca la jerarquía real confirmada**, no la que se asume a priori — 5 sub-secciones hijas (Actividades, Práctica, Microteaching, Autoevaluación, Encuesta de cierre) más la Introducción viviendo en la raíz de la unidad. Ver `references/estructura-aula-real.md` para el detalle y las inconsistencias reales que NO hay que replicar.
- **NotebookLM nunca se automatiza.** Entregable = guion fuente, nunca un link inventado.
- **El PDF de la Práctica nunca se genera sin aprobación explícita del documento (`documento-practica.html`)** que lo origina.
- **El PDF de la Práctica no es una captura de la página de Moodle.** Es un documento con membrete institucional (ver `references/plantilla-pdf-practica.md`), no el HTML con tarjetas/degradés de `consigna-practica.html`.
- **Nunca generes un HTML con varios bloques de nivel superior pegados.** Cada bloque de `references/plantillas-html.md` (Descripción de sección, Label, Descripción de Cuestionario) es un archivo propio — ver la regla de generación al inicio del Workflow y el `→` junto a cada bloque de esa referencia.
- **La Fase 8 (Importación) nunca arranca sin las 5 precondiciones** (URL del curso, rol de gestor confirmado, aviso explícito de que es una acción riesgosa/difícil de revertir + confirmación del usuario, mapeo unidad↔sección confirmado, conteo de módulos reales antes de tocar nada) y **nunca termina sin dejar `reporte-importacion.md`**, aunque se corte a mitad de camino.

## Componentes de la skill

| Archivo | Para qué |
|---|---|
| `scripts/scaffold_unidad.py` | Crea la carpeta de una unidad nueva (6 sub-carpetas) y crea/actualiza `estado.yml` en la raíz de la materia |
| `scripts/generar_pregunta_xml.py` | Convierte un YAML simple de preguntas a XML de Moodle importable |
| `scripts/render_pdf.py` | Convierte un HTML ya confirmado a PDF fiel (Playwright + Chromium); con `--materia` agrega membrete institucional (header/footer repetidos) |
| `references/plantillas-html.md` | Los bloques HTML oficiales de cada sub-sección, listos para completar |
| `references/plantilla-pdf-practica.md` | Plantilla del documento con membrete que se convierte en el PDF descargable de la Práctica |
| `references/plantilla-tpi-standalone.md` | Plantilla curso-level del Trabajo Práctico Integrador (Fase 7) |
| `references/plantilla-evaluacion.md` | Plantilla curso-level de Evaluaciones — parciales/recuperatorios (Fase 7) |
| `references/estructura-aula-real.md` | Jerarquía real confirmada del aula + inconsistencias a no replicar |
| `references/importacion-moodle.md` | Fase 8: técnicas de browser automation confirmadas, checklist de precondiciones y reglas duras para importar al aula real |
| `references/plantilla-reporte-importacion.md` | Plantilla del reporte de pendientes/incoherencias que deja la Fase 8 en la carpeta de la unidad |
| `references/formato-preguntas-moodle-xml.md` | Schema de pregunta Moodle XML + convención de códigos |
| `references/notebooklm-guion.md` | Spec de configuración de NotebookLM por tipo de material + plantilla de guion |
| `references/estado-yml-schema.md` | Esquema del archivo de estado por materia |
| `assets/plantilla-oficial-extraida.txt` | Texto completo de la plantilla oficial (fuente original, trazabilidad) |
| `assets/tpi-evaluaciones-html-real.txt` | HTML real relevado en vivo para TPI y Evaluaciones curso-level, con notas de qué NO replicar |
| `assets/logo-utn-tup.jpg` | Logo institucional UTN/TUP, extraído de un TP real de cátedra, usado en el membrete del PDF |
