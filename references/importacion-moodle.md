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
| `Introduccion/01-video-introduccion.html`, `02-banner-foro.html`, `03-hoja-de-ruta.html` | Un Label cada uno, en ese orden |
| `Actividades/00-descripcion-seccion.html` | Descripción de la sub-sección Actividades |
| `Actividades/actividad-N/actividad-N.html` | Label de la actividad N |
| `Actividades/actividad-N/cuestionario-actividad-N.html` | Descripción del `mod_quiz` "Cuestionario – Actividad N" |
| `Actividades/actividad-N/preguntas-actividad-N.xml` | Import al banco de preguntas + agregado al `mod_quiz` |
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

## 10. Qué NO cubre esta referencia

Microteaching queda habitualmente **fuera de alcance** de una importación real salvo
que el usuario lo pida explícitamente (suele decidir no subir video/repo todavía) —
confirmá con el usuario si entra o no en esa corrida antes de tocarlo.
