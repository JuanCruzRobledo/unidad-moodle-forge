# NotebookLM por actividad — spec y guion fuente

NotebookLM no tiene API pública: **no se automatiza la creación del notebook**. Lo
que la skill entrega es el **guion/fuente** listo para que el usuario lo pegue como
fuente en NotebookLM y genere los 5 materiales él mismo, en unos minutos.

## Gate: cuándo tiene sentido generar esto

Este paquete de fuentes lista archivos reales de la actividad (el PDF de
Lectura, el/los PDF(s) de Material de apoyo, y los 3 guiones de video). No tiene
sentido generarlo antes de que esos archivos existan — estarías documentando
fuentes que todavía no están. **No generar el guion de NotebookLM de una
actividad hasta que**, para esa misma actividad:

- `material_apoyo.prompts[]` tenga al menos un ítem `prompt_status: generado`
  (ver `prompt-gamma-material-apoyo.md`) — o esté explícitamente vacío porque
  esa actividad no tiene material de apoyo real.
- `lectura_pdf.documento_html_status: generado` como mínimo (ver
  `plantilla-pdf-lectura.md`) — no hace falta esperar al PDF confirmado, alcanza
  con que el documento ya esté escrito.
- Los 3 `videos[].guion_status` estén en `generado` (ver
  `automatizacion-videos-actividad.md`) — no hace falta que estén renderizados,
  el guion ya sirve como transcripción exacta.

Si el usuario pide el guion de NotebookLM antes de que se cumpla esto, avisale
qué falta en vez de generar un paquete de fuentes incompleto.

## Configuración exacta a usar por tipo de material (según la cátedra)

| Material | Configuración a elegir en NotebookLM |
|---|---|
| Resumen de video | Video explicativo · idioma español latino · estilo clásico |
| Resumen de audio | Formato Breve · idioma español latino |
| Infografía | Idioma español latino · orientación horizontal · nivel de detalle: detallado |
| Presentación | Presentación Detallada · idioma español latino · duración predeterminada |
| Tarjetas didácticas | Número de tarjetas: Standard · dificultad: media |

Después de generar la infografía, comprimirla antes de subirla al aula con
https://www.iloveimg.com/es/comprimir-imagen (el aula real usa imágenes livianas para
que el modal cargue rápido).

## Plantilla de guion fuente por actividad

Generá un archivo `guion-actividad-N.md` con esta estructura — es lo que el usuario
pega como fuente en NotebookLM (además de los PDFs/videos que ya tenga la actividad):

```markdown
# Guion fuente — Actividad [N]: [NOMBRE DE LA ACTIVIDAD]

## Tema
[Tema principal de la actividad, en 1-2 líneas]

## Conceptos clave a cubrir
- [Concepto 1]: [definición/explicación breve]
- [Concepto 2]: [definición/explicación breve]
- [Concepto 3]: [definición/explicación breve]

## Ejemplos de aplicación
[1-2 ejemplos concretos que ilustren los conceptos — código, casos de uso, o
ejercicios resueltos, según la materia]

## Errores comunes / puntos de confusión
[Lo que suele confundir a los estudiantes en este tema, para que el resumen de
audio/video y las tarjetas los aborden explícitamente]

## Fuentes adicionales
Subí estos archivos reales como fuente en el mismo notebook, además de este guion:
- `documento-lectura-actividad-N.pdf` (Lectura obligatoria de la actividad)
- [Cada PDF de Material de apoyo ya generado en Gamma y subido por el usuario —
  listar los nombres reales de `material_apoyo.prompts[]`]
- `guion-video-actividad-N-1.md`, `guion-video-actividad-N-2.md`,
  `guion-video-actividad-N-3.md` (transcripción exacta de cada video — el TTS de
  HyperFrames los lee literal, así que sirven como transcripción sin necesidad
  de transcribir el `.mp4` renderizado)
```

**Regla dura**: el contenido de "Conceptos clave", "Ejemplos" y "Errores comunes" se
completa a partir del material real que aportó el usuario (apuntes, programa,
PDFs) — nunca se inventa un tema que no esté respaldado por lo que el docente trajo.
Si falta ese material para una actividad puntual, preguntale al usuario antes de
generar el guion.

## Después de que el usuario genera el notebook

Pedile la URL real (`https://notebooklm.google.com/notebook/<uuid>`) y reemplazá el
placeholder `URL_IA_NOTEBOOKLM` de la tarjeta "Asistente IA" en el HTML de la
actividad correspondiente. Marcá en `estado.yml` que el NotebookLM de esa actividad
quedó `notebooklm.link_pegado: true` (ver `estado-yml-schema.md`).
