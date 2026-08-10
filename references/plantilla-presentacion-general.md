# Plantilla de Presentación General del curso — pestaña "[Materia] - General"

## Por qué esto es distinto de la Introducción de unidad

"General" es la **sección 0 del curso real** (`course/view.php?id=X&section=0`) —
la primera pestaña que ve el alumno, antes que cualquier unidad. Se llama
literalmente **"[NOMBRE DE LA MATERIA EN MAYÚSCULAS] - General"**, no
"Introducción" (ese nombre ya lo usa la página raíz de cada unidad, ver
`references/estructura-aula-real.md`). Es un artefacto **curso-level, único por
materia** — no se repite por unidad y no vive dentro de la carpeta de ninguna
unidad, igual que Evaluaciones y el Trabajo Práctico Integrador (ver
`plantilla-evaluacion.md` / `plantilla-tpi-standalone.md`).

Confirmado en vivo, solo lectura (curso real `tup.sied.utn.edu.ar`,
`course/view.php?id=82&section=0`, "Programación III"): la sección trae un banner
de identidad, 3 foros nativos de nivel curso, una Lección de onboarding con
seguimiento de finalización, un Label puente, y un Cuestionario inicial no
calificado gateado a que esa Lección esté completa. `estructura-aula-real.md` ya
documentaba en líneas generales que esto existía ("Foros de curso, Lección
introductoria, Cuestionario inicial no calificado") — esta plantilla es el
desarrollo completo de esas piezas, que hasta ahora la skill nunca generaba.

## Las 5 piezas, en este orden

```
Banner de identidad (Descripción de la sección)
  → 3 Foros nativos (Avisos generales, Punto de Partida, Avisos de la comisión)
  → Lección "Información importante sobre la materia" (multi-página, con
    seguimiento de finalización activado)
  → Label "¿Qué necesitás para estudiar?" (puente hacia el cuestionario)
  → Cuestionario inicial obligatorio (no calificado, gateado a que la Lección
    esté marcada como completa)
```

El orden importa por dependencia real de contenido, no solo de lectura: el
Cuestionario inicial pregunta sobre lo que dice la Lección (normas de foros,
organización de la materia, condiciones de aprobación) — no se puede escribir
bien antes de que esa Lección exista. El banner y los 3 foros no dependen de
nada, se pueden generar apenas se sepa el nombre de la materia.

## Bloque 1 — Banner de identidad (una sola vez, toda la sección)

→ `00-descripcion-seccion.html` — Descripción de la sección 0 (`editsection.php`), **no es un Label**.

```html
<div style="background-color: #ffffff; border: 1px solid #ccc; padding: 30px; border-radius: 12px;
box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 30px; font-family: 'Segoe UI', sans-serif;">
  <div style="text-align: center;">
    <h1 style="font-size: 2.2rem; margin-bottom: 10px; background-color: #001855; color: #ffffff;
    padding: 15px; border-radius: 8px; font-family: sans-serif;">
      [ÍCONO] [NOMBRE DE LA MATERIA]
    </h1>
    <img class="img-fluid" src="URL_DE_LA_IMAGEN" alt="[Descripción breve de la imagen, ver más abajo]"
      style="margin-top: 15px; border-radius: 8px; max-width: 100%; height: auto;">
    <p style="color: #2c3e50; font-size: 1.1rem; margin-top: 15px; font-family: sans-serif;">
      [BAJADA DE UNA LÍNEA — qué es la materia y a quién está dirigida, ej. "Desarrollo Full Stack: Frontend + Backend + Bases de Datos"]
    </p>
  </div>
</div>
```

Misma estructura visual que el banner de Introducción de unidad (tarjeta
blanca + barra de título navy + imagen + texto debajo), sin la tabla de
"Resultados de Aprendizaje" — acá el objetivo es identidad de toda la materia,
no resultados de aprendizaje de un tema puntual.

**La imagen (`URL_DE_LA_IMAGEN`) se genera con el mismo mecanismo que el
banner de Introducción de unidad** — ver `references/imagen-banner-introduccion.md`
completo antes de generarla, en particular el **Paso 0 (ofrecer 2-4 conceptos
visuales distintos al usuario antes de generar nada — nunca generar a
ciegas)**. La diferencia con Fase 1: acá los conceptos representan a **toda la
materia**, no un tema de unidad puntual, y no hay paleta rotativa por número
de unidad (no es una unidad) — elegí un color de la misma paleta que quede
libre o que tenga sentido para la identidad general del curso. Guardá el
archivo en `Presentacion General/imagen-banner-general.png`, forzá 600×600px
con `scripts/resize_imagen_banner.py`, y mostrásela al usuario para confirmar
antes de seguir — marcá `presentacion_general.imagen_banner.status` en
`estado.yml` (ver `references/estado-yml-schema.md`).

## Bloque 2 — Los 3 Foros nativos (nombre + descripción, no HTML de página)

→ Tres módulos `mod_forum` reales, **no un Label**. La skill genera nombre +
descripción de cada uno como su propio archivo — igual categoría que
`cuestionario-actividad-N.html` (contenido que va en el campo Descripción del
módulo nativo, con "Mostrar descripción en la página del curso" activado si el
tema lo permite).

Nombres confirmados en vivo — reusalos tal cual salvo que la materia pida otros:

### `01-foro-avisos-generales.html`

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h4 style="color: #1565c0; font-family: sans-serif;">📢 Foro de Avisos</h4>
  <p style="font-size: 1rem;">
    Acá vas a encontrar todas las novedades del curso, fechas clave y recordatorios
    importantes. 🔍 ¡Revisalo seguido para no perderte nada! 📝🚀
  </p>
</div>
```

Nombre del módulo: **"Avisos generales 📢"**.

### `02-foro-punto-de-partida.html`

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h4 style="color: #1565c0; font-family: sans-serif;">🚀💻 Punto de Partida: Instalaciones y Ayuda</h4>
  <p style="font-size: 1rem;">
    💬 ¿Tenés dudas técnicas [sobre instalación de herramientas, entorno de trabajo, etc.]?
    Este es el espacio para dejar tus consultas. La comunidad y los profes están para
    ayudarte. 🚀🛠️
  </p>
</div>
```

Nombre del módulo: **"🚀💻 Punto de Partida: Instalaciones y Ayuda"**. Adaptá el
contenido entre corchetes al tipo de instalación/setup real que necesita esta
materia (derivalo del Programa Detallado si trae una sección de requisitos
técnicos — ver Bloque 4).

### `03-foro-avisos-comision.html`

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h4 style="color: #1565c0; font-family: sans-serif;">📌 Foro de Avisos de la Comisión</h4>
  <p style="font-size: 1rem;">
    📢 Aquí se publicarán anuncios importantes sobre los encuentros sincrónicos y
    novedades relevantes de esta comisión. 🗓️ Consultá fechas y horarios, y proponé
    temas que te gustaría tratar. 🔍 Revisalo con frecuencia para no perderte nada.
    ¡Tu participación es clave! 🚀
  </p>
</div>
```

Nombre del módulo: **"Avisos de la comisión 📌"**.

Si la materia no tiene comisiones separadas (dictado único), preguntale al
usuario si igual quiere este tercer foro o si lo omite — no lo asumas.

## Bloque 3 — Lección "Información importante sobre la materia" (multi-página)

→ Un módulo `mod_lesson` real, con **seguimiento de finalización activado**
(esto es configuración de Moodle, no HTML — se marca en Fase 8, ver
`references/importacion-moodle.md` §11). El entregable de la skill es el
**guion de páginas**, listo para pegar una por una en el editor de contenido de
la Lección: `04-leccion-informacion-importante.md`, con un bloque HTML por
página, en este orden. Cada página termina con un único botón "Siguiente" (salto
lineal, sin ramas) — no armes navegación condicional salvo que el usuario la
pida explícitamente.

**Regla dura de contenido**: las páginas 3 y 4 (organización de la materia y
condiciones de aprobación) son datos institucionales reales, no relleno
genérico. La página 3 sale del índice de unidades/bloques del Programa
Detallado (fuente de verdad, ver el `CLAUDE.md` del workspace). La página 4
(condiciones de aprobación: regularidad, promoción, % de asistencia, TPs
obligatorios, etc.) **se pregunta al usuario si el Programa Detallado no la
trae explícita** — nunca se inventa un criterio de aprobación.

### Página 1 — Bienvenida

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.7;">
  <h3 style="color: #1565c0;">📘 Información Introductoria</h3>
  <p>
    👋 Bienvenido/a, aquí encontrarás la información fundamental para comenzar el
    recorrido de <strong>[NOMBRE DE LA MATERIA]</strong> de manera organizada y clara.
  </p>
  <p>En los siguientes apartados vas a conocer:</p>
  <ul style="padding-left: 25px;">
    <li>📢 Las normas de participación en los foros.</li>
    <li>📚 Los contenidos de la materia y su organización.</li>
    <li>📌 Las condiciones de aprobación.</li>
  </ul>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    🎯 <strong>Objetivo de esta sección:</strong> brindarte una visión clara del
    funcionamiento de la materia, las expectativas académicas y las pautas de trabajo.
  </div>
  <p style="margin-top: 15px;">
    💡 Te recomendamos leer cada apartado con atención antes de avanzar. Una
    comprensión clara de estas pautas va a facilitar tu desempeño durante el cursado.
  </p>
</div>
```

### Página 2 — Normas de participación en los foros

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.7;">
  <h3 style="color: #1565c0;">📢 Normas de participación en los foros</h3>
  <p>Los foros son el canal oficial de comunicación de la materia. Para que funcionen bien para todos:</p>
  <ul style="padding-left: 25px;">
    <li>[Norma 1 — ej. usar el foro correcto según el tipo de consulta: Avisos vs. Punto de Partida vs. Avisos de la comisión]</li>
    <li>[Norma 2 — ej. tono respetuoso, sin lenguaje ofensivo]</li>
    <li>[Norma 3 — ej. tiempo estimado de respuesta de la cátedra]</li>
    <li>[Norma 4 — ej. buscar si la consulta ya fue respondida antes de repetirla]</li>
  </ul>
</div>
```

Completá las normas con lo que el usuario ya tenga como convención de cátedra
(si no las trajo, preguntale — son reglas de convivencia reales de su curso, no
un genérico inventado por la skill).

### Página 3 — Contenidos de la materia y su organización

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.7;">
  <h3 style="color: #1565c0;">📚 Contenidos de la materia y su organización</h3>
  <p>
    <strong>[NOMBRE DE LA MATERIA]</strong> está organizada en las siguientes unidades:
  </p>
  <ol style="padding-left: 25px;">
    <li>[Unidad 1 — nombre real, del Programa Detallado]</li>
    <li>[Unidad 2 — nombre real]</li>
    <!-- una fila por cada unidad real del Programa Detallado, en orden -->
  </ol>
  <p>
    Cada unidad se organiza en las mismas sub-secciones: <strong>Actividades</strong>,
    <strong>Práctica</strong>[, <strong>Microteaching</strong>], <strong>Autoevaluación</strong>
    y <strong>Encuesta de cierre</strong> — así vas a poder ubicarte rápido en
    cualquier unidad que estés cursando.
  </p>
</div>
```

Esta lista de unidades sale 1:1 del Programa Detallado — el mismo texto/orden
que ya usás para armar el resto del material, nunca una versión resumida o
reinterpretada.

### Página 4 — Condiciones de aprobación

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.7;">
  <h3 style="color: #1565c0;">📌 Condiciones de aprobación</h3>
  <p>Para aprobar/regularizar <strong>[NOMBRE DE LA MATERIA]</strong> necesitás:</p>
  <ul style="padding-left: 25px;">
    <li>[Condición 1 — ej. % de asistencia a encuentros sincrónicos]</li>
    <li>[Condición 2 — ej. entrega y aprobación de los Trabajos Prácticos de cada unidad]</li>
    <li>[Condición 3 — ej. nota mínima en las Evaluaciones Integradoras]</li>
    <li>[Condición 4 — ej. condiciones de promoción directa vs. cursado regular con examen final]</li>
  </ul>
  <div style="background-color: #fff3e0; padding: 10px; border-radius: 5px; border-left: 4px solid #ff9800; margin-top: 15px;">
    ⚠️ Ante cualquier duda sobre tu situación puntual, consultá en el foro
    <strong>Avisos de la comisión</strong> o directamente con tu docente.
  </div>
</div>
```

**Nunca completes esta página con un porcentaje o criterio inventado.** Si el
Programa Detallado no trae esta información explícita, es de las pocas veces en
todo el flujo de la skill donde hay que **cortar y preguntarle directamente al
usuario** antes de seguir — es información institucional real que va a leer
cada alumno.

### Página 5 — Cierre

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.7; text-align: center;">
  <h3 style="color: #1565c0;">✅ ¡Ya tenés lo que necesitás para arrancar!</h3>
  <p>
    Con esto ya conocés cómo participar, cómo está organizada la materia y qué
    hace falta para aprobarla. El siguiente paso es completar el
    <strong>Cuestionario inicial obligatorio</strong> — te va a tomar solo unos
    minutos y no tiene calificación.
  </p>
  <p style="font-weight: bold; color: #0d47a1;">¡Éxitos en este nuevo recorrido! 🚀</p>
</div>
```

## Bloque 4 — Label "¿Qué necesitás para estudiar?"

→ `05-que-necesitas-para-estudiar.html` — Label independiente, puente hacia el Cuestionario inicial.

```html
<div style="background-color: #fff3e0; border: 1px solid #ffcc80; padding: 20px; border-radius: 10px;
font-family: sans-serif; color: #5d4037; line-height: 1.7;">
  <h3 style="color: #e65100;">🧰 ¿Qué necesitás para estudiar?</h3>
  <p>Antes de arrancar con el contenido de la materia, asegurate de tener:</p>
  <ul style="padding-left: 25px;">
    <li>[Requisito 1 — ej. cuenta de GitHub creada]</li>
    <li>[Requisito 2 — ej. entorno de desarrollo instalado: <nombre real de la herramienta>]</li>
    <li>[Requisito 3 — ej. acceso al material de cátedra / bibliografía]</li>
  </ul>
  <p style="margin-top: 15px; font-weight: bold;">
    Antes de comenzar con el estudio de la materia, respondé el siguiente cuestionario 👈
  </p>
</div>
```

Los requisitos técnicos salen del Programa Detallado si trae una sección de
"requisitos"/"herramientas" (buscala antes de preguntar); si no la trae,
preguntale al usuario qué necesita instalar/tener el alumno para esta materia
puntual — no reuses de memoria la lista de otra materia.

## Bloque 5 — Cuestionario inicial obligatorio (no calificado, gateado)

→ `06-cuestionario-inicial.html` — Descripción del `mod_quiz`, **no un Label**
(mismo patrón que `cuestionario-actividad-N.html`).

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h3 style="color: #1565c0;">📋 Cuestionario Inicial Obligatorio</h3>
  <p>
    📚 Este cuestionario inicial te va a ayudar a repasar los temas clave del curso:
    planificación, reglas, estructura y condiciones de aprobación.
  </p>
  <p>
    📝 <strong>¿Cómo se evalúa?</strong> No se califica. Tiene intentos ilimitados
    y es requisito responder todo correctamente para continuar.
  </p>
  <p style="font-weight: bold; color: #0d47a1;">🚀 ¡Completalo para comenzar con el pie derecho!</p>
</div>
```

### Configuración del Cuestionario (no es HTML, es ajustes de `mod_quiz`)

Documentá esto en `estado.yml` y confirmalo con el usuario antes de dar por
generada esta pieza (no son valores que la skill invente):

- **Método de calificación**: no calificado / calificación máxima 0 — no pesa en
  la nota final de la materia.
- **Intentos permitidos**: ilimitados.
- **Nota para aprobar**: 100% (el objetivo es que el alumno repase hasta
  contestar todo bien, no filtrar quién sabe más).
- **Restricción de acceso**: disponible solo cuando la Lección "Información
  importante sobre la materia" esté marcada como completa (`completion` de esa
  actividad) — ver `references/importacion-moodle.md` §11 para la técnica.

### Preguntas del Cuestionario inicial (XML)

A diferencia del resto de los cuestionarios de esta skill (que preguntan sobre
contenido técnico de una actividad/unidad), acá las preguntas son
**administrativas/de comprensión lectora sobre la propia Lección** — nunca
sobre los temas técnicos de las unidades. Generá 5 preguntas de opción múltiple
con `scripts/generar_pregunta_xml.py`, siguiendo `references/formato-preguntas-moodle-xml.md`,
con un prefijo propio de esta sección (ej. `GEN 1`..`GEN 5`, o el prefijo que
uses en `estado.yml` para el resto del banco de esa materia + un sufijo
distintivo — no reuses el prefijo de ninguna unidad). Ejemplos de qué cubrir:

1. Qué foro corresponde usar para cada tipo de consulta.
2. Cómo está organizada la materia (unidades / sub-secciones).
3. Una condición de aprobación real (de la Página 4).
4. Un requisito técnico real (del Bloque 4).
5. Qué pasa si no se responde todo bien (se puede reintentar, no hay límite de intentos).

## Checklist antes de mostrarle el material al usuario

- ¿Le ofreciste al usuario 2-4 conceptos visuales distintos para la imagen del
  banner ANTES de generarla (nunca el cliché de cerebro/chip para todo lo de
  IA), y generaste solo la que eligió? Ver `references/imagen-banner-introduccion.md` Paso 0.
- ¿El banner dice el nombre real de la materia, no un placeholder?
- ¿La Página 3 de la Lección lista las unidades reales del Programa Detallado,
  en el mismo orden, sin resumir ni inventar nombres?
- ¿La Página 4 (condiciones de aprobación) sale del Programa Detallado o fue
  confirmada explícitamente por el usuario — nunca un porcentaje/criterio
  inventado?
- ¿El Bloque 4 (requisitos técnicos) es específico de esta materia, no una
  lista genérica reciclada de otra?
- ¿Las 5 preguntas del Cuestionario inicial son sobre la Lección (administrativas),
  no sobre contenido técnico de ninguna unidad?
- ¿Quedó documentado en `estado.yml` que la Lección necesita seguimiento de
  finalización activado y el Cuestionario necesita la restricción de acceso
  gateada a esa Lección (dos ajustes de Moodle, no HTML)?
