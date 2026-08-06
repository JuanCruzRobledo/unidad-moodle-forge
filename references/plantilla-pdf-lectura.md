# Plantilla del documento PDF de Lectura (tarjeta "Lectura PDF" de cada actividad)

## Por qué este archivo es distinto de `actividad-N.html`

La tarjeta "Lectura PDF" de cada actividad (`references/plantillas-html.md` §
Cuerpo de cada actividad, placeholder `URL_PDF`) linkea a un PDF descargable —
no a un fragmento de la página de Moodle. Igual que con `documento-practica.html`
(ver `plantilla-pdf-practica.md`), ese PDF **no es una captura de HTML de la
página**: es un documento sobrio con membrete institucional, para que el alumno
se lo baje y lo lea con calma como "material obligatorio" de la actividad.

## Por qué esto va DESPUÉS del prompt de Gamma (Material de apoyo)

Antes de escribir este documento, tiene que estar ya decidido qué va a cubrir el
**Material de apoyo** de esa actividad (ver `prompt-gamma-material-apoyo.md`) —
así la Lectura PDF se queda con el contenido núcleo/obligatorio de la actividad
(lo mínimo indispensable para resolverla) y no repite lo que Gamma ya va a cubrir
como profundización/ejemplos extendidos. No hace falta esperar a que el usuario
termine de correr el prompt en Gamma — alcanza con que el contenido de ambos
documentos ya esté planificado y no se solape.

**Regla y orden de generación** (igual mecanismo que la Práctica): se escribe
`documento-lectura-actividad-N.html` primero, se le muestra al usuario y se
**espera su confirmación explícita** antes de convertirlo a PDF con
`scripts/render_pdf.py --materia "<Nombre de la materia>"`. Nunca se genera el
PDF sin esa confirmación — mismo gate que `practica.pdf_status` /
`pdf_confirmado_por_usuario` en `estado.yml`, ahora aplicado a
`lectura_pdf.pdf_status` / `lectura_pdf.pdf_confirmado_por_usuario`.

## Estructura del documento

`documento-lectura-actividad-N.html` es un HTML **standalone**, con el mismo
`<head><style>` sobrio de `documento-practica.html` (blanco y negro con acentos
azules #4F81BD / #365F91, sin degradés ni tarjetas — reusar el mismo bloque
`<style>` de `plantilla-pdf-practica.md` tal cual, no reinventar otro). El
membrete (logo UTN + institución arriba, barra de color + materia + número de
página abajo) tampoco va en este HTML — lo agrega `render_pdf.py --materia`
igual que en la Práctica.

A diferencia del documento de Práctica (que puede tener "Caso Práctico" con
pasos, o preguntas de análisis), este es más corto y lineal — es una **lectura**,
no una consigna con entregable:

```html
<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<style>
  /* mismo bloque de estilos que plantilla-pdf-practica.md */
</style>
</head>
<body>

  <p class="doc-materia">[NOMBRE DE LA MATERIA EN MAYÚSCULAS]</p>
  <p class="doc-titulo">Lectura – Actividad [N]: [Nombre de la actividad]</p>

  <h2 class="seccion">Qué vas a poder hacer después de esta lectura</h2>
  <p>[1-2 líneas: el objetivo concreto, ligado al resultado de aprendizaje de
  la actividad — no genérico.]</p>

  <h2 class="seccion">[Nombre del primer concepto núcleo]</h2>
  <p>[Desarrollo, basado 1:1 en el material real ya usado para la actividad —
  ejercicios-resueltos.html / cuadernillo / ítem del programa.]</p>

  <h2 class="seccion">[Nombre del segundo concepto núcleo]</h2>
  <p>[Desarrollo.]</p>

  <!-- Repetir tantas secciones como conceptos núcleo tenga la actividad —
  normalmente 2 a 4, no más: esto es la lectura OBLIGATORIA, no un cuadernillo
  completo. Lo que profundiza más va al Material de apoyo (Gamma), no acá. -->

  <h2 class="seccion">Para repasar</h2>
  <ul>
    <li>[Idea clave 1, en una línea.]</li>
    <li>[Idea clave 2, en una línea.]</li>
  </ul>

</body>
</html>
```

## Generar el PDF

```
python scripts/render_pdf.py \
  --entrada "Actividades/actividad-N/documento-lectura-actividad-N.html" \
  --salida "Actividades/actividad-N/documento-lectura-actividad-N.pdf" \
  --materia "Metodologia I"
```

## Checklist antes de mostrarle el documento al usuario

- ¿Cada sección sale 1:1 del material real ya usado para escribir
  `actividad-N.html` — nada inventado ni genérico?
- ¿Se evitó repetir lo que ya va a cubrir el Material de apoyo de Gamma de esa
  misma actividad (ver su prompt ya escrito)?
- ¿Es realmente una lectura corta y núcleo (2-4 secciones), no un intento de
  meter ahí todo el contenido de profundización?
- ¿Mismo estilo sobrio que la Práctica — sin colores/tarjetas del resto del
  aula filtrándose acá?
