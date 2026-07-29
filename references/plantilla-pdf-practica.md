# Plantilla del documento PDF de la Práctica (el que descarga el alumno)

## Por qué este archivo es distinto de `consigna-practica.html`

En el aula real, la pestaña **Práctica** de Moodle tiene dos cosas separadas:

1. Un bloque breve en la propia página de Moodle (`consigna-practica.html` +
   `entrega-practica.html` de `plantillas-html.md` § Trabajo Práctico) — el
   `<details>` con el resumen del TP y el bloque de formato de entrega. Esto
   sigue viviendo directo en la página, con las tarjetas/cajas de color del
   resto del aula.
2. Un **archivo PDF descargable** con la consigna completa — el documento que
   el alumno se lleva y lee con calma. Ese PDF **no es una captura de la
   página de Moodle**: es un documento con membrete institucional, igual al
   que se ve subiendo cualquier TP real del campus (comprobado bajando
   "Trabajo Integrador HTML" de Programación 3 y comparando contra
   `Actividad de Reflexión AI-Augmented Development.docx` como segundo
   ejemplo) — encabezado y pie de página institucionales repetidos en cada
   hoja, tipografía sobria, sin degradés ni tarjetas.

**Regla y orden de generación**: `documento-practica.html` se escribe **primero**,
se confirma, y se convierte a PDF con `scripts/render_pdf.py --materia "<Nombre de
la materia>"` — ahí vive la consigna completa y detallada. Recién con eso ya
resuelto se redactan `entrega-practica.html` (que describe el formato de entrega
del TP definido en la consigna — no se puede escribir bien antes) y, al final,
`consigna-practica.html` (que puede quedar breve: un resumen que apunte al PDF ya
generado, no la consigna completa palabra por palabra). Ver SKILL.md Fase 3 para
el orden completo.

## Estructura del documento

`documento-practica.html` es un HTML **standalone** (con su propio
`<head><style>`, no un fragmento para pegar en Moodle). El encabezado (logo
UTN + "TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN") y el pie de página (barra
de color con el nombre de la materia + número de página) **no van en este
HTML** — los agrega automáticamente `render_pdf.py` vía
`header_template`/`footer_template` de Playwright, que es la única forma de
lograr que se repitan en cada hoja del PDF (el CSS de impresión de un
navegador no soporta encabezados/pies corridos). No dupliques ese membrete a
mano dentro del body.

### Bloques de contenido (elegí y combiná según el TP)

El TP puede ser **procedimental/de código** (bloque A), **teórico/de
reflexión** (bloque B), o una combinación de ambos — no fuerces un TP teórico
a tener "Caso Práctico" con pasos de código si no corresponde, ni un TP de
código a tener secciones de preguntas de opinión.

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  body {
    font-family: Calibri, Arial, sans-serif;
    font-size: 11pt;
    color: #1a1a1a;
    line-height: 1.5;
    margin: 0;
    padding: 0;
  }
  .doc-materia, .doc-titulo {
    font-family: Calibri, Arial, sans-serif;
    font-size: 20pt;
    font-weight: 700;
    color: #000000;
    margin: 0 0 2px 0;
  }
  .doc-titulo { margin-bottom: 20px; }
  h2.seccion {
    font-family: Cambria, Georgia, 'Times New Roman', serif;
    font-size: 14pt;
    font-weight: 700;
    color: #4F81BD;
    text-transform: uppercase;
    margin: 26px 0 10px 0;
    page-break-after: avoid;
  }
  h3.subseccion {
    font-family: Cambria, Georgia, 'Times New Roman', serif;
    font-size: 12.5pt;
    font-weight: 700;
    color: #365F91;
    margin: 18px 0 8px 0;
    page-break-after: avoid;
  }
  p { margin: 0 0 10px 0; }
  ul, ol { margin: 0 0 10px 0; padding-left: 22px; }
  li { margin-bottom: 4px; }
  table.marco-teorico {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 16px;
  }
  table.marco-teorico th {
    background-color: #365F91;
    color: #ffffff;
    text-align: left;
    padding: 10px 12px;
    border: 1px solid #2b4a70;
    font-size: 11pt;
  }
  table.marco-teorico td {
    border: 1px solid #b9c6d6;
    padding: 10px 12px;
    vertical-align: top;
    font-size: 10.5pt;
  }
  table.marco-teorico tr { page-break-inside: avoid; }
  .consideraciones { list-style: none; padding-left: 0; }
  .consideraciones li::before { content: "\2705  "; }
</style>
</head>
<body>

  <p class="doc-materia">[NOMBRE DE LA MATERIA EN MAYÚSCULAS]</p>
  <p class="doc-titulo">[Nombre del Trabajo Práctico]</p>

  <h2 class="seccion">Objetivo general</h2>
  <p>[2-4 líneas: qué se espera que el alumno logre con este TP.]</p>

  <!-- OPCIONAL — solo si el TP necesita anclar conceptos antes del caso/las preguntas -->
  <h2 class="seccion">Marco teórico</h2>
  <table class="marco-teorico">
    <thead><tr><th>Concepto</th><th>Aplicación en este TP</th></tr></thead>
    <tbody>
      <tr><td>[Concepto 1]</td><td>[Cómo se aplica acá]</td></tr>
      <tr><td>[Concepto 2]</td><td>[Cómo se aplica acá]</td></tr>
    </tbody>
  </table>

  <!-- BLOQUE A — TP procedimental/de código: pasos numerados con sub-bullets -->
  <h2 class="seccion">Caso práctico</h2>
  <p>[Contexto general antes de los pasos.]</p>

  <h3 class="subseccion">1. [Nombre del paso o entregable]</h3>
  <ul>
    <li><strong>[Sub-bloque]:</strong>
      <ul><li>[Detalle concreto y verificable]</li></ul>
    </li>
  </ul>

  <h3 class="subseccion">2. [Nombre del siguiente paso o entregable]</h3>
  <p>[Descripción.]</p>

  <!-- BLOQUE B — TP teórico/de reflexión: secciones temáticas con preguntas -->
  <h2 class="seccion">[Nombre de la sección temática 1]</h2>
  <p>[Pregunta de análisis 1, redactada completa, no un título suelto.]</p>
  <p>[Pregunta de análisis 2.]</p>

  <h2 class="seccion">[Nombre de la sección temática 2]</h2>
  <p>[Pregunta de reflexión.]</p>

  <!-- Cierre, casi siempre presente -->
  <h2 class="seccion">Consideraciones</h2>
  <ul class="consideraciones">
    <li><strong>[Aspecto 1]:</strong> [detalle a tener en cuenta al resolver].</li>
    <li><strong>[Aspecto 2]:</strong> [detalle a tener en cuenta al resolver].</li>
  </ul>

  <h2 class="seccion">Conclusiones esperadas</h2>
  <ul>
    <li>[Qué debería poder hacer o entender el alumno al terminar el TP.]</li>
  </ul>

</body>
</html>
```

## Generar el PDF

```
python scripts/render_pdf.py \
  --entrada "Practica/documento-practica.html" \
  --salida "Practica/documento-practica.pdf" \
  --materia "Metodologia I"
```

`--materia` es lo que dispara el membrete completo (encabezado con logo +
institución, pie con la barra de color y ese texto). El logo institucional ya
está en `assets/logo-utn-tup.jpg` (extraído del PDF real de cátedra, no hace
falta pedirlo de nuevo). Si algún día hace falta convertir un HTML sin
membrete (caso legacy), se puede omitir `--materia` y el script hace una
conversión simple.

## Checklist antes de mostrarle el documento al usuario

- ¿El título es la materia + el nombre real del TP, no un placeholder?
- ¿Elegiste el bloque A (caso práctico), el B (preguntas de análisis), o
  ambos, según lo que el TP pide de verdad — sin forzar una estructura que no
  corresponde?
- ¿"Marco teórico" solo aparece si aporta (no es obligatorio en todos los TP)?
- ¿"Consideraciones" son items verificables, no relleno genérico?
- ¿No se filtró ningún color/tarjeta del estilo de la página de Moodle acá?
  Este documento es sobrio: blanco y negro con acentos azules (#4F81BD /
  #365F91), sin degradés ni cajas con `border-radius`.
