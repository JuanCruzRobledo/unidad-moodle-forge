# Plantilla de Evaluaciones (parciales/recuperatorios) — sección de curso aparte

## Por qué esto es distinto de la Autoevaluación de unidad

"Evaluaciones" es una **sección de curso separada** (`Evaluaciones`, fuera de la
jerarquía de unidades — ver `references/estructura-aula-real.md`), con parciales,
recuperatorios, certificados y foros de consulta propios. No es la Autoevaluación
de cada unidad (esa es un cuestionario chico dentro de la unidad, sin nota que
pese en la cursada) — Evaluaciones es donde se juega la nota real de la materia.

Confirmado en vivo (curso Programación 3, TUP, `section=63`, HTML real en
`assets/tpi-evaluaciones-html-real.txt`): cada instancia de evaluación (1er
parcial, 2do parcial, Integrador, y sus recuperatorios) repite **el mismo patrón
de 5 piezas**, así que la plantilla modela una instancia canónica que se clona
por cada parcial que tenga la materia.

## Las 5 piezas de una instancia de evaluación

```
Consigna (PDF con membrete) → Tarjeta "Importante" + video → Entrega (assign) → Certificado (customcert, gateado) → Foro de consultas
```

1. **`documento-evaluacion-<nombre>.html`** — el documento completo con membrete
   institucional (mismo mecanismo que `plantilla-pdf-practica.md` /
   `plantilla-tpi-standalone.md`: `render_pdf.py --materia`). Confirmá con el
   usuario antes de generar el PDF.
2. **`presentacion-evaluacion-<nombre>.html`** — el bloque que va en la página de
   Moodle: tarjeta título de la instancia + tarjeta "Importante" con link al PDF
   y al video de referencia (si existe).
3. **`entrega-evaluacion-<nombre>.html`** — la descripción del `assign` de
   entrega, con las reglas de formato de archivo.
4. **Certificado** — no se genera HTML: es un módulo tipo certificado nativo del
   LMS (en Moodle, `customcert`), gateado a que la Entrega esté marcada como
   realizada. Documentá la regla de disponibilidad, no inventes contenido.
5. **Foro de consultas** — un foro nativo, sin HTML de presentación propio.

## Bloque 1 — Banner + tabla de fechas (a nivel de toda la sección, una sola vez)

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>✅ Evaluaciones - [NOMBRE DE LA MATERIA]</strong>
  </h2>
</div>
<div style="background-color: #e0f7fa; border: 4px solid #0097a7; border-radius: 10px; padding: 15px;
color: #000000; font-family: Arial, sans-serif; font-size: 16px; line-height: 1.6;">
  <h3 style="text-align: center; font-family: sans-serif;">
    <strong>📅 FECHAS DE EXAMEN DE [NOMBRE DE LA MATERIA]</strong>
  </h3>
  <table style="width: 100%; border-collapse: collapse; margin-top: 15px;">
    <thead>
      <tr style="background-color: #b2ebf2;">
        <th style="border: 1px solid #0097a7; padding: 8px; text-align: left;">PARCIALES</th>
        <th style="border: 1px solid #0097a7; padding: 8px; text-align: left;">Fecha de Examen</th>
        <th style="border: 1px solid #0097a7; padding: 8px; text-align: left;">Fecha de Recuperatorio</th>
      </tr>
    </thead>
    <tbody>
      <!-- Una fila por cada instancia de evaluación de la materia -->
      <tr>
        <td style="border: 1px solid #0097a7; padding: 8px;">[Nombre de la instancia]</td>
        <td style="border: 1px solid #0097a7; padding: 8px;">[Fecha/rango]</td>
        <td style="border: 1px solid #0097a7; padding: 8px;">[Fecha/rango o "Con la primer mesa de examen"]</td>
      </tr>
    </tbody>
  </table>
</div>
```

Esta tabla usa paleta propia (celeste/turquesa `#0097a7` / `#e0f7fa` / `#b2ebf2`) —
no la confundas con la tabla Pomodoro verde de la Introducción de unidad
(`plantillas-html.md`), son componentes distintos para propósitos distintos.

## Bloque 2 — Tarjeta título de la instancia (una por parcial/recuperatorio)

```html
<div style="background-color: #e3f2fd; border: 2px solid #64b5f6; padding: 20px; border-radius: 12px;
font-family: sans-serif; color: #0a1f44; line-height: 1.6;">
  <h3 style="color: #0a1f44; margin-bottom: 15px; border-bottom: 2px solid #90caf9; padding-bottom: 10px;
  font-family: sans-serif;">
    ✨ [NOMBRE DE LA INSTANCIA] – [NOMBRE DE LA MATERIA]
  </h3>
  <p style="font-weight: bold; color: #0d47a1;">🗓️ Fecha apertura: [DÍA DE LA SEMANA], [FECHA]</p>
  <p>
    El [NOMBRE DE LA INSTANCIA EN MAYÚSCULAS] consiste en <strong>[QUÉ DEBE HACER EL ALUMNO]</strong>,
    asegurando que [CRITERIO DE APROBACIÓN CLAVE].
  </p>
  <p style="color: #0d47a1; font-weight: bold; text-align: center; margin-top: 25px;">
    ¡A aprovechar esta instancia y a darlo todo! ¡Muchos éxitos! 💪🚀
  </p>
</div>
```

## Bloque 3 — Tarjeta "Importante" con video de referencia (sobre el recurso de consigna)

```html
<div style="background-color: #eef4ff; border: 2px solid #b7cdfa; padding: 20px; border-radius: 12px;
font-family: Arial, sans-serif; color: #1f2d3d; line-height: 1.6;">
  <h2 style="color: #0d47a1; margin-top: 0; font-family: sans-serif;">📘 Importante – [NOMBRE DE LA INSTANCIA]</h2>
  <p style="margin-bottom: 12px;">
    Les pedimos que <strong>lean atentamente el documento de [NOMBRE DE LA INSTANCIA]</strong>, ya
    que allí encontrarán la consigna completa, los requisitos de entrega y todos los detalles que
    deben tener en cuenta para realizarlo correctamente.
  </p>
  <p style="margin-top: 20px; background-color: #e3f2fd; padding: 10px; border-radius: 6px; text-align: center;">
    <a href="URL_PDF_DOCUMENTO_EVALUACION" target="_blank" rel="noopener" style="font-weight: bold;">
      📄 Descargar la consigna completa (PDF)
    </a>
  </p>
  <!-- Sección de video de referencia: opcional, solo si YA existe un video de ejemplo
       (a diferencia del video de Introducción de unidad, este NO se resuelve con un
       guion de grabación — es un video de ejemplo de una entrega ya corregida, no
       algo que la cátedra necesite grabar de cero para poder publicar la evaluación). -->
  <p style="margin-bottom: 12px;">
    Además, les dejamos un <strong>video de ejemplo</strong> para que puedan observar con mayor
    claridad <strong>qué es lo que se espera en esta entrega</strong>.
  </p>
  <div style="background-color: #e3f2fd; border-left: 4px solid #1e88e5; padding: 12px 15px; border-radius: 8px;
  margin-top: 15px;">
    <p style="margin: 0; font-weight: bold; color: #0d47a1;">▶️ Video de referencia:</p>
    <p style="margin: 8px 0 0 0;">
      <a href="URL_VIDEO_EJEMPLO" style="color: #1565c0; font-weight: bold; text-decoration: underline;">
        Ver video de ejemplo
      </a>
    </p>
  </div>
</div>
```

Si todavía no existe un video de ejemplo real, omití el sub-bloque de "Video de
referencia" entero en vez de dejar un placeholder — a diferencia del video de
Introducción de unidad, acá no corresponde generar un guion de grabación (no es
un video que la cátedra tenga que grabar para poder publicar la evaluación).

## Bloque 4 — Tarjeta de descripción de la Entrega (assign)

```html
<div style="background-color: #f9f9ff; border: 2px solid #cbb2ff; padding: 18px; border-radius: 10px;
font-family: sans-serif; color: #333; line-height: 1.6;">
  <h3 style="color: #5a189a; margin-bottom: 12px; font-family: sans-serif;">
    📤 Entrega de [NOMBRE DE LA INSTANCIA]
  </h3>
  <p>En este espacio deberás <strong>subir tu resolución de [NOMBRE DE LA INSTANCIA]</strong>.</p>
  <p>
    Recordá que la entrega estará habilitada desde <strong>[FECHA/HORA DE APERTURA]</strong> hasta
    <strong>[FECHA/HORA DE CIERRE]</strong>.
  </p>
  <p style="background: #fff3cd; padding: 10px; border-left: 5px solid #ffcd39; border-radius: 8px;
  margin-top: 15px;">
    ⚠️ <strong>Importante:</strong> la entrega debe realizarse en <strong>[REGLA DE FORMATO DE
    ARCHIVO/NOMBRE]</strong>.<br>
    <strong>[REGLA ADICIONAL si aplica, ej. dónde va el link del video/repositorio]</strong>.
  </p>
  <p style="font-size: 1.05em; color: #5a189a; font-weight: bold; text-align: center; margin-top: 18px;">
    ¡Revisá bien tu archivo antes de enviarlo y mucho éxito! 🚀✨
  </p>
</div>
```

## Bloque 5 — Certificado (no es HTML, es configuración + regla de gating)

El Certificado/Constancia de cada instancia **no se redacta como HTML** — es un
módulo de certificado nativo del LMS (en Moodle, tipo `customcert`) que genera un
PDF automáticamente a partir de una plantilla configurada en el propio módulo.
Lo único que documentás vos (y confirmás con el usuario) es la **regla de
disponibilidad**: el certificado queda oculto hasta que la Entrega correspondiente
esté marcada como realizada (o la condición de fecha/grupo que aplique). No
inventes contenido de certificado — si el usuario no tiene esa plantilla armada
en el LMS todavía, marcalo como pendiente en `estado.yml` y avisale.

## Generar el PDF de la consigna de cada instancia

```
python scripts/render_pdf.py \
  --entrada "Evaluaciones/documento-evaluacion-<nombre>.html" \
  --salida "Evaluaciones/documento-evaluacion-<nombre>.pdf" \
  --materia "<Nombre de la materia>"
```

Mismo gate de siempre: nunca corrés esto sin confirmación explícita del usuario
sobre el HTML del documento.

## Checklist antes de mostrarle el material al usuario

- ¿La tabla de fechas tiene una fila por cada instancia real de la materia (no
  copiaste "1er/2do Parcial + Integrador" si la materia tiene otra cantidad)?
- ¿La tarjeta de "Entrega" describe el formato de archivo real que se espera
  (no el `.zip` con front/back de Programación 3 si no aplica)?
- ¿Dejaste claro en `estado.yml` si el módulo de certificado ya existe
  configurado en el LMS o todavía está pendiente?
- ¿Evitaste inventar un video de referencia con placeholder si no hay uno real
  todavía (a diferencia del video de unidad, acá se omite el bloque entero)?
