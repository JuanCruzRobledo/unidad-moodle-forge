# Imagen de banner de Introducción — generación con nanobanana

## Qué resuelve esto

El primer bloque de cada unidad (`Introduccion/00-descripcion-seccion.html`, ver
`plantillas-html.md` § Banner de introducción de unidad) trae un
`<img src="URL_DE_LA_IMAGEN">` debajo del título. Hasta ahora ese placeholder
quedaba sin resolver en toda unidad generada desde cero — no había forma de
producir la imagen real sin depender de que el usuario la subiera a mano. Esta
referencia cierra ese hueco usando el MCP `gemini-nanobanana-mcp`
(`mcp__gemini-nanobanana-mcp__generate_image`), ya reservado para este uso
puntual (ver la nota en `plantillas-html.md` § Cuerpo para cada actividad: la
infografía de cada actividad sale de NotebookLM Studio, **nunca** de
nanobanana — nanobanana es solo para este banner).

## Estilo validado contra el aula real

Contrastado en vivo navegando varias unidades de un curso real de la TUP
(`tup.sied.utn.edu.ar/course/view.php?id=82`, Programación III — unidades
HTML, CSS y JavaScript, sin tocar ni editar nada de ese curso, solo lectura).
Patrón consistente en las tres:

- **Fondo plano de un solo color sólido**, sin gradiente ni textura — cada
  unidad usa un color distinto (visto: azul para HTML, coral/salmón para CSS,
  amarillo para JavaScript).
- **1 a 3 elementos vectoriales flat** relacionados con el tema concreto de la
  unidad — no genéricos: un ícono de monitor con `</>`, el logo real de la
  tecnología cuando existe uno reconocible (ej. el logo oficial de JS), un
  ícono de documento. Estilo *flat design*, sin sombras marcadas, sin
  degradados, sin efecto 3D ni fotorrealismo.
- **Sin texto/letras dentro de la imagen.** El título real (`NOMBRE DE LA
  MATERIA – UNIDAD / TEMA`) ya va arriba, en el `<h1>` de la plantilla — la
  imagen es puramente ilustrativa. Los modelos de generación de imagen suelen
  destrozar el texto que se les pide dibujar, así que ni se lo pedimos.
- Composición limpia, harto espacio negativo, buen contraste entre los íconos
  y el fondo — se ve bien tanto grande (banner) como achicado (thumbnail del
  curso).

**No es un estilo 100% uniforme entre unidades del curso de referencia** (la
de HTML usaba además una figura humana isométrica; CSS/JS no) — lo que sí es
constante es el patrón fondo-sólido + íconos-flat-sin-texto. Esta referencia
formaliza esa constante, no una ilustración calcada 1:1 de una unidad puntual.

## Derivar los 1-3 elementos visuales del tema real

**Nunca uses un ícono genérico de "laptop con código" para todo.** Mirá el
tema concreto de la unidad (el nombre de la unidad + sus resultados de
aprendizaje ya redactados en el punto 1 de Fase 1) y elegí 1 a 3 elementos que
lo representen de verdad. Ejemplos de este workspace (Metodología I/II, no son
lenguajes de programación con logo propio, así que hay que pensar el ícono en
vez de calcarlo):

| Tema de la unidad | Elementos posibles |
|---|---|
| Marco funcional / IA generativa | chip o cerebro estilizado, ventana de chat |
| Prompt engineering | globo de diálogo, cursor de terminal, engranaje |
| Agentes inteligentes (loop) | robot simple, flechas en bucle (observar→actuar) |
| Agentes especializados / orquestación | varios íconos de robot conectados por líneas (DAG) |
| Spec-Driven Development | documento con checklist, plano/blueprint |
| MCP y automatización | enchufe/conector, engranajes encadenados |
| Orquestación / CI-CD | flujo de cajas conectadas, check verde |
| Calidad y responsabilidad | balanza, lupa sobre documento |

Si la unidad sí trata una tecnología con logo oficial reconocible y libre de
uso (ej. una unidad de un lenguaje o framework puntual en otra materia), se
puede incluir ese logo real como uno de los elementos — igual que el curso de
referencia usa el logo real de JS. Si no hay un logo así, no inventes uno que
se parezca a la marca de una empresa real (mismo riesgo ya documentado para
Gamma en `prompt-gamma-material-apoyo.md`: un ícono libre elegido sin cuidado
puede terminar pareciéndose a un logo comercial existente sin que nadie lo
haya pedido).

## Paleta rotativa por unidad

Para que las unidades de una misma materia se vean distintas entre sí sin
quedar disonantes con el resto de la plantilla (navy `#001855` del título,
blanco del texto), rotá por esta paleta usando `(numero_de_unidad - 1) % 8`:

| Índice | Hex | Nombre |
|---|---|---|
| 0 | `#2A9D8F` | Teal |
| 1 | `#E76F51` | Terracota |
| 2 | `#F4A261` | Ámbar |
| 3 | `#457B9D` | Azul acero |
| 4 | `#E9C46A` | Mostaza |
| 5 | `#6A4C93` | Violeta |
| 6 | `#EF476F` | Magenta |
| 7 | `#06A77D` | Verde esmeralda |

Si dos unidades consecutivas de la reestructuración quedan fusionadas o
renumeradas (ver "Reestructuración de Metodología I" en el `CLAUDE.md` del
workspace), rotá igual por el número final de unidad — no hace falta
preservar el color que tenía la unidad vieja antes de fusionarse.

## Plantilla del prompt para nanobanana

```
Ilustración vectorial flat design para el banner de una unidad universitaria.
Fondo sólido de un único color plano, hex {COLOR_HEX}, sin gradientes ni
texturas. En el centro, componé de forma equilibrada estos elementos en estilo
flat/vector minimalista, sin sombras marcadas, sin efecto 3D, sin
fotorrealismo: {ELEMENTOS_VISUALES}. Los elementos van en blanco, negro o un
color de acento que contraste bien contra el fondo. Mucho espacio negativo
alrededor, composición limpia y equilibrada, apta para achicarse a thumbnail
sin perder legibilidad. IMPORTANTE: no incluyas ningún texto, letra, palabra
ni número dentro de la imagen. No uses logos ni íconos que se parezcan a la
marca de una empresa comercial real, salvo que se pida explícitamente un logo
oficial de tecnología libre de uso. Composición cuadrada (proporción 1:1),
con los elementos centrados dejando margen parejo en los cuatro bordes.
```

Completá `{COLOR_HEX}` con la paleta de arriba y `{ELEMENTOS_VISUALES}` con
los 1-3 elementos concretos del tema (ver tabla de arriba), descriptos en una
frase corta cada uno (ej. "un robot simple de líneas limpias", "un documento
con una lista de tareas tildadas", "dos flechas formando un ciclo").

## Tamaño final: 600×600px exactos

El archivo que termina en `Introduccion/imagen-banner-introduccion.png` tiene
que quedar en **600×600 píxeles exactos** — tamaño definido por el usuario
para esta imagen puntual (no un default de la skill para otro tipo de
imagen). **No confíes en que el modelo lo devuelva ya en ese tamaño**:
confirmado en vivo que aunque el prompt pida composición cuadrada, nanobanana
(vía OpenRouter) puede devolver otra resolución cuadrada distinta (ej.
1024×1024) sin avisar. Por eso el tamaño se **fuerza siempre** como paso
aparte después de generar, nunca se da por bueno el archivo tal cual sale del
modelo — ver el paso 2 de "Después de generar la imagen" más abajo.

## Invocación

```
mcp__gemini-nanobanana-mcp__generate_image
  prompt: <prompt completado de la plantilla de arriba, sin superar 2000 caracteres>
  saveToFilePath: "<carpeta de la unidad>/Introduccion/imagen-banner-introduccion.png"
```

Guardá el archivo dentro de la carpeta de la unidad, nunca fuera de ella —
igual que el resto de los assets generados por la skill.

## Si el MCP no está disponible en esta instalación

`gemini-nanobanana-mcp` es un MCP externo, no algo que la skill controle o
verifique por `.env` (a diferencia de Gamma en Fase -1). Si al intentar la
tool call no está disponible o falla, no lo reintentes en loop: avisale al
usuario, dejá `URL_DE_LA_IMAGEN` como placeholder tal cual, y ofrecele el
prompt ya completado (de la plantilla de arriba) para que lo corra a mano en
cualquier herramienta de generación de imagen que tenga a mano — el resultado
se guarda igual en `Introduccion/imagen-banner-introduccion.png` y se sigue el
resto del flujo normal.

## Después de generar la imagen

1. Guardá el archivo en `Introduccion/imagen-banner-introduccion.png` (o la
   extensión que devuelva la tool).
2. **Forzá el tamaño a 600×600px** corriendo
   `python scripts/resize_imagen_banner.py --entrada "<ruta>/Introduccion/imagen-banner-introduccion.png"`
   (sobrescribe el mismo archivo con un recorte centrado + resize a 600×600).
   Este paso es obligatorio siempre, no solo cuando el archivo "se ve" de otro
   tamaño — no lo saltees asumiendo que el modelo ya devolvió 600×600.
3. Marcá `introduccion.imagen_banner.status: generado` y completá
   `introduccion.imagen_banner.ruta` en `estado.yml` (ver
   `references/estado-yml-schema.md`).
4. **Mostrale la imagen al usuario y esperá su confirmación** antes de pasar
   `status` a `confirmado` — mismo principio de revisión que el resto de la
   skill (Práctica, Lectura PDF, Material de apoyo): generar es barato,
   publicar algo que no queda bien es más caro de deshacer. Si no convence,
   volvé a generar ajustando el prompt (otro elemento visual, otro color)
   antes de seguir — igual corré de nuevo el resize del paso 2 sobre el nuevo
   archivo.
5. El `src="URL_DE_LA_IMAGEN"` del HTML **no se resuelve todavía** en este
   paso — sigue siendo un placeholder hasta la Fase 8 (Importación), donde se
   sube el archivo real a Moodle y se reemplaza por la URL real (ver
   `references/importacion-moodle.md` § 9e).

## Actualizar un componente que ya está vivo en el aula (retrofit / regeneración)

Si la unidad ya tiene una imagen real subida en el aula (Fase 9, retrofit, o
el usuario pide explícitamente regenerar el banner de una unidad ya
importada), **no la reemplaces de oficio**: preguntale al usuario si quiere
conservar la imagen actual (copiándole la URL existente antes de tocar nada,
como indica la nota en `plantillas-html.md`) o generar una nueva con este
flujo. Nunca asumas que "más nuevo es mejor" sobre contenido que un docente ya
aprobó y publicó.
