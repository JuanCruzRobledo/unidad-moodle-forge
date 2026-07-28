# unidad-moodle-forge

Genera el **material completo de una unidad** para el aula virtual Moodle de TUP — HTML, preguntas XML, guiones de NotebookLM y PDF — calcando la **estructura real del campus**, no una suposición sobre cómo debería ser.

> Generar contenido es barato; publicar contenido pedagógico mal fundamentado o desincronizado de la plantilla oficial es caro. Por eso todo parte del material real del docente, y los pasos que dependen de una herramienta externa esperan confirmación explícita.

---

## ¿Qué hace?

A partir del programa de la materia, apuntes o un tema puntual, arma unidad por unidad:

1. **Introducción** — banner con resultados de aprendizaje, video colapsable, link al foro, hoja de ruta con tabla Pomodoro.
2. **Actividades** — HTML de cada actividad (con tarjetas de Infografía/PDF/Asistente IA), 5 preguntas XML por actividad para importar al banco de Moodle, y el guion fuente para que generes cada Notebook LM a mano.
3. **Práctica (Trabajo Práctico)** — consigna, formato de entrega según la carrera, y PDF fiel al HTML (solo después de que confirmes que el HTML está bien).
4. **Microteaching** — banner y contenido con los links de la clase.
5. **Autoevaluación** — HTML + 10 preguntas XML.
6. **Encuesta de cierre** — bloque prácticamente fijo entre unidades.
7. **Evaluaciones** (opcional, al final) — parciales y recuperatorios a nivel curso, fuera del material por unidad.

Un archivo `estado.yml` por materia guarda en qué unidad y sub-sección quedaste, para retomar en cualquier momento sin perder el hilo.

---

## Instalación

```bash
npx skills add https://github.com/JuanCruzRobledo/unidad-moodle-forge
```

La skill se carga sola cuando pedís armar o continuar el material de una unidad del aula virtual.

### Dependencias

```bash
python -m pip install -r requirements.txt
playwright install chromium
```

---

## Uso

Le decís al agente algo como:

```
"Armá la unidad 3 de Programación 3 (Herencia y Polimorfismo) a partir de este apunte"
"Seguí con la unidad de CSS donde quedó"
"Generá las preguntas XML y el guion de NotebookLM de la actividad 2"
```

El agente relee `estado.yml`, completa lo que falte fase por fase, y te muestra cada HTML antes de dar por confirmada una sub-sección — en particular, el HTML de la Práctica se te muestra y espera tu OK antes de convertirlo a PDF.

---

## Estructura

```
unidad-moodle-forge/
├── SKILL.md
├── README.md
├── requirements.txt
├── scripts/
│   ├── scaffold_unidad.py
│   ├── generar_pregunta_xml.py
│   └── render_pdf.py
├── references/
│   ├── plantillas-html.md
│   ├── estructura-aula-real.md
│   ├── formato-preguntas-moodle-xml.md
│   ├── notebooklm-guion.md
│   └── estado-yml-schema.md
└── assets/
    └── plantilla-oficial-extraida.txt
```

Una unidad generada queda así en el filesystem del usuario:

```
<Materia>/
├── estado.yml
└── Unidad N - <Nombre>/
    ├── Introduccion/introduccion.html
    ├── Actividades/
    │   ├── notebooklm/guion-actividad-1.md ...
    │   ├── actividad-1/actividad-1.html + preguntas-actividad-1.xml
    │   └── ...
    ├── Practica/consigna-tp.html + entrega-tp.html + consigna-tp.pdf
    ├── Microteaching/microteaching.html
    ├── Autoevaluacion/autoevaluacion.html + preguntas-autoevaluacion.xml
    └── EncuestaCierre/encuesta.html
```

---

## Por qué esta estructura

- **La Introducción no es una sub-carpeta separada de contenido nuevo, pero sí un archivo propio** — en el aula real esa página vive en la raíz de la sección de la unidad; separarla en su propio archivo deja clara la correspondencia 1:1 con esa sección de Moodle.
- **references/ en vez de meter las plantillas en SKILL.md** — los bloques HTML completos son extensos (con script del modal de infografía incluido); progressive disclosure evita que SKILL.md se vuelva ilegible.
- **PDF vía Playwright y no vía un motor tipo LaTeX/rendercv** — el contenido fuente ya es HTML con estilos inline, flexbox e iframes; un render de navegador headless reproduce exactamente lo que el usuario ve en Moodle, sin tener que traducir el diseño a otro formato.
- **estado.yml por materia** — la generación de una unidad completa no se hace en una sola pasada; el estado permite pausar, confirmar de a una sub-sección, y retomar en otra sesión sin perder contexto.
- **Evaluaciones como fase aparte** — vive en una sección de curso distinta (no es la "Autoevaluación" de cada unidad) y se activa bajo pedido explícito, para no inflar cada corrida con algo que solo se necesita una vez por cuatrimestre.

---

## Licencia

Apache-2.0
