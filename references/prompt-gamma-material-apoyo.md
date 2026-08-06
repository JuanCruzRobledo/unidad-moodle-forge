# Prompt para Gamma — Material de apoyo por actividad

## Qué resuelve esto

En el aula real, cada actividad tiene una carpeta Moodle **"Material de apoyo –
Actividad N"** (un recurso tipo Carpeta) que hoy queda siempre vacía — la skill
nunca generó nada para ese lugar, y quedó documentado como pendiente en las
bitácoras de importación de Unidad 2 a 5.

[Gamma](https://gamma.app) es una herramienta externa que arma documentos/PDFs
con diseño vía IA a partir de un prompt de texto. No tiene API pública, así que
—igual que con NotebookLM (ver `notebooklm-guion.md`)— **el entregable de la
skill acá es el texto del prompt, nunca el PDF en sí**: el usuario corre el
prompt en Gamma a mano, revisa el resultado, lo descarga y lo sube él mismo a la
carpeta real de Moodle.

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

## Regla dura: no inventar contenido

El prompt se arma **citando y resumiendo el material real** que ya se usó para
esa actividad — nunca un tema genérico "de relleno" para completar la carpeta.
Si el material fuente disponible no alcanza para justificar un documento de
apoyo con contenido real, no se genera un prompt vacío: se avisa que no hay
material de apoyo claro para esa actividad y se deja `material_apoyo.prompts: []`
en `estado.yml`, documentado como tal en el reporte de pendientes.

## Plantilla del prompt (`Actividades/actividad-N/material-apoyo/prompt-gamma-N-K.md`)

```markdown
# Prompt para Gamma — Material de apoyo K: [Nombre del documento]

## Instrucción para Gamma (pegar esto tal cual en el prompt de Gamma)

Generá un documento PDF de apoyo académico en español, para estudiantes de
[nombre de la materia] en la Tecnicatura Universitaria en Programación (TUP,
UTN), sobre el siguiente tema: [tema puntual del documento].

Estructura esperada:
1. [Sección 1 — ej. "Contexto y por qué importa"]
2. [Sección 2 — ej. "Desarrollo con ejemplos concretos"]
3. [Sección 3 — ej. "Casos resueltos paso a paso"]
4. [Sección de cierre — ej. "Errores comunes a evitar"]

Tono: técnico pero accesible, con ejemplos concretos (no solo teoría abstracta).
Extensión aproximada: [N] páginas. No repitas contenido genérico de internet —
basate estrictamente en los puntos de contenido que te doy abajo.

## Contenido real a partir del cual Gamma debe construir el documento
(esto es lo que evita que Gamma invente o generalice de más — pegale estos
puntos como contexto adicional en Gamma si lo permite, o dejalos como guía para
vos al revisar el resultado)

- [Punto de contenido 1, con su fuente real: "ejercicios-resueltos.html §
  Unidad N · ejercicio N.K" o "cuadernillo_agentes_ia... Tutorial N.K"]
- [Punto de contenido 2, con su fuente]
- [Punto de contenido 3, con su fuente]

## Qué NO debe cubrir este documento
(para no solaparse con `documento-lectura-actividad-N.html`, que cubre el
contenido núcleo/obligatorio de la actividad)

- [Lo que ya va a estar en la Lectura PDF, para que Gamma no lo repita]

## Checklist al revisar el resultado de Gamma
- ¿El PDF generado respeta los puntos de contenido reales de arriba, sin
  inventar datos o ejemplos que no estén respaldados por el material fuente?
- ¿No repite lo mismo que la Lectura PDF de esta actividad?
- ¿La extensión es razonable (ni una página vacía, ni un tocho de 30 páginas
  para una actividad puntual)?
```

## Después de generar el prompt

1. Guardar el `.md` en `Actividades/actividad-N/material-apoyo/`.
2. Marcar `material_apoyo.prompts[K].prompt_status: generado` en `estado.yml`.
3. Avisarle al usuario que el prompt está listo para correr en Gamma — no se
   sigue con `lectura_pdf` de esa actividad hasta que el usuario confirme que
   ya decidió/generó el material de apoyo (no hace falta esperar a que lo suba
   a Moodle, solo a que el contenido esté definido, para poder coordinar la
   Lectura PDF sin pisarlo).
4. Cuando el usuario confirme que subió el PDF real a la carpeta de Moodle,
   marcar `pdf_subido_por_usuario: true`.
