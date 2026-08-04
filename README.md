# unidad-moodle-forge

Genera el **material completo de una unidad** para el aula virtual Moodle de TUP — HTML, preguntas XML, guiones de NotebookLM y PDF — calcando la **estructura real del campus**, no una suposición sobre cómo debería ser. Bajo pedido explícito, también puede **importar ese material al aula real** vía browser automation.

> Generar contenido es barato; publicar contenido pedagógico mal fundamentado o desincronizado de la plantilla oficial es caro. Por eso todo parte del material real del docente, y los pasos que dependen de una herramienta externa o que modifican el aula real esperan confirmación explícita.

---

## ¿Qué hace?

A partir del programa de la materia, apuntes o un tema puntual, arma unidad por unidad — **un archivo HTML por cada bloque real de Moodle** (Descripción de sección, Label, Descripción de Cuestionario), nunca un único HTML con varios bloques pegados:

1. **Introducción** — banner con resultados de aprendizaje, video colapsable, link al foro, hoja de ruta con tabla Pomodoro (4 archivos separados).
2. **Actividades** — HTML de cada actividad (con tarjetas de Infografía/PDF/Asistente IA) separado de la intro al cuestionario, 5 preguntas XML por actividad para importar al banco de Moodle, y el guion fuente para que generes cada Notebook LM a mano.
3. **Práctica (Trabajo Práctico)** — bloque breve de consigna y formato de entrega según la carrera para la página de Moodle, más un documento aparte con membrete institucional (logo UTN, encabezado/pie repetidos) que es el que se convierte al PDF real que descarga el alumno — solo después de que confirmes que ese documento está bien.
4. **Microteaching** — banner, tarjeta introductoria y contenido con los links de la clase (3 archivos separados).
5. **Autoevaluación** — HTML (2 archivos separados) + 10 preguntas XML.
6. **Encuesta de cierre** — bloque prácticamente fijo entre unidades (2 archivos separados).
7. **Evaluaciones** (opcional, al final) — parciales y recuperatorios a nivel curso, fuera del material por unidad.
8. **Importación al aula real** (opcional, bajo pedido explícito) — sube el material ya generado y confirmado al curso real de Moodle vía browser automation (crea/edita secciones, Labels, Cuestionarios, Tareas y Encuestas), con checklist de seguridad previo (URL del curso, rol de gestor confirmado, aviso explícito de que es una acción riesgosa) y un reporte de pendientes/incoherencias al terminar.

Un archivo `estado.yml` por materia guarda en qué unidad y sub-sección quedaste — generación e importación — para retomar en cualquier momento sin perder el hilo.

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

Para importar al aula real, se lo pedís explícitamente ("importá la unidad 2 al aula", "subí esto a Moodle") — el agente primero te pide la URL exacta del curso, confirma que tenés rol de gestor, y te avisa en texto claro que va a modificar el aula real antes de tocar nada.

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
│   ├── plantilla-pdf-practica.md
│   ├── estructura-aula-real.md
│   ├── importacion-moodle.md
│   ├── plantilla-reporte-importacion.md
│   ├── formato-preguntas-moodle-xml.md
│   ├── notebooklm-guion.md
│   └── estado-yml-schema.md
└── assets/
    ├── plantilla-oficial-extraida.txt
    └── logo-utn-tup.jpg
```

Una unidad generada queda así en el filesystem del usuario — **un archivo por bloque
real de Moodle**, nunca un HTML con varios bloques concatenados:

```
<Materia>/
├── estado.yml
└── Unidad N - <Nombre>/
    ├── Introduccion/
    │   ├── 00-descripcion-seccion.html   (Descripción de la sección raíz)
    │   ├── 01-video-introduccion.html
    │   ├── 02-banner-foro.html
    │   └── 03-hoja-de-ruta.html
    ├── Actividades/
    │   ├── 00-descripcion-seccion.html
    │   ├── notebooklm/guion-actividad-1.md ...
    │   ├── actividad-1/
    │   │   ├── actividad-1.html                  (Label)
    │   │   ├── cuestionario-actividad-1.html      (Descripción del Cuestionario)
    │   │   └── preguntas-actividad-1.xml
    │   └── ...
    ├── Practica/
    │   ├── 00-descripcion-seccion.html
    │   ├── consigna-practica.html + entrega-practica.html
    │   └── documento-practica.html + documento-practica.pdf
    ├── Microteaching/
    │   ├── 00-descripcion-seccion.html
    │   ├── 01-material-microteaching.html
    │   └── 02-contenido-enlaces.html
    ├── Autoevaluacion/
    │   ├── 00-descripcion-seccion.html
    │   ├── 01-autoevaluacion.html
    │   └── preguntas-autoevaluacion.xml
    ├── EncuestaCierre/
    │   ├── 00-descripcion-seccion.html
    │   └── 01-encuesta-cierre.html
    └── reporte-importacion.md   (solo si ya se corrió la Fase 8 sobre esta unidad)
```

---

## Por qué esta estructura

- **La Introducción no es una sub-carpeta separada de contenido nuevo, pero sí un archivo propio** — en el aula real esa página vive en la raíz de la sección de la unidad; separarla en su propio archivo deja clara la correspondencia 1:1 con esa sección de Moodle.
- **references/ en vez de meter las plantillas en SKILL.md** — los bloques HTML completos son extensos (con script del modal de infografía incluido); progressive disclosure evita que SKILL.md se vuelva ilegible.
- **PDF vía Playwright y no vía un motor tipo LaTeX/rendercv** — el contenido fuente ya es HTML con estilos inline, flexbox e iframes; un render de navegador headless reproduce exactamente lo que el usuario ve en pantalla, sin tener que traducir el diseño a otro formato.
- **El PDF de la Práctica sale de un documento aparte, no de una captura de la página de Moodle** — comparado en vivo contra un TP real de cátedra, el PDF que descarga el alumno es un documento con membrete institucional (encabezado/pie repetidos por página), no las tarjetas y degradés de la página web. `render_pdf.py` usa `header_template`/`footer_template` de Playwright para lograr ese membrete repetido, algo que el CSS de impresión normal no soporta.
- **estado.yml por materia** — la generación de una unidad completa no se hace en una sola pasada; el estado permite pausar, confirmar de a una sub-sección, y retomar en otra sesión sin perder contexto.
- **Evaluaciones como fase aparte** — vive en una sección de curso distinta (no es la "Autoevaluación" de cada unidad) y se activa bajo pedido explícito, para no inflar cada corrida con algo que solo se necesita una vez por cuatrimestre.
- **Un archivo por bloque, no un HTML concatenado** — confirmado importando una unidad completa contra el aula real: el primer bloque de cada sub-sección es la Descripción de esa sección de Moodle (no un Label), y cada bloque siguiente es un Label independiente. Generarlos ya separados evita que alguien tenga que cortar un único HTML a mano al momento de pegarlo en el aula (que es justo lo que pasó en la primera corrida real, antes de este fix).
- **Importación como fase aparte y con checklist de seguridad** — modifica el aula real (no hay forma de "probarlo en seco"), así que nunca se dispara sola: pide la URL del curso, confirma el rol de gestor, avisa explícitamente que es una acción riesgosa, y deja siempre un reporte de pendientes/incoherencias — incluso si la corrida se corta a mitad de camino.

---

## Licencia

Apache-2.0
