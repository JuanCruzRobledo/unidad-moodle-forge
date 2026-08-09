# Prompt para Gamma — Material de apoyo por actividad

## Qué resuelve esto

En el aula real, cada actividad tiene una carpeta Moodle **"Material de apoyo –
Actividad N"** (un recurso tipo Carpeta) que hoy queda siempre vacía — la skill
nunca generó nada para ese lugar, y quedó documentado como pendiente en las
bitácoras de importación de Unidad 2 a 5.

[Gamma](https://gamma.app) es una herramienta externa que arma documentos/PDFs
con diseño vía IA a partir de un prompt de texto. **Por default, el entregable
de la skill acá es el texto del prompt, nunca el PDF en sí** — igual que con
NotebookLM (ver `notebooklm-guion.md`): el usuario corre el prompt en Gamma a
mano, revisa el resultado, lo descarga y lo sube él mismo a la carpeta real de
Moodle. Esto sigue siendo el camino por default porque no todos los que
instalen esta skill van a tener cuenta paga de Gamma.

Gamma **sí tiene API pública** (`https://developers.gamma.app`), pero requiere
una cuenta paga (Pro/Ultra/Team/Business — el plan free no da acceso) y
funciona por créditos. Si el usuario ya tiene esa cuenta, existe un camino
opcional para generar el PDF directo sin copiar/pegar a mano — ver
"Generación automatizada opcional (API de Gamma)" más abajo. En los dos casos
el resultado se revisa antes de darlo por bueno; la API automatiza el paso
mecánico de generar/descargar, no el control de calidad del contenido.

## Por qué esto va ANTES de Lectura PDF

El "Material de apoyo" es contenido de profundización/complementario (ejemplos
extendidos, casos adicionales, ejercicios resueltos de más), mientras que la
tarjeta **Lectura PDF** de la actividad (`documento-lectura-actividad-N.html`,
ver `plantilla-pdf-lectura.md`) es la lectura núcleo/obligatoria. Para que estos
dos documentos no terminen repitiendo el mismo contenido, primero se decide y
se escribe el prompt de Gamma (qué va a cubrir el material de apoyo), y **recién
con eso ya planificado** se redacta la Lectura PDF, dejándole el contenido
núcleo y evitando pisar lo que ya va a cubrir Gamma. Ver el orden completo en
SKILL.md Fase 2.

## Cuántos prompts por actividad

**No es un número fijo.** Mirá el material real ya usado para escribir esa
actividad (sección de `ejercicios-resueltos.html`, cuadernillo, ítems del
programa) y decidí si alcanza con **un solo documento** de apoyo, o si tiene
sentido partirlo en **más de uno** (ej: un documento de profundización teórica +
un documento de casos/ejemplos resueltos aparte) porque el tema es amplio o
mezcla dos naturalezas distintas de contenido. La convención de `estado.yml` ya
soporta una lista (`material_apoyo.prompts[]`) — usala con 1 ítem cuando alcanza,
o más si de verdad hace falta separar.

## Regla dura #1: no inventar contenido

El prompt se arma **citando y resumiendo el material real** que ya se usó para
esa actividad — nunca un tema genérico "de relleno" para completar la carpeta.
Si el material fuente disponible no alcanza para justificar un documento de
apoyo con contenido real, no se genera un prompt vacío: se avisa que no hay
material de apoyo claro para esa actividad y se deja `material_apoyo.prompts: []`
en `estado.yml`, documentado como tal en el reporte de pendientes.

## Regla dura #2: el prompt tiene que ser AUTOCONTENIDO (Gamma no lee tu filesystem)

**Gamma no tiene acceso a ningún archivo local ni a `ejercicios-resueltos.html`
ni al PDF de cátedra.** Lo único que "sabe" es lo que el usuario pega en su caja
de prompt. Por eso, el bloque que se marca como "listo para pegar en Gamma" NO
puede contener:

- Nombres de archivo (`ejercicios-resueltos.html`, `guion-actividad-N.md`, `AI-Augmented-Development.pdf`, etc.)
- Frases tipo "Fuente: ...", "ver archivo...", "según el documento..."
- Referencias a otras piezas del material de la unidad por nombre ("la Lectura PDF", "el documento de la Práctica")

Todo el contenido real que justifica el documento —los datos, ejemplos,
conceptos que se extrajeron del material fuente— tiene que estar **ya escrito
en prosa completa, dentro del bloque que se pega**, no resumido como bullet +
puntero a dónde ampliarlo. Si hace falta citar de dónde salió cada dato (para
la trazabilidad y la Regla dura #1), esa cita va **aparte, en una sección
separada y claramente marcada como "no pegar en Gamma"** — nunca mezclada
adentro del bloque copiable.

Mismo criterio para las exclusiones ("qué no debe cubrir este documento"):
se describen **por tema** ("no cubras la evolución histórica completa"), nunca
por nombre de archivo ("no cubras lo que ya está en documento-lectura-....html").

## Plantilla del prompt (`Actividades/actividad-N/material-apoyo/prompt-gamma-N-K.md`)

El archivo tiene **dos bloques bien separados** por un divisor visible — el
primero es lo único que el usuario copia y pega en Gamma tal cual, el segundo
es uso interno de la skill/el usuario y nunca va a Gamma:

```markdown
# Prompt para Gamma — Material de apoyo K: [Nombre del documento]

## ✂️ PROMPT LISTO PARA GAMMA — copiar TODO este bloque tal cual (nada de afuera)

Generá un documento PDF de apoyo académico en español, para estudiantes de
[nombre de la materia] en la Tecnicatura Universitaria en Programación (TUP,
UTN), sobre el siguiente tema: [tema puntual del documento].

Estructura esperada (desarrollá cada sección con profundidad real, sin relleno
genérico — ver más abajo cómo calibrar la extensión al material fuente real):
1. Portada: título del documento, subtítulo, un párrafo breve de presentación.
2. [Sección 1 — ej. "Contexto y por qué importa"]
3. [Sección 2 — ej. "Desarrollo con ejemplos concretos", partida en 2-3 tarjetas si el tema lo amerita]
4. [Sección 3 — ej. "Casos resueltos paso a paso"]
5. Cierre: síntesis del material y qué NO cubre este documento.

Basate ESTRICTAMENTE en el siguiente contenido real — no lo resumas de más, no
completes con información genérica de internet, no inventes datos, ejemplos ni
casos concretos que no estén acá. Si un punto es breve en el contenido de
abajo, mantenelo breve en el documento — no lo alargues inventando contenido
nuevo:

[Contenido real ya redactado en prosa/bullets COMPLETOS y autosuficientes —
3 a 6 puntos, cada uno debe poder leerse y entenderse solo, sin acceso a
ningún otro documento. Esto es la síntesis real del material fuente, no un
resumen-de-un-resumen con un puntero a "ver más en...". Escribí acá el dato,
el ejemplo, el caso — no dónde encontrarlo.]

No cubras en este documento: [temas que va a cubrir la Lectura PDF de esta
misma actividad, descriptos por TEMA — nunca mencionando el nombre de ese
archivo].

Reglas de formato obligatorias para este documento:
- La primera tarjeta es una portada: solo título, subtítulo y un párrafo de
  presentación breve — sin íconos ni gráficos decorativos ahí.
- El encabezado o pie de página de cada tarjeta de contenido tiene que decir
  "[nombre de la materia] — TUP · UTN". Nunca uses el nombre de otra materia.
- Si usás íconos o pictogramas de apoyo visual, que sean genéricos y neutros.
  Nunca uses un ícono que se parezca a un logo de una marca comercial
  conocida — ninguna marca comercial es parte de este contenido.

Tono: técnico pero accesible, con ejemplos concretos (no solo teoría
abstracta).

---

## 🔒 Trazabilidad interna — esto NO se pega en Gamma, es solo para auditar

- "[fragmento del contenido de arriba]" → sale de: `ejercicios-resueltos.html § Unidad N · ejercicio N.K` (o el archivo/sección real que corresponda)
- "[otro fragmento]" → sale de: `cuadernillo... Tutorial N.K`

## Checklist al revisar el resultado de Gamma (uso interno)
- ¿El PDF generado respeta el contenido real citado arriba, sin inventar datos
  o ejemplos que no estén respaldados por el material fuente?
- ¿No repite lo mismo que la Lectura PDF de esta actividad?
- ¿La extensión es razonable (ni una página vacía, ni un tocho de 30 páginas
  para una actividad puntual)?
```

## Después de generar el prompt

1. Guardar el `.md` en `Actividades/actividad-N/material-apoyo/`.
2. Marcar `material_apoyo.prompts[K].prompt_status: generado` en `estado.yml`.
3. Revisar el `.env` de la raíz de la skill (no lo leas vos con tus herramientas
   de archivo — Read/Edit sobre `.env*` están bloqueados por política global;
   simplemente corré el script y dejá que él lo lea): si `GAMMA_AUTOMATIZADO=true`,
   corré directo `scripts/gamma_generate.py` (ver sección de abajo) sin
   preguntarle nada al usuario — la máquina ya está configurada para eso. Si
   no existe `.env` o `GAMMA_AUTOMATIZADO=false` (default), avisale al usuario
   que el prompt está listo para correr en Gamma a mano — aclarando que solo
   debe copiar el bloque delimitado como "PROMPT LISTO PARA GAMMA", no el
   archivo entero. En los dos casos, no se sigue con `lectura_pdf` de esa
   actividad hasta que el contenido del material de apoyo esté decidido/generado
   (no hace falta esperar a que lo suba a Moodle, solo a que el contenido esté
   definido, para poder coordinar la Lectura PDF sin pisarlo).
4. Cuando el usuario confirme que subió el PDF real a la carpeta de Moodle,
   marcar `pdf_subido_por_usuario: true`.

## Generación automatizada opcional (API de Gamma)

Requiere que el usuario ya tenga una cuenta Gamma paga y haya corrido
`python scripts/configurar.py` una vez en esta máquina para dejar
`GAMMA_API_KEY` y `GAMMA_AUTOMATIZADO=true` en el `.env` de la raíz de la
skill (ver `env.example` para el resto de las variables). Ese script pide la
key con `getpass` — nunca se la pidas vos al usuario por el chat, ni la
hardcodees en ningún script: `scripts/gamma_generate.py` la toma sola desde
`.env` vía `python-dotenv`. Si el usuario no corrió `configurar.py` o eligió
no activarlo, seguí con el camino manual de siempre — esto es un atajo
opcional, no un requisito, y la propia skill no puede leer ni escribir el
`.env` para forzarlo (bloqueo de seguridad global sobre archivos `.env*`).

- **Uso**: `scripts/gamma_generate.py` lee el bloque "PROMPT LISTO PARA GAMMA"
  del `.md` ya escrito (la misma extracción que haría un humano al copiar/
  pegar) y llama a `POST /v1.0/generations` de la API de Gamma — **nunca**
  `POST /v1.0/generations/from-template`: ese segundo endpoint está pensado
  para adaptar una plantilla de **una sola página**, no para generar un
  documento nuevo de varias páginas — con una plantilla real (multi-página)
  produce documentos cortos, sin portada real, y puede arrastrar contenido
  viejo de la plantilla que no se puede corregir por prompt.
  ```
  python scripts/gamma_generate.py \
      --prompt-file "Actividades/actividad-2/material-apoyo/prompt-gamma-2-1.md" \
      --titulo "Material de apoyo - Actividad 2" \
      --salida "Actividades/actividad-2/material-apoyo/material-apoyo-2-1.pdf"
  ```
- **Calibrá `--num-cards`/`--text-amount` al volumen real del contenido
  fuente, no a un número fijo**: para material núcleo con buen desarrollo de
  fuente (varios puntos ricos en `## PROMPT LISTO PARA GAMMA`), `--num-cards
  10 --text-amount detailed` da un documento denso y fiel. Para material
  acotado u opcional (2-3 puntos breves, como una profundización optativa),
  bajá a `--num-cards 6 --text-amount medium` o menos — forzar siempre 10
  páginas sobre contenido delgado empuja al modelo a inventar ejemplos
  propios para rellenar, justo lo que la Regla dura #1 prohíbe. Si el prompt
  original ya sugiere una extensión acotada ("no hace falta estirarlo"),
  respetala.
- **Riesgo residual conocido, no bloqueante**: el pie de página con el nombre
  de la materia (pedido arriba en "Reglas de formato obligatorias") no sale
  garantizado al 100% en todas las páginas — a veces Gamma usa ese espacio
  para una etiqueta de sección en su lugar. No es el error original (nunca
  puso el nombre de OTRA materia), pero tampoco es 100% consistente entre
  corridas. Por eso el resultado se sigue revisando página por página antes
  de subirlo, igual que con el camino manual.
- El script no cambia qué contenido lleva el prompt ni quién lo redacta —
  siguen valiendo las Reglas duras #1 y #2 de arriba tal cual. Una vez
  corrido, sigue haciendo falta que el usuario revise el PDF resultante antes
  de darlo por bueno y confirmar `pdf_subido_por_usuario: true`.
