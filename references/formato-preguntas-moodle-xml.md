# Formato Moodle XML para preguntas importables

Moodle importa preguntas al banco vía **Cuestionario → Banco de preguntas →
Importar → formato "Moodle XML"**. El archivo raíz es `<quiz>` con uno o más
`<question>`. Todas las actividades y la autoevaluación del aula real usan
`multichoice` de opción única.

## Convención de códigos vista en el aula real

- Actividades: un código corto por tema + número correlativo, ej. `HTML 1`
  .. `HTML 5` (una actividad = 5 preguntas = 5 códigos).
- Autoevaluación: comparte banco con las actividades y lo extiende, ej. `HTML1`
  .. `HTML19` (sin espacio, distinto del de actividades — respetá el patrón que ya
  tenga la unidad si estás extendiendo un banco existente; si es unidad nueva, elegí
  un prefijo corto del tema, ej. `CSS 1`, `CSS1`).
- Guardá el prefijo elegido en `estado.yml` para que todas las actividades de la
  misma unidad usen el mismo, y no se pisen entre unidades distintas.

## Ubicar las preguntas en una categoría del banco

Al principio del archivo, una pregunta especial de tipo `category` le dice a Moodle
en qué categoría del banco crear las siguientes preguntas del archivo:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<quiz>
  <question type="category">
    <category>
      <text>$course$/top/Unidad N - Nombre/Actividad 1</text>
    </category>
  </question>

  <!-- ... preguntas multichoice acá ... -->

</quiz>
```

## Pregunta `multichoice` — ejemplo completo y funcional

```xml
  <question type="multichoice">
    <name>
      <text>HTML 1</text>
    </name>
    <questiontext format="html">
      <text><![CDATA[<p>¿Cuál de las siguientes etiquetas HTML se usa para crear un hipervínculo?</p>]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text><![CDATA[<p>La etiqueta <code>&lt;a&gt;</code> (anchor) es la que define un hipervínculo en HTML.</p>]]></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <single>true</single>
    <shuffleanswers>true</shuffleanswers>
    <answernumbering>abc</answernumbering>
    <showstandardinstruction>0</showstandardinstruction>
    <correctfeedback format="html">
      <text>Respuesta correcta.</text>
    </correctfeedback>
    <partiallycorrectfeedback format="html">
      <text>Respuesta parcialmente correcta.</text>
    </partiallycorrectfeedback>
    <incorrectfeedback format="html">
      <text>Respuesta incorrecta.</text>
    </incorrectfeedback>
    <answer fraction="100" format="html">
      <text><![CDATA[<code>&lt;a&gt;</code>]]></text>
      <feedback format="html"><text>¡Correcto!</text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<code>&lt;link&gt;</code>]]></text>
      <feedback format="html"><text>Incorrecto. Esa etiqueta se usa para hojas de estilo u otros recursos externos.</text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<code>&lt;href&gt;</code>]]></text>
      <feedback format="html"><text>Incorrecto. <code>href</code> es un atributo, no una etiqueta.</text></feedback>
    </answer>
    <answer fraction="0" format="html">
      <text><![CDATA[<code>&lt;nav&gt;</code>]]></text>
      <feedback format="html"><text>Incorrecto. Esa etiqueta agrupa bloques de navegación.</text></feedback>
    </answer>
  </question>
```

Campos clave a completar por pregunta:
- `name/text`: el código corto (ver convención arriba).
- `questiontext`: el enunciado, en HTML (podés envolver en `<![CDATA[...]]>` para no
  escapar caracteres).
- `single`: `true` para opción única (lo que usa el aula real), `false` para opción
  múltiple.
- `shuffleanswers`: `true` para que Moodle mezcle el orden de las opciones en cada
  intento.
- Una sola `<answer fraction="100">` (la correcta) y el resto en `fraction="0"` para
  opción única con puntaje binario — así se ve en el aula real (1 punto por
  pregunta en actividades). Si la unidad usa pesos no uniformes (como la
  Autoevaluación real, 0.55 a 1.00), ajustá `defaultgrade` por pregunta.

## Checklist antes de entregar el XML al usuario

- ¿El archivo tiene exactamente el número de preguntas esperado? 5 para actividad,
  10 para autoevaluación — contá antes de escribir el archivo, no asumas.
- ¿Cada pregunta tiene una única respuesta con `fraction="100"`?
- ¿Los códigos de pregunta (`name/text`) siguen el prefijo acordado para esa unidad
  y no se repiten entre preguntas ya existentes en el banco?
- ¿El XML es válido? (abrí/cerrá todas las etiquetas, `<![CDATA[]]>` bien cerrado).
  `scripts/generar_pregunta_xml.py` genera el XML a partir de un YAML simple para
  evitar errores manuales de escritura.
