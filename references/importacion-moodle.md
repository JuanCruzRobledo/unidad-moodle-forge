# Importación al aula real de Moodle — técnicas confirmadas (Fase 8)

Esta referencia consolida lo que se confirmó operando en vivo contra un curso real
de Moodle (TUP, tema del curso con tabs por sección) vía browser automation. No hay
atajo de API limpio para armar secciones/Labels/Cuestionarios de punta a punta —
Moodle no expone ese endpoint — así que todo esto pasa por la UI, con atajos de
URL/JS que ahorran clics. Cargá esta referencia completa antes de arrancar la Fase 8
de `SKILL.md` (que tiene las precondiciones y el checklist de seguridad).

## 0. No hay atajo de API — es 100% UI por dentro

Confirmado: no existe un endpoint de la API REST de Moodle que cree una sección
completa con sus Labels/Cuestionarios/Tareas de una sola llamada. Todo lo de acá
abajo son atajos de **URL directa** o **JavaScript en la página ya cargada**
(`javascript_tool`), no llamadas a un servicio — seguís operando dentro de la sesión
logueada del usuario en el navegador.

## 1. Relevar la estructura real antes de tocar nada

Cada sub-sección de una unidad (Inicio/raíz, Actividades, Práctica, Microteaching,
Autoevaluación, Encuesta de cierre) es una **sección nativa de Moodle**
(`course/view.php?id=<courseid>&section=N`), no un tab renderizado en una sola
página. Antes de editar cualquiera, contá cuántos módulos reales tiene:

```js
fetch('/course/view.php?id=<courseid>&section=<N>', {credentials:'same-origin'})
  .then(t => t.text())
  .then(html => [...html.matchAll(/id="module-(\d+)"/g)].map(m => m[1]))
```

Si el número es sospechosamente el doble de lo esperado, es un bug de contenido
duplicado (pasó en una corrida real al reciclar la unidad de otra materia como base)
— no asumas cuál copia es la buena, preguntale al usuario. Una vez que define el
criterio para un caso (expandir plantilla existente vs. contenido único a
reemplazar), aplicalo consistentemente al resto de esa unidad sin volver a
preguntar.

**El PRIMER bloque de cada sub-sección casi siempre NO es un Label** — es el campo
**Descripción** (resumen) de la SECCIÓN misma, editable en
`course/editsection.php?id=<id-de-sección>`, no un módulo aparte. Se nota porque al
abrir el ⋮ de ese primer bloque aparecen opciones de sección ("Editar ajustes" →
lleva a `editsection.php`, "Destacar", "Ocultar tema", "Duplicar" el tema entero) en
vez de opciones de actividad ("Asignar roles", etc.). Esto es exactamente lo que la
convención de generación de `references/plantillas-html.md` ya separa como
`00-descripcion-seccion.html` — pegalo ahí, no en un Label.

También es común que el título/descripción de un módulo real (Archivo, Tarea,
Encuesta) se muestre expandido como una cajita debajo del nombre — es su propio
campo "Descripción" con "Mostrar descripción en la página del curso" activado, **no**
un Label separado. Antes de asumir que hay un Label extra, contá los módulos reales
con el `fetch` de arriba.

Para encontrar el id de sección desde su URL:

```js
const res = await fetch('/course/view.php?id=<courseid>&section=<N>', {credentials:'same-origin'});
const id = (await res.text()).match(/editsection\.php\?id=(\d+)/)[1];
// después: course/editsection.php?id=<id>&sr=1
```

## 2. Pegar HTML sin romperlo

El diálogo "Código fuente" del editor TinyMCE tiene auto-cierre de etiquetas —
tipear ahí con el `type` del navegador duplica y corrompe los tags de cierre. Usá
`javascript_tool` para setear el contenido directo:

```js
tinymce.get('<id_del_editor>').setContent(htmlString);
document.querySelector('input[name="submitbutton2"]').click(); // módulos (Label, Quiz, etc.)
// o input[name="submitbutton"] para editsection.php (secciones)
```

Verificá el largo con `tinymce.get('<id>').getContent().length` después de setear,
antes de guardar, para confirmar que entró completo.

**¡Ojo con `tinymce.activeEditor`!** Sirve cuando el formulario tiene un solo editor
(Labels, resúmenes de sección, banner de Foro). Pero **algunos módulos tienen 2+
editores TinyMCE en la misma página** y `activeEditor` puede apuntar al que NO se ve
en el curso:

- `mod_assign` (Tarea): `id_introeditor` = Descripción (la que se muestra en el
  curso) + `id_activityeditor` = "Instrucciones de la actividad" (NO se muestra por
  defecto). Si el contenido nuevo va a `id_activityeditor` por error, el curso sigue
  mostrando el texto viejo.
- `mod_feedback` (Encuesta): `id_introeditor` (Descripción, visible) +
  `id_page_after_submit_editor` (mensaje post-envío, no tocar).

Antes de usar `setContent`, corré `JSON.stringify(tinymce.get().map(e => e.id))` y
seteá el id correcto a mano — nunca asumas `activeEditor`.

## 3. Crear módulos nuevos: dos formas, elegí según el caso

**a) Duplicar + editar** — cuando ya existe una actividad de ejemplo en la
sub-sección (típico en cursos reciclados de otra unidad/materia como base): menú ⋮
de esa actividad → "Duplicar" → editá la copia (nombre + contenido) en vez de crear
desde cero. Es la forma más rápida de clonar la estructura de la Actividad 1 hacia
la 2, 3, etc. cuando el patrón ya está armado en el curso.

**b) URL directa** — cuando no hay nada que duplicar (sub-sección vacía, o el tipo
de módulo no existe todavía en esa sección):

```
course/modedit.php?add=<tipo>&type=&course=<courseid>&section=<N>&return=0&sr=0
```

Tipos útiles: `label` (Área de texto y medios, para cada `NN-*.html`), `quiz`
(Cuestionario de actividad/autoevaluación), `resource` (Archivo, ej. el PDF de
Práctica), `assign` (Tarea de entrega).

## 4. Importar preguntas XML a un Cuestionario

Flujo completo, repetible por cada actividad y por Autoevaluación:

1. `question/bank/importquestions/import.php?courseid=<courseid>&cmid=<quizcmid>`
2. Click radio **"Formato Moodle XML"**.
3. Click "Seleccione un archivo..." → se abre el selector de Moodle → tab **"Subir
   un archivo"** → usar `file_upload` sobre el input `type=file` real (buscarlo con
   `find`; el primer resultado a veces es un botón decorativo, no el input) →
   "Subir este archivo".
4. Click **"Importar"** — Moodle muestra una confirmación con el enunciado de cada
   pregunta importada (buena señal para verificar que coincide con el XML antes de
   seguir) → "Continuar".
5. Esto crea una **categoría de preguntas nueva** en el banco, con el nombre literal
   del `<question type="category"><text>$course$/top/.../NOMBRE</text>` del XML
   (ej. "Actividad 1", "Autoevaluacion"). Anotá ese nombre — lo necesitás en el
   siguiente paso.

Agregar las preguntas importadas al Cuestionario, en
`mod/quiz/edit.php?cmid=<id>` → "Agregar" → "del banco de preguntas" → en el combo
de categoría **escribir el nombre exacto de la categoría del paso anterior**, NO
quedarse con el filtro por defecto ("Por defecto en <nombre del cuestionario>" está
casi siempre vacío, es autogenerado y no tiene nada que ver). El combo muestra el
conteo entre paréntesis (ej. "Autoevaluacion (10)") — confirmá que coincide con lo
esperado (5 en actividades, 10 en autoevaluación) antes de seleccionar. A veces hay
que clickear "Aplicar filtros" **dos veces** para que la tabla termine de renderizar.
Tildá el checkbox de cabecera para seleccionar todas, "Añadir preguntas
seleccionadas para el cuestionario".

## 5. Reordenar y borrar

**Reordenar** dentro de una sub-sección: ⋮ → "Mover" abre "Mover actividad ...
después de:" con la lista completa de items — clickear el item después del cual se
quiere insertar. Sirve para intercalar (ej. mover cada Cuestionario recién creado,
que Moodle agrega al final de la sección, justo después de su Label/Carpeta
correspondiente).

**Borrar módulos en lote** (solo cuando ya está confirmado con el usuario que
corresponde borrar, no ocultar):

```js
const sesskey = M.cfg.sesskey;
for (const id of [<ids-a-borrar>]) {
  await fetch(`/course/mod.php?sesskey=${sesskey}&delete=${id}&confirm=1&sr=0`, {credentials:'same-origin'});
}
```

Ojo: una verificación GET aislada e inmediata sobre un id ya borrado puede devolver
una página que contiene la palabra "confirm" en el HTML aunque el borrado ya se haya
efectuado — no dejarse engañar por eso, verificar con un `fetch` limpio de la lista
de `module-` ids después. La alternativa 100% confiable es la UI: ⋮ → "Borrar" →
confirmar el modal "¿Eliminar actividad?" → "Borrar" (esto sí requiere clic real, no
hay atajo de URL que muestre el modal).

**Ocultar en vez de borrar** (criterio por defecto para contenido sin equivalente en
el material generado, ver Fase 8 de `SKILL.md`): usar el ⋮ → "Ocultar" del módulo,
no `mod.php?delete=`.

## 6. Renombrar rápido

El ícono de lápiz "Editar título" al lado del nombre de cualquier actividad (Foro,
Carpeta, etc.) permite edición inline: clic → Ctrl+A → escribir → Enter. Más rápido
que abrir el formulario completo cuando solo hay que cambiar el nombre.

## 7. Convención de "copia editable + copia roja de referencia"

Algunos cursos (reciclados de otra unidad/materia como base) dejan, por cada
sub-sección que se va a expandir con más actividades, **dos copias** de la actividad
de ejemplo: una **normal, que sí se edita** (sobre esta se reemplaza el contenido) y
una **en color rojo, que NO se toca nunca** (referencia para que el usuario mismo la
siga duplicando a mano). Regla dura: nunca editar ni borrar la copia roja. Si no está
claro cuál copia es cuál, **preguntar antes de tocar nada** — no asumir.

Importante: el resaltado en rojo que Moodle pinta sobre la sección actualmente
activa en el árbol de navegación lateral **no tiene nada que ver** con esta
convención — es solo el indicador de "sección que estás mirando ahora". La copia
roja real se identifica por el color del texto/fondo del contenido mismo, no del
árbol de navegación.

## 8. Bug de contenido duplicado — qué hacer según el caso

Si al contar módulos (paso 1) aparece el doble de lo esperado en una sub-sección:

- Si el contenido duplicado **coincide con una plantilla que de todos modos hay que
  expandir a N copias** (ej. una única actividad de ejemplo que se iba a duplicar
  para la actividad 2 y 3), **aprovechá el duplicado existente en vez de borrar y
  volver a duplicar desde cero** — es más eficiente.
- Si el contenido duplicado **no es una plantilla a expandir** (ej. es el único
  Trabajo Práctico de la sub-sección, no hay "TP 2" ni "TP 3"), correspondería
  borrar la copia sobrante y quedarse con una sola.
- **Preguntá antes de asumir cuál caso aplica.** Una vez que el usuario define el
  criterio para esa unidad, aplicalo de forma consistente al resto sin
  re-preguntar.

## 8a. Microteaching: sus 2 bloques de contenido son un único Label — verificado en vivo

A diferencia del resto de las sub-secciones, en Microteaching la tarjeta
introductoria ("Material de la Microteaching") y el bloque de contenido/enlaces
**no son dos Labels separados** — van concatenados en **un solo Label**, además de
la Descripción de la sección. Confirmado contando módulos reales en un curso ya
bien armado: esa sub-sección tiene un único Label. Generá
`01-contenido-microteaching.html` con los dos bloques ya concatenados en el orden
de `references/plantillas-html.md`, no como dos archivos.

## 8b. Autoevaluación y Encuesta de cierre no tienen Label — verificado en vivo

Confirmado inspeccionando el conteo real de módulos (`li[id^="module-"]`) tanto en
una corrida con un bug real (texto plano genérico pegado en la Descripción del
Cuestionario en vez del HTML de la plantilla) como en un curso ya bien armado: las
sub-secciones **Autoevaluación** y **Encuesta de cierre** tienen, cada una, **un
único módulo real** — el Cuestionario y la Encuesta (`mod_feedback`)
respectivamente. No hay ningún Label ahí. Todo el contenido "de más" que se ve en
la página (aparte del banner, que es la Descripción de la sección) es el campo
Descripción de ese único módulo, con "Mostrar descripción en la página del curso"
activado. Si en una importación aparece un Label extra en alguna de estas dos
sub-secciones, es una desviación — confirmá con el usuario antes de asumir que
corresponde.

## 9. Mapeo de archivo local → destino real en Moodle (resumen)

| Archivo generado | Destino en Moodle |
|---|---|
| `<Subsección>/00-descripcion-seccion.html` | Campo Descripción de esa sección (`editsection.php`) |
| `Introduccion/imagen-banner-introduccion.png` | `<img>` embebida dentro del campo Descripción de la sección raíz, reemplazando `URL_DE_LA_IMAGEN` — ver §9e |
| `Introduccion/01-video-introduccion.html`, `02-banner-foro.html`, `03-hoja-de-ruta.html` | Un Label cada uno, en ese orden |
| `Actividades/00-descripcion-seccion.html` | Descripción de la sub-sección Actividades |
| `Actividades/actividad-N/actividad-N.html` | Label de la actividad N |
| `Actividades/actividad-N/cuestionario-actividad-N.html` | Descripción del `mod_quiz` "Cuestionario – Actividad N" |
| `Actividades/actividad-N/preguntas-actividad-N.xml` | Import al banco de preguntas + agregado al `mod_quiz` |
| `Actividades/actividad-N/material-apoyo/material-apoyo-N-K.pdf` | Archivo dentro de la Carpeta (`mod_folder`) "Material de apoyo – Actividad N" — ver §9a |
| `Practica/00-descripcion-seccion.html` | Descripción de la sub-sección Práctica |
| `Practica/documento-practica.pdf` | Archivo (`mod_resource`) |
| `Practica/consigna-practica.html` | Label que describe el Archivo/la consigna |
| `Practica/entrega-practica.html` | Descripción de la Tarea (`mod_assign`) |
| `Microteaching/00-descripcion-seccion.html` | Descripción de la sub-sección Microteaching |
| `Microteaching/01-contenido-microteaching.html` | Un único Label (tarjeta intro + contenido/enlaces concatenados) |
| `Autoevaluacion/00-descripcion-seccion.html` | Descripción de la sub-sección Autoevaluación (no hay Label acá) |
| `Autoevaluacion/cuestionario-autoevaluacion.html` | Descripción del `mod_quiz` de Autoevaluación |
| `Autoevaluacion/preguntas-autoevaluacion.xml` | Import al banco de preguntas + agregado al `mod_quiz` de Autoevaluación |
| `EncuestaCierre/00-descripcion-seccion.html`, `01-encuesta-cierre.html` | Descripción de sección + Descripción del `mod_feedback` existente |
| `Presentacion General/00-descripcion-seccion.html` | Descripción de la sección `section=0` ("[Materia] - General") — ver Fase 10 de `SKILL.md` |
| `Presentacion General/01-foro-avisos-generales.html`, `02-foro-punto-de-partida.html`, `03-foro-avisos-comision.html` | Descripción de cada `mod_forum` nativo (no Label) |
| `Presentacion General/04-leccion-informacion-importante.md` | Contenido de las páginas del `mod_lesson` "Información importante sobre la materia" — ver §11 |
| `Presentacion General/05-que-necesitas-para-estudiar.html` | Label independiente |
| `Presentacion General/06-cuestionario-inicial.html` + preguntas XML | Descripción del `mod_quiz` "Cuestionario Inicial Obligatorio" + import de preguntas al banco — ver §11 |

## 9a. Material de apoyo — subir el PDF real a la Carpeta (confirmado en vivo)

Cada actividad trae, en su sub-sección Actividades, una Carpeta (`mod_folder`)
llamada **"Material de apoyo – Actividad N (pendiente)"** — el sufijo
"(pendiente)" viene de una corrida anterior que la dejó marcada así a
propósito, como señal visual de que faltaba contenido real. Confirmado en vivo
(Unidad 1, Actividad 1, `campustest` id=8) que el flujo completo es:

1. **Ubicar el `module-id` real de esa Carpeta**, con la misma técnica de
   `fetch` + regex del §1 (contar `id="module-(\d+)"`), o inspeccionando el
   HTML alrededor del texto "Material de apoyo" para sacar el id de
   `data-id="<id>"` del contenedor `activity-wrapper folder`.
2. **Ir directo a `course/modedit.php?update=<module-id>&return=1`** — abre el
   formulario de edición de la Carpeta, con una sección "Contenido" que trae
   el filemanager de Moodle (no hace falta pasar por la vista pública de la
   carpeta primero).
3. **Si la carpeta ya trae archivos de otra materia/plantilla reciclada**
   (pasó en vivo: una carpeta de Unidad 1 traía "Estructuras Secuenciales -
   Actividad I.pdf" e "Introducción a la programación.pdf", claramente de
   Programación 1) — es el mismo bug de contenido reciclado del §8, aplicá el
   mismo criterio: **no asumas que se borran solos**, confirmá con el usuario
   la primera vez que aparece en una unidad. Para borrar cada uno: click en el
   ícono del archivo dentro del filemanager → se abre un modal "Editar
   \<nombre\>.pdf" con un botón **"Borrar"** → confirma con el modal
   "¿Está seguro...?" → botón **"Sí"** (es un modal propio de Moodle, no un
   `confirm()` nativo del navegador — no bloquea la sesión).
4. **Subir el PDF real**: click en el botón "+" del filemanager (ícono de
   agregar, arriba a la izquierda del área de "Archivos") → se abre el
   "Selector de archivos" ya posicionado en la pestaña **"Subir un archivo"**
   → usá `find` para ubicar el botón "Adjunto"/"Seleccionar archivo" (es un
   `<input type=file>` real) → `file_upload` con la ruta absoluta del
   `material-apoyo-N-K.pdf` ya generado → botón **"Subir este archivo"**.
5. **Sacar el sufijo "(pendiente)" del campo Nombre** (arriba del todo del
   formulario, sección "General") una vez que la carpeta ya tiene contenido
   real — dejarlo así sería engañoso para cualquiera que mire el curso
   después.
6. **Guardar con "Guardar cambios y regresar al curso"** (mismo patrón que
   cualquier `modedit.php`).

Si una actividad tiene más de un documento de Material de apoyo
(`material_apoyo.prompts[]` con más de un ítem en `estado.yml`), repetí el
paso 4 por cada archivo — el filemanager de una Carpeta acepta múltiples
archivos sin problema, no hace falta crear una Carpeta por documento.

Marcá `material_apoyo.prompts[K].pdf_subido_por_usuario: true` en `estado.yml`
recién cuando el archivo ya está confirmado adentro de la Carpeta real (no
alcanza con que el PDF exista en el filesystem local).

## 9b. El widget de infografía se pega completo, nunca se recorta

Cada `actividad-N.html` trae un botón + `<details>` modal + `<script>` para la
infografía. Moodle va a stripear el `<script>` al guardar el Label — es esperado,
no es un error a corregir borrando el bloque. Pegá el bloque completo igual; lo
único real que suele faltar es la imagen (`URL_IMAGEN_INFOGRAFIA`), y eso se anota
como pendiente en el reporte, no se "arregla" sacando el widget entero.

## 9c. Si te trabás, pedí una mano en vez de forzar

Editores WYSIWYG que reescriben el HTML al pegarlo, modales que tardan en cargar,
checks de "cambios sin guardar" que no cierran — son esperables. Si después de 2-3
intentos razonables algo no cede, **avisá al usuario y pedile que lo resuelva a
mano esa vez** en lugar de seguir reintentando a ciegas contra el aula real.

## 9d. Link real de "Lectura PDF" en el Label — subir al draft area + reconstruir HTML completo

Cada `actividad-N.html` trae, dentro del widget de recursos, un `<a href="URL_PDF">`
que debe apuntar al PDF real de Lectura obligatoria de esa actividad
(`documento-lectura-actividad-N.pdf`). A diferencia del Material de apoyo (§9a, que
tiene su propia Carpeta `mod_folder` dedicada), este link vive DENTRO del mismo Label
de la actividad — no hay un módulo separado para alojarlo. **No uses el diálogo
"Crear enlace" de TinyMCE para insertarlo directo**: con "Texto a mostrar" vacío, el
botón auto-inserta la URL cruda en la posición del cursor apenas termina de subir el
archivo (sin pasar por "Crear enlace" ni mostrar el URL para copiar antes) —
corrompe cualquier texto que esté ahí. Es un comportamiento consistente de esta
versión de TinyMCE, no un bug esporádico: pasa siempre que subís un archivo nuevo
desde ese diálogo, con o sin colisión de nombre.

**Descartado antes de empezar**: el Banco de contenido (`contentbank/index.php?contextid=<id-curso>`)
NO sirve para esto — confirmado en vivo abriendo el botón "Subir" (no "Añadir", que
solo lista tipos H5P para crear contenido nuevo): el diálogo "Subir" declara
explícitamente "Tipos de archivo aceptados: Archivo (H5P) .h5p" — esta instancia de
Moodle solo tiene habilitado el plugin de tipo H5P en el Banco de contenido, ningún
plugin de archivo genérico/PDF. No hay URL permanente que sacar de ahí.

**Flujo que funciona, paso a paso:**

1. Abrí `course/modedit.php?update=<label-id>&return=1`. Anotá el itemid real
   leyendo el input `introeditor[itemid]` — **cambia en cada carga de página**, no
   reuses uno de una carga anterior ni de otra sesión.
2. Antes de tocar nada, leé del propio DOM (`tinymce.get('id_introeditor').getDoc()`)
   los links de Video 1/2/3 si ya están reales (el usuario suele cargarlos a mano
   directo en Moodle antes que vos) — los vas a necesitar para reconstruir el HTML
   completo en el paso 5, y así no los pisás con los placeholders del archivo local.
3. Click en el botón "Enlace" del toolbar → dialog "Crear enlace". Escribí cualquier
   texto inofensivo en "Texto a mostrar" (ej. `temp-safety`) como red de seguridad —
   sabés que se va a auto-insertar solo, mejor que sea texto reconocible y no una URL
   cruda. Click en "Ver repositorios..." → "Subir un archivo".
4. Subí el PDF real con un **nombre de archivo único** en el campo "Guardar como"
   (ej. `lectura-actividad-N-u1mf.pdf`) para evitar el diálogo "El archivo existe"
   (que además tiene su propia rareza: reusar un archivo con el mismo nombre a veces
   agrega un sufijo " (1)" inconsistente). Click en "Subir este archivo" — el link se
   auto-inserta con el texto ancla del paso 3.
5. Leé el href real recién insertado:
   `tinymce.get('id_introeditor').getDoc().querySelector('a').getAttribute('href')`.
   Es una URL `draftfile.php/<userid>/user/draft/<itemid>/<filename>` válida SOLO
   dentro de esta carga de página.
6. Reconstruí el HTML COMPLETO del Label offline, a partir del `actividad-N.html`
   local: sustituí `URL_VIDEO_1/2/3` por los reales del paso 2, `URL_PDF` por el href
   del paso 5, y dejá como placeholder lo que siga pendiente (`URL_IA_NOTEBOOKLM`,
   `URL_IMAGEN_INFOGRAFIA`, etc.). Pisá TODO el contenido en una sola pasada:
   `tinymce.get('id_introeditor').setContent(htmlCompleto)`. Nunca edites el DOM ya
   renderizado a pedazos (`setAttribute` puntual, editor de "Código fuente" a mano) —
   es la causa raíz de que este link se rompiera en un intento anterior.
7. Verificá antes de guardar (summary limpio, cantidad de links esperada, el resto
   del widget — infografía, código de apoyo — presente) y recién ahí click en
   "Guardar cambios y regresar al curso". Moodle reescribe automáticamente el
   `draftfile.php` a un `pluginfile.php` permanente al mover el archivo del área de
   borrador al área de archivos definitiva del módulo — comportamiento estándar de
   Moodle para editores de texto con archivos embebidos, no hace falta nada extra.

**Por qué reconstruir todo el HTML y no parchear solo el link**: si el Label ya
sufrió un intento fallido antes, es común que se haya perdido contenido de más (no
solo el link roto) — en una corrida real, el widget completo de Infografía
(botón + `<details>` modal) y el bloque "Código de apoyo" habían desaparecido
enteros de 3 Labels distintos, no solo el `<script>` que se pierde por comportamiento
normal de Moodle (§9b). Reconstruir el HTML completo desde el archivo local de una
sola vez repara ese daño colateral de paso, en vez de dejarlo pasar.

## 9e. Imagen de banner de Introducción — subir al campo Descripción de la sección (confirmado en vivo, Unidad 1 Metodología I, `campustest` id=8 sección 1)

1. Abrí `course/editsection.php?id=<section-id>` de la sección raíz de la
   unidad (la misma página donde se pega `00-descripcion-seccion.html`, ver
   §9) — llegás ahí desde el menú "⋮ → Editar ajustes" del encabezado de la
   sección en `course/view.php?id=<curso>&section=<N>` con "Modo de edición"
   activado, no hace falta armar la URL a mano. A diferencia de Tarea/
   Encuesta, esta página trae **un único** editor TinyMCE — confirmado que su
   id real es `id_summary_editor` (leelo con
   `Array.from(document.querySelectorAll('textarea')).map(t=>t.id)` antes de
   asumirlo, puede variar entre instancias/versiones de Moodle).
2. El botón "Imagen" del toolbar de TinyMCE (ícono de foto, distinto del
   botón "Enlace" que usa §9d para el PDF) abre un diálogo **"Insertar
   imagen"** con una zona de drag-and-drop/click-to-upload directa (sin pasar
   por "Buscar en repositorios" primero). Subí
   `Introduccion/imagen-banner-introduccion.png` con `file_upload` sobre el
   `<input type=file>` real de esa zona.
3. Al subir, se abre un sub-diálogo **"Detalles de la imagen"** con preview +
   un campo obligatorio "¿Cómo describiría esta imagen a alguien que no
   pudiera verla?" (alt text, **límite ~125 caracteres** — un alt más largo
   se corta a mitad de palabra, escribilo corto) + opciones de tamaño +
   checkbox "La imagen solo es decorativa". Si intentás guardar con el alt
   vacío, Moodle rechaza con "Una imagen debe tener una descripción salvo que
   se haya marcado como decorativa" y el diálogo se queda abierto — completá
   el campo (usá `find` para ubicarlo preciso, el diálogo puede quedar
   recortado por el viewport) antes de tocar "Guardar".
4. **Confirmado: este diálogo NO autoinserta como el de "Enlace" de §9d** —
   inserta el `<img>` real recién al tocar "Guardar" del sub-diálogo de
   detalles, en la posición del cursor. Eso significa que **coexiste con el
   `<img src="URL_DE_LA_IMAGEN">` que ya estaba en el contenido** — no lo
   reemplaza in-place. Confirmá con
   `tinymce.get('id_summary_editor').getDoc().querySelectorAll('img')` que
   ahora hay 2 imágenes antes de seguir.
5. **Igual que en §9d paso 6: reconstruí el HTML completo** de
   `00-descripcion-seccion.html` offline a partir del archivo local,
   reemplazando `URL_DE_LA_IMAGEN` por el `src` real de la imagen recién
   insertada (`draftfile.php/<userid>/user/draft/<itemid>/<filename>`, lo
   sacás del primer `<img>` del paso anterior) y usando el alt text real que
   escribiste en el paso 3. Pegalo entero con
   `tinymce.get('id_summary_editor').setContent(htmlCompleto)` — esto además
   saca de encima la imagen vieja/placeholder en la misma pasada, no hace
   falta borrarla aparte.
6. Guardá la sección ("Guardar cambios"). **Confirmado**: al guardar, Moodle
   reescribe automáticamente el `draftfile.php` a un `pluginfile.php`
   permanente (mismo comportamiento que §9d) — no hace falta ningún paso
   extra. Verificá visualmente en `course/view.php?id=<curso>&section=<N>`
   que la imagen se ve bien antes de dar nada por confirmado.
7. Marcá `introduccion.imagen_banner.subida_por_usuario: true` en `estado.yml`
   recién cuando la imagen ya se ve real en el aula (no alcanza con que el
   archivo exista en el filesystem local).

Si en la práctica el diálogo de imagen de esta instancia de Moodle se comporta
distinto a lo descripto arriba (ej. autoinserta igual que el de enlace, o no
tiene pestaña de subida), aplicá el mismo criterio de §9c: no fuerces varios
intentos a ciegas, avisá y ajustá esta sección con lo que se confirme.

## 10. Qué NO cubre esta referencia

Microteaching queda habitualmente **fuera de alcance** de una importación real salvo
que el usuario lo pida explícitamente (suele decidir no subir video/repo todavía) —
confirmá con el usuario si entra o no en esa corrida antes de tocarlo.

## 11. Presentación General (Fase 10) — Lección multi-página y Cuestionario gateado

Esta sección es la primera vez que la skill importa un módulo `mod_lesson` (todo
lo anterior era Label, Descripción de sección/módulo, Archivo, Tarea o Encuesta) y
la primera vez que configura una restricción de acceso real (gating) en vez de
solo documentarla — a diferencia del gating secuencial entre Cuestionarios de
Actividades, que el aula real ya trae preconfigurado en el template reciclado y
la skill solo documenta (ver `estructura-aula-real.md`), acá el módulo se crea
desde cero, así que si no se configura, nunca queda gateado.

**a) Crear el módulo Lección**: `course/modedit.php?add=lesson&type=&course=<courseid>&section=0&return=0&sr=0`.
En el formulario: nombre "ℹ️ Información importante sobre la materia.", pegar la
Descripción si aplica, y en la pestaña **"Finalización de actividad"** elegir
"Los estudiantes pueden marcar manualmente la actividad como completada" o
"Mostrar la actividad como completada cuando se cumplan las condiciones" (usá lo
que ya tenga configurado el resto del curso para otras Lecciones/mod_lesson, si
hay alguna de referencia; si no, preguntale al usuario cuál prefiere). Guardar.

**b) Cargar las páginas de contenido**: dentro de la Lección recién creada,
`mod/lesson/editpage.php?id=<cmid>&edit=1` — cada página nueva se agrega con
"Añadir una página de contenido", pegando el HTML de cada bloque del guion
(`04-leccion-informacion-importante.md`) vía `tinymce.get(...).setContent(html)`
(mismo mecanismo que el resto de la skill, ver §2) en el editor de esa página, y
un único botón "Continuar" apuntando a "Siguiente página" — no armes ramas ni
saltos condicionales salvo pedido explícito. Guardar cada página antes de pasar
a la siguiente.

**c) Restricción de acceso del Cuestionario inicial**: crear el `mod_quiz`
("📋 Cuestionario Inicial Obligatorio") con la técnica ya conocida (§3b), pegar
`06-cuestionario-inicial.html` en su Descripción (con "Mostrar descripción en la
página del curso" activado) e importar sus preguntas (§4). Después, en
`course/modedit.php?update=<cmid_quiz>&return=1`, sección **"Restricción de
acceso"** → "Añadir restricción..." → "Finalización de actividad" → seleccionar
la Lección del paso (a) → condición "debe estar completa". Guardar cambios.
Confirmá visualmente que el mensaje "No disponible hasta que..." apunte a la
Lección correcta antes de dar el paso por terminado.

**d) Si algo de (a)-(c) resulta más frágil de lo esperado** (el formulario de
Restricción de acceso cambia de layout entre versiones de Moodle, el editor de
páginas de Lección no carga bien): aplicá la misma regla general de la skill —
no reintentar en loop, dejar la pieza documentada como pendiente en el reporte
final (`presentacion_general.leccion_informacion_importante.completion_tracking_configurado`
/ `cuestionario_inicial.restriccion_acceso_configurada` en `false`) y avisarle
al usuario que la termine a mano, en vez de forzar un intento a ciegas.

**e) Los 3 foros** se crean con la técnica genérica de §3b (`add=forum`),
pegando cada descripción de `references/plantilla-presentacion-general.md`
Bloque 2 en el campo Descripción del foro (sin Label, mismo patrón que
`cuestionario-actividad-N.html`).
