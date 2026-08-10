# Estructura real del aula (confirmada en vivo)

Fuente: recorrido de solo-lectura del campus TUP (`tup.sied.utn.edu.ar`, curso
Programación 3, `id=44`), contrastado contra la plantilla oficial en PDF. Esta es la
jerarquía que hay que calcar — no la que se supone a priori.

## Jerarquía

```
Curso (ej. "Programación 3", id=44)
├── section=0  → "<MATERIA> - General" (portada del curso, NO se llama "Introducción",
│     siempre la primera pestaña, antes de la Unidad 1 — ver plantilla-presentacion-general.md)
│     Banner de identidad, 3 Foros de curso, Lección introductoria multi-página con
│     seguimiento de finalización, Label puente, Cuestionario inicial no calificado
│     (gateado a que la Lección esté completa)
├── section=N   → "N- <Nombre de la unidad>"   = página raíz de la unidad
│                  (acá vive el contenido de "Introducción": banner, video, foro, hoja de ruta)
├── section=N+1 → "Actividades 🧩"     (hija de la unidad)
├── section=N+2 → "Práctica 💻"        (hija de la unidad — es el "Trabajo Práctico")
├── section=N+3 → "Microteaching 📘"   (hija de la unidad)
├── section=N+4 → "Autoevaluación 🔍"  (hija de la unidad)
├── section=N+5 → "Encuesta de cierre 🗳️" (hija de la unidad)
├── ... el patrón se repite +6 secciones por cada unidad siguiente
├── "Trabajo Practico Integrador" (curso-level, confirmado en vivo — ver plantilla-tpi-standalone.md)
├── "Encuentros Sincrónicos" (curso-level)
├── "Evaluaciones" (curso-level: parciales, recuperatorios, certificados — NO es la Autoevaluación de unidad, ver plantilla-evaluacion.md)
└── Secciones de gestión (Comisiones, Entrenamiento, Gestión Académica, etc. — fuera de alcance)
```

**Clave**: la unidad NO tiene una sub-sección "Introducción" propia. La página raíz de
la sección de la unidad (la que aparece en el menú con el nombre de la unidad) ES la
Introducción. Las 5 sub-secciones hijas reales son: Actividades, Práctica,
Microteaching, Autoevaluación, Encuesta de cierre.

## Mecanismo técnico de los tabs

Son **secciones nativas de Moodle** (`course/view.php?id=X&section=N`), no tabs
renderizados con HTML/JS dentro de una sola página. El tema del curso las muestra
como una barra horizontal de tabs (que son links a `section=N` distintos) más un
dropdown "Ir a..." con jerarquía indentada. Cada sub-sección se edita de forma
independiente (`course/editsection.php?id=N`).

Dentro de "Actividades", cada actividad concreta = 1 recurso **Label** (el bloque
HTML colapsable de `plantillas-html.md`) + 1 **mod_quiz** ("Cuestionario actividad N
[UNIDAD]") con **gating secuencial**: el cuestionario N+1 exige que el N esté
"realizado y superado" antes de habilitarse. Replicá ese gating conceptualmente al
documentar el orden de las actividades (no hace falta configurarlo vos si solo
generás archivos locales, pero avisale al usuario que el aula real lo tiene así).

## Conteos confirmados (Unidad 1, real)

- 4 actividades reales por unidad (puede variar; confirmá con el usuario si no lo
  aportó — no asumas siempre 4).
- **5 preguntas por cuestionario de actividad**, 1 punto cada una, 1 pregunta por
  página, todas de opción múltiple. Códigos de banco de preguntas del estilo
  `TEMA 1`, `TEMA 2` ... `TEMA 5` (en el aula real: `HTML 1`..`HTML 5`).
- **10 preguntas en el cuestionario de Autoevaluación**, compartiendo banco con las
  de actividades (en el aula real: `HTML1`..`HTML19`, pesos no uniformes de 0.55 a
  1.00 puntos). La Autoevaluación suele estar bloqueada hasta que se entrega el TP.

## Estado del material NotebookLM

Es **real y funcional en el aula**, no un placeholder — se confirmó un link
operativo del tipo `https://notebooklm.google.com/notebook/<uuid>`. NotebookLM no
tiene API pública: la skill genera el guion fuente (ver `notebooklm-guion.md`) y deja
el link como placeholder hasta que el usuario suba el material a mano y devuelva la
URL real.

## Qué SÍ existe y el usuario no había mencionado

- **Microteaching** y **Encuesta de cierre** — presentes en las 10 unidades reales
  del curso relevado, aunque el usuario originalmente solo mencionó
  Introducción/Actividades/Práctica/Autoevaluación. Si el usuario pide "las mismas
  secciones que el aula real", hay que incluir estas dos.
- Sección de curso **"Evaluaciones"** (parciales, recuperatorios, certificados) —
  distinta de la Autoevaluación de cada unidad, con sus propios foros de consulta
  por examen y tareas de entrega con ventana de fechas. Se trabaja como fase aparte
  (ver SKILL.md, Fase 7), no como parte del material de unidad. Plantilla:
  `references/plantilla-evaluacion.md`. HTML real relevado en vivo (banner,
  tabla de fechas de examen, tarjetas de consigna/entrega, regla de gating del
  certificado): `assets/tpi-evaluaciones-html-real.txt`.
- Sección de curso **"Trabajo Practico Integrador"** — el proyecto final del
  curso, también fuera de la jerarquía de unidades (ver SKILL.md, Fase 7).
  Plantilla: `references/plantilla-tpi-standalone.md`. Mismo asset de HTML real
  que Evaluaciones: `assets/tpi-evaluaciones-html-real.txt`.
- Foros de nivel curso: "Avisos generales", "Punto de Partida: Instalaciones y
  Ayuda", "Avisos de la comisión" — no existe un "Foro social" con ese nombre exacto
  en el curso real relevado. Viven en `section=0` ("General"), junto con una
  Lección de onboarding ("Información importante sobre la materia": normas de
  foros, organización de la materia, condiciones de aprobación) y un Cuestionario
  inicial no calificado gateado a que esa Lección esté completa — confirmado en
  vivo (solo lectura) contra `tup.sied.utn.edu.ar/course/view.php?id=82&section=0`,
  "Programación III". Se genera como fase aparte, curso-level y **una sola vez
  por materia** (a diferencia de Evaluaciones/TPI, acá no hay múltiples
  instancias) — ver SKILL.md Fase 10 y `references/plantilla-presentacion-general.md`.

## El primer bloque de cada sub-sección es la Descripción de esa sección, no un Label

Confirmado importando de punta a punta una unidad completa contra el aula real: el
primer `<div>` de cada bloque de `references/plantillas-html.md` (el banner grande
con el título de la sub-sección) **no es un Label** — es el campo **Descripción**
(resumen) de esa sección/sub-sección de Moodle, editable en
`course/editsection.php`, no un módulo aparte. Se nota porque su ⋮ trae opciones de
sección ("Editar ajustes", "Destacar", "Ocultar tema", "Duplicar" el tema entero) en
vez de opciones de actividad.

Por eso la skill genera ese primer bloque como su propio archivo
(`00-descripcion-seccion.html`) en vez de concatenarlo con el resto del contenido de
la sub-sección — ver la convención completa en `references/plantillas-html.md` y el
detalle operativo de cómo pegarlo en el lugar correcto en
`references/importacion-moodle.md` (Fase 8 de `SKILL.md`).

## Inconsistencias reales detectadas — NO replicar

- En las unidades 9 y 10 del curso relevado, la sub-sección "Práctica" aparece
  nombrada como **"Practica🧩"** (sin tilde, con el emoji de Actividades en vez del
  de Práctica) — es un error editorial del aula real, no un patrón a seguir. Usá
  siempre **"Práctica 💻"**.
- Hay inconsistencia narrativa real en el banner de hoja de ruta de la Unidad 1
  (dice "4 actividades" en un lugar y detalla solo 3 + integrador en otro) — no es
  intencional, no la repitas: contá bien las actividades que generás.
