# NotebookLM por actividad — spec y guion fuente

NotebookLM no tiene API pública: **no se automatiza la creación del notebook**. Lo
que la skill entrega es el **guion/fuente** listo para que el usuario lo pegue como
fuente en NotebookLM y genere los 5 materiales él mismo, en unos minutos.

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
[Lista de los PDFs/videos/links que ya tiene la actividad, para que el usuario los
suba también como fuente en el mismo notebook]
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
quedó `pegado: true` (ver `estado-yml-schema.md`).
