# unidad-moodle-forge

Genera el **material completo de una unidad** para el aula virtual Moodle de TUP — HTML, preguntas XML, guiones de NotebookLM y PDF — calcando la **estructura real del campus**, no una suposición sobre cómo debería ser. Bajo pedido explícito, también puede **importar ese material al aula real** vía browser automation.

> Generar contenido es barato; publicar contenido pedagógico mal fundamentado o desincronizado de la plantilla oficial es caro. Por eso todo parte del material real del docente, y los pasos que dependen de una herramienta externa o que modifican el aula real esperan confirmación explícita.

---

## ¿Qué hace?

A partir del programa de la materia, apuntes o un tema puntual, arma unidad por unidad — **un archivo HTML por cada bloque real de Moodle** (Descripción de sección, Label, Descripción de Cuestionario), nunca un único HTML con varios bloques pegados:

0. **Selección de componentes** (solo al crear una unidad nueva) — te pregunta qué incluir: Actividad lúdica, Microteaching, Material de apoyo, Videos de actividad, Autoevaluación, Encuesta de cierre. Queda grabado en `estado.yml` y no se vuelve a preguntar.
1. **Introducción** — banner con resultados de aprendizaje, video colapsable (placeholder), link al foro, hoja de ruta con tabla Pomodoro (4 archivos separados). El guion de grabación del video se escribe recién al **cierre de la unidad**, no acá — para que sea coherente con el contenido ya completo.
2. **Actividades** — HTML de cada actividad (con tarjetas de Infografía/PDF/Asistente IA) separado de la intro al cuestionario, 5 preguntas XML por actividad, y una cadena de recursos con orden de dependencias: el **prompt para Gamma** que resuelve el Material de apoyo → el documento y PDF de **Lectura obligatoria** (con membrete, vía `render_pdf.py`) → los **3 videos de la actividad**, con guion propio y render real bajo demanda con la skill `hyperframes` (TTS + slides, sin alucinar contenido) → recién con todo eso, el guion fuente para que generes el Notebook LM a mano.
3. **Práctica (Trabajo Práctico)** — bloque breve de consigna y formato de entrega según la carrera para la página de Moodle, más un documento aparte con membrete institucional (logo UTN, encabezado/pie repetidos) que es el que se convierte al PDF real que descarga el alumno — solo después de que confirmes que ese documento está bien.
4. **Microteaching** (opcional) — banner (Descripción de sección) + tarjeta introductoria y contenido con los links de la clase en un único Label.
5. **Autoevaluación** (opcional) — banner (Descripción de sección) + descripción del cuestionario directo en el Cuestionario (sin Label) + 10 preguntas XML.
6. **Encuesta de cierre** (opcional) — bloque prácticamente fijo entre unidades (2 archivos separados). Al cierre de la unidad (después de este paso) se escribe el guion del video de Introducción.
7. **Evaluaciones** (opcional, al final) — parciales y recuperatorios a nivel curso, fuera del material por unidad.
8. **Importación al aula real** (opcional, bajo pedido explícito) — sube el material ya generado y confirmado al curso real de Moodle vía browser automation (crea/edita secciones, Labels, Cuestionarios, Tareas y Encuestas), con checklist de seguridad previo (URL del curso, rol de gestor confirmado, aviso explícito de que es una acción riesgosa) y un reporte de pendientes/incoherencias al terminar.
9. **Completar pendientes** (opcional, bajo pedido explícito) — para una unidad que ya tiene material generado (o incluso ya importado) pero le quedaron placeholders sin resolver: recorre la misma cadena de dependencias de Actividades y completa solo lo que falta, sin repetir trabajo.

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

### Configuración (opcional, una sola vez por máquina)

Por default la skill funciona 100% manual: te entrega el prompt para pegar en Gamma, vos lo corrés y subís el resultado. Si tenés cuenta **Gamma paga** (Pro/Ultra/Team/Business) podés activar la generación automática del Material de apoyo:

```bash
cd unidad-moodle-forge
python scripts/configurar.py
```

Te va a preguntar si querés activarlo y te pide la API key con `getpass` (no queda visible en pantalla). Esto crea un `.env` local — **gitignoreado, nunca se versiona**.

> ⚠️ **Corré esto en tu propia terminal, no le pidas al agente que lo haga por vos.** Hay un bloqueo de seguridad global que le impide a Claude Code leer o editar cualquier archivo `.env`/`.env.*` — ni con Read/Edit ni con Bash — justamente para que una API key nunca termine expuesta en una conversación. Si el agente corre el script por vos, no hay forma de que la tipees sin que quede en el chat.

**¿Ya tenías la key seteada de antes (ej. con `setx GAMMA_API_KEY ...`) y Gamma no te la vuelve a mostrar?** Recuperala vos mismo, en tu propia terminal, con:

```powershell
powershell.exe -Command "[Environment]::GetEnvironmentVariable('GAMMA_API_KEY','User')"
```

Copiá ese valor y pegalo cuando `configurar.py` te lo pida — así no hace falta generar una key nueva en Gamma.

Una vez configurado, `scripts/gamma_generate.py` la toma sola desde `.env` (vía `python-dotenv`) y el agente corre la automatización sin volver a preguntar. Ver `env.example` para el resto de las variables (todavía sin implementar: generación de imagen de infografía y automatización de NotebookLM, quedan en `false` a propósito).

---

## Uso

Le decís al agente algo como:

```
"Armá la unidad 3 de Programación 3 (Herencia y Polimorfismo) a partir de este apunte"
"Seguí con la unidad de CSS donde quedó"
"Generá las preguntas XML y el guion de NotebookLM de la actividad 2"
"Completá los pendientes de la unidad 1 — le faltan videos y material de apoyo"
"Dame el prompt de Gamma para el material de apoyo de la actividad 2"
"Generame el video 1 de la actividad 3"
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
├── env.example              (plantilla de configuración por máquina — ver "Configuración")
├── scripts/
│   ├── configurar.py        (setup interactivo, una vez por máquina)
│   ├── scaffold_unidad.py
│   ├── generar_pregunta_xml.py
│   ├── gamma_generate.py
│   └── render_pdf.py
├── references/
│   ├── plantillas-html.md
│   ├── plantilla-pdf-practica.md
│   ├── plantilla-pdf-lectura.md
│   ├── prompt-gamma-material-apoyo.md
│   ├── automatizacion-videos-actividad.md
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
    │   │   ├── preguntas-actividad-1.xml
    │   │   ├── material-apoyo/prompt-gamma-1-1.md   (texto para correr en Gamma)
    │   │   ├── documento-lectura-actividad-1.html + .pdf
    │   │   └── videos/guion-video-actividad-1-1.md ... (+ .mp4 cuando se renderiza)
    │   └── ...
    ├── Practica/
    │   ├── 00-descripcion-seccion.html
    │   ├── consigna-practica.html + entrega-practica.html
    │   └── documento-practica.html + documento-practica.pdf
    ├── Microteaching/                        (2 bloques, 1 solo Label)
    │   ├── 00-descripcion-seccion.html
    │   └── 01-contenido-microteaching.html
    ├── Autoevaluacion/                       (sin Label — solo el Cuestionario)
    │   ├── 00-descripcion-seccion.html
    │   ├── cuestionario-autoevaluacion.html  (Descripción del mod_quiz)
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
- **Material de apoyo → Lectura PDF → Videos → NotebookLM, en ese orden estricto** — cada uno depende de que el anterior ya esté planificado: la Lectura PDF necesita saber qué va a cubrir el Material de apoyo de Gamma para no repetirlo, y el paquete de fuentes de NotebookLM lista archivos reales (PDF de Lectura, PDF de apoyo, guiones de video como transcripción) que tienen que existir antes de poder documentarlos.
- **Los videos de actividad se renderizan con la skill `hyperframes`, no con el "Resumen de video" nativo de NotebookLM** — NotebookLM sintetiza narración con sus propias palabras a partir de las fuentes, sin aceptar un guion exacto para leer al pie de la letra; HyperFrames usa el guion como texto literal para el TTS, así que es la opción que de verdad no alucina ni se desvía del contenido real. Se generan **on-demand** (nunca en lote para varias actividades/unidades a la vez) para no disparar el costo de render.
- **La selección de componentes opcionales se pregunta una sola vez, al crear la unidad** — queda grabada en `estado.yml` (bloque `incluir`) para que ninguna fase posterior tenga que volver a preguntar si esa unidad lleva Microteaching, Autoevaluación, etc.

---

## Licencia

Apache-2.0
