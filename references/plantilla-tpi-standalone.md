# Plantilla del Trabajo Práctico Integrador (TPI) — sección de curso aparte

## Por qué esto no es "una Práctica más grande"

El TPI vive en su **propia sección de curso** (`Trabajo Practico Integrador`, fuera
de la jerarquía de unidades — ver `references/estructura-aula-real.md`), no dentro
de la Práctica de ninguna unidad puntual. Confirmado en vivo (curso Programación 3,
TUP, `section=61`, HTML real en `assets/tpi-evaluaciones-html-real.txt`): tiene su
propio banner, su propia tabla/tarjeta de presentación, un bloque de "Método de
Entrega" separado de la consigna, su propio foro de consultas, y su propio PDF de
rúbrica de corrección — es un mini-curso dentro del curso, con la misma lógica de
tres piezas que ya usa la Práctica de unidad (ver `plantilla-pdf-practica.md`), pero
a escala de proyecto final integrador.

**Reusa el mismo mecanismo de PDF con membrete que la Práctica de unidad** — no se
inventa un pipeline nuevo. La única diferencia real es que la consigna del TPI
suele ser más larga (varias entregas parciales, rúbrica propia) y vive en una
sección de curso, no en la carpeta de una unidad.

## Las piezas (mismo orden que Fase 3, aplicado a curso-level)

1. **`documento-tpi.html`** — PRIMERO. El documento completo con membrete
   institucional (igual estructura que `documento-practica.html`, ver
   `plantilla-pdf-practica.md` para los bloques de Objetivo general / Marco
   teórico / Caso Práctico o preguntas de análisis / Consideraciones /
   Conclusiones esperadas — para un TPI, "Caso Práctico" casi siempre aplica
   porque integra todo lo dado en el curso). Mostraselo al usuario y esperá su
   confirmación explícita antes de convertirlo a PDF con
   `scripts/render_pdf.py --materia "<Nombre de la materia>"`.
2. **`presentacion-tpi.html`** — SEGUNDO. El bloque que va en la página de Moodle
   de la sección: banner + tarjeta de descarga con link al PDF ya generado +
   video de presentación (casi nunca grabado todavía — mismo tratamiento que el
   video de Introducción de unidad: generá también un guion de grabación).
3. **`metodo-entrega-tpi.html`** — TERCERO. El bloque de reglas de entrega
   (formato del .zip, qué va en el README, qué NO se acepta). Necesita la
   consigna ya escrita porque describe exactamente qué archivos entrega el
   alumno.

## Bloque 1 — Presentación en la página de Moodle

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>📚 TRABAJO INTEGRADOR - [NOMBRE DE LA MATERIA EN MAYÚSCULAS]</strong>
  </h2>
</div>
<div style="background-color: #f9fbff; padding: 25px; border-radius: 15px; border: 1px solid #d0e3f7;
font-family: 'Poppins', sans-serif; color: #2c3e50; line-height: 1.7; box-shadow: 0 4px 8px rgba(0,0,0,0.05);">
  <p style="font-size: 1.1rem; color: #2c3e50; line-height: 1.8; margin-bottom: 15px;">
    En esta sección vas a encontrar todo lo necesario para preparar tu Trabajo Integrador de la
    materia: desde la consigna oficial 🧾, las pautas de evaluación 📌.
  </p>
  <p style="font-size: 1.1rem; color: #2c3e50; line-height: 1.8;">
    🔍 Explorá cada recurso con atención y no dudes en consultar si tenés dudas. ¡Estamos para
    acompañarte en este proceso! 💪✨
  </p>
</div>

<div style="background-color: #f4f7ff; padding: 22px; border-radius: 12px; border: 1px solid #d6e0ff;
border-left: 6px solid #4a7bdc; margin-top: 15px; font-family: sans-serif; color: #001855;
line-height: 1.75; box-shadow: 0 4px 10px rgba(0, 24, 85, 0.08);">
  <h2 style="color: #001855; margin: 0 0 12px; text-align: center; font-family: sans-serif;">
    📥 Descargá el Trabajo Práctico Integrador ([SIGLA, ej. TPI])
  </h2>
  <p style="margin: 0 0 16px;">
    En esta sección vas a encontrar el <strong>[SIGLA]</strong> para descargar y comenzar a
    trabajar. Te recomendamos bajarlo, leerlo completo y dejarlo a mano para ir avanzando durante
    la cursada.
  </p>
  <p style="margin-top: 20px; background-color: #e3f2fd; padding: 10px; border-radius: 6px; text-align: center;">
    <a href="URL_PDF_DOCUMENTO_TPI" target="_blank" rel="noopener" style="font-weight: bold;">
      📄 Descargar la consigna completa (PDF)
    </a>
  </p>
  <div style="background-color: #ffffff; border: 1px solid #d6e0ff; border-radius: 10px; padding: 16px;">
    <h3 style="margin: 0 0 10px; color: #001855; font-family: sans-serif;">🎥 Mirá el video de presentación</h3>
    <p style="margin: 0 0 12px;">
      Antes de empezar, mirá este video donde se explica <strong>qué se va a hacer</strong>, cómo
      organizarse y qué esperamos como resultado final.
    </p>
    <a href="URL_DEL_VIDEO_YOUTUBE" target="_blank" rel="noopener" style="display: inline-block;
    background-color: #4a7bdc; color: #ffffff; text-decoration: none; padding: 10px 14px;
    border-radius: 8px; font-weight: bold;"> ▶️ Ver video de presentación </a>
    <div style="background-color: #ffffff; padding: 12px; border-radius: 8px; border: 1px dashed #d6e0ff;
    margin-top: 14px;">
      ✅ <strong>Recomendación:</strong> [PUNTO CLAVE A TENER EN CUENTA ANTES DE EMPEZAR].
    </div>
  </div>
</div>
```

Si todavía no hay video grabado (caso casi seguro): generá igual el guion de
grabación (mismo tratamiento que el video de Introducción de unidad, 4-6 min) y
dejá `URL_DEL_VIDEO_YOUTUBE` como placeholder.

## Bloque 2 — Método de Entrega (separado de la consigna)

```html
<div style="background-color: #f4f7ff; border: 1px solid #d6e0ff; border-left: 6px solid #4a7bdc;
padding: 18px; border-radius: 10px; font-family: sans-serif; color: #001855; line-height: 1.6;
box-shadow: 0 4px 10px rgba(0, 24, 85, 0.08); margin-bottom: 20px;">
  <h4 style="color: #001855; font-size: 1.8rem; margin: 0; font-family: sans-serif;">
    📤 Entrega del Trabajo Integrador
  </h4>
</div>
<div style="background-color: #ffffff; border: 1px solid #e1e8ff; padding: 20px; border-radius: 8px;
font-family: sans-serif; color: #333; line-height: 1.7; margin-bottom: 20px;">
  <p style="margin-top: 0;">📌 <strong>Método de Entrega</strong></p>
  <p>
    La entrega del Trabajo Práctico Integrador deberá realizarse <strong>[FORMATO DE ENTREGA, ej.
    exclusivamente en formato .zip]</strong>. [Qué debe contener] deberá contener obligatoriamente:
  </p>
  <ul style="padding-left: 25px;">
    <li>[Ítem obligatorio 1, ej. código fuente / documento].</li>
    <li>[Ítem obligatorio 2].</li>
  </ul>
  <!-- Sumá acá cualquier archivo adicional obligatorio (ej. README con links) si aplica -->
  <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin-top: 20px;
  border-left: 4px solid #ff9800;">
    <p style="margin: 0; font-size: 1rem; color: #e65100;">
      <strong>⚠️ Importante:</strong> [QUÉ NO SE ACEPTA — entregas incompletas, fuera de formato, etc].
    </p>
  </div>
</div>
```

La caja de "Importante" reusa el mismo componente ya documentado en
`plantillas-html.md` (fondo claro + borde de color de acento) — no inventes un
estilo nuevo para esta caja.

## Generar el PDF de la consigna

Mismo comando que la Práctica de unidad, solo cambia la ruta:

```
python scripts/render_pdf.py \
  --entrada "Trabajo Practico Integrador/documento-tpi.html" \
  --salida "Trabajo Practico Integrador/documento-tpi.pdf" \
  --materia "<Nombre de la materia>"
```

**Nunca corras esto sin que el usuario haya confirmado `documento-tpi.html`
primero.** Ver la regla dura de SKILL.md — aplica igual acá.

## Componentes que NO se generan como HTML

- **Foro de Consultas del TPI**: solo un `forum` nativo de Moodle con el título
  "Foro de Consultas – Trabajo Práctico Integrador" — no lleva HTML de
  presentación propio.
- **Rúbrica de corrección**: un PDF aparte que sube el docente a mano (no lo
  genera esta skill; si el usuario ya tiene una rúbrica, se sube tal cual).
- **Recursos complementarios opcionales** (ej. plantilla base de código, datos
  de prueba): si el TPI los necesita, agrupalos en una tarjeta como la de
  "Recursos disponibles" del bloque de presentación (mismo estilo de tarjeta
  blanca con botones), pero es opcional — no todos los TPI la necesitan.

## Checklist antes de mostrarle el material al usuario

- ¿El banner dice el nombre real de la materia, no un placeholder?
- ¿El bloque de Método de Entrega describe el formato real de entrega de ESTE
  TPI (no copiaste literal el .zip con front/back de Programación 3 si la
  materia no tiene ese formato)?
- ¿La consigna completa vive en el PDF (`documento-tpi.html` → PDF), no
  duplicada palabra por palabra en la página de Moodle?
- ¿Dejaste el guion de grabación del video de presentación si no hay video real
  todavía?
