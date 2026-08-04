# Plantillas HTML oficiales por sub-sección

Fuente: "Plantillas aula virtual - 2026" (PDF de cátedra). Texto completo original en
`assets/plantilla-oficial-extraida.txt`. Estos bloques ya están contrastados contra el
aula real (curso Programación 3, TUP) — coinciden 1:1.

**Regla de uso**: completá los placeholders en MAYÚSCULAS o entre `[corchetes]`
manteniendo estructura, estilos e IDs exactos. No elimines, resumas ni fusiones
bloques — cada `<div>`, lista o script se conserva tal cual, solo cambia el contenido.
Donde el bloque trae un comentario `<!-- ... -->` que es una instrucción para quien
arma la plantilla (no para el HTML final), quitalo al usar el bloque.

**Convención de generación — un archivo por bloque, nunca un HTML concatenado.**
Confirmado recorriendo el aula real (ver `references/estructura-aula-real.md` y
`references/importacion-moodle.md`): cada `<div>` de nivel superior de esta
referencia es un componente independiente en Moodle, no un fragmento de una misma
página. Por eso cada bloque se genera como su **propio archivo `.html`**, nunca
concatenado con los demás bloques de la misma sub-sección:

- El **primer bloque** de cada sub-sección (el banner grande con el título) es el
  campo **Descripción** de esa sección/sub-sección de Moodle — se edita en
  `course/editsection.php`, **no es un Label**. Se genera siempre como
  `00-descripcion-seccion.html`.
- **Cada bloque siguiente es un Label independiente** (`mod_label`) — se genera
  como `01-<slug>.html`, `02-<slug>.html`, ... en el mismo orden en que aparecen
  en esta referencia.
- **Única excepción**: el bloque "Cuestionario de la Actividad" (dentro de
  Actividades) no es un Label — va en el campo **Descripción** del `mod_quiz`
  correspondiente. Se genera aparte, como `cuestionario-actividad-N.html`.

Cada encabezado de bloque de acá abajo trae una nota `→` con el nombre de archivo
que le corresponde y su destino real en Moodle.

---

## Introducción

### Banner de introducción de unidad (resultados de aprendizaje)

→ `00-descripcion-seccion.html` — Descripción de la sección raíz de la unidad (`editsection.php`), **no es un Label**.

```html
<div style="background-color: #ffffff; border: 1px solid #ccc; padding: 30px; border-radius: 12px;
box-shadow: 0 4px 10px rgba(0,0,0,0.05); margin-bottom: 30px; font-family: 'Segoe UI', sans-serif;">
  <div style="text-align: center; margin-bottom: 20px;">
    <h1 style="font-size: 2rem; margin-bottom: 10px; background-color: #001855; color: #ffffff;
    padding: 15px; border-radius: 8px; font-family: sans-serif;">
      NOMBRE DE LA MATERIA – UNIDAD / TEMA
    </h1>
    <img class="img-fluid" src="URL_DE_LA_IMAGEN" alt="Descripción de la imagen relacionada con la materia"
      style="margin-top: 15px; border-radius: 8px; max-width: 100%; height: auto;">
    <h2 style="color: #2c3e50; font-size: 1.5rem; margin-top: 20px; font-family: sans-serif;">
      <strong style="color: #001855;">Resultados de Aprendizaje</strong>
    </h2>
  </div>
  <ul style="color: #2c3e50; font-size: 1.1rem; line-height: 1.8; padding-left: 25px; margin-top: 20px;">
    <li><strong>Resultado 1:</strong> Descripción clara y concreta del aprendizaje esperado.</li>
    <li><strong>Resultado 2:</strong> Descripción clara y concreta del aprendizaje esperado.</li>
    <li><strong>Resultado 3:</strong> Descripción clara y concreta del aprendizaje esperado.</li>
    <li><strong>Resultado 4:</strong> Descripción clara y concreta del aprendizaje esperado.</li>
    <li><strong>Resultado 5:</strong> Descripción clara y concreta del aprendizaje esperado.</li>
  </ul>
</div>
```

Nota: la URL de la imagen se copia del componente que se está actualizando (el link
existente) antes de reemplazarlo — no se inventa una nueva.

### Video de introducción a la unidad (colapsable)

→ `01-video-introduccion.html` — Label independiente.

```html
<div style="margin-bottom: 30px; font-family: 'Segoe UI', sans-serif; border: 1px solid #ccc;
border-radius: 12px; background-color: #ffffff; box-shadow: 0 4px 10px rgba(0,0,0,0.05);">
  <details>
    <summary style="cursor: pointer; padding: 20px; font-size: 1.2rem; font-weight: bold; color: #004173;">
      Introducción a [NOMBRE DE LA UNIDAD] (haz clic para ver)
    </summary>
    <div style="padding: 30px; text-align: center;">
      <iframe title="Introducción a [NOMBRE DE LA UNIDAD]" src="URL_DEL_VIDEO_YOUTUBE"
        width="560" height="315" frameborder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
        allowfullscreen="allowfullscreen" referrerpolicy="strict-origin-when-cross-origin"
        style="max-width: 100%; border-radius: 8px;"></iframe>
    </div>
  </details>
</div>
```

### Sección antes del foro de la unidad

→ `02-banner-foro.html` — Label independiente.

```html
<div style="background: linear-gradient(to right, #fff6e5, #ffe9cc); width: 100%; padding: 30px;
border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.06); margin-bottom: 30px;
font-family: 'Segoe UI', sans-serif; border-left: 6px solid #f4a261;">
  <div style="text-align: center;">
    <h1 style="font-size: 1.7rem; color: #8b4513; margin: 0; font-family: sans-serif;">
      <a style="text-decoration: none; color: #8b4513;" href="URL_DEL_FORO">
        <strong>Foro de Consultas – [NOMBRE DE LA UNIDAD]</strong>
      </a>
    </h1>
  </div>
</div>
```

### Hoja de ruta de la unidad (con tabla Pomodoro)

→ `03-hoja-de-ruta.html` — Label independiente.

```html
<div style="background-color: #faf5f8; border: 1px solid #ccc; padding: 30px; border-radius: 12px;
box-shadow: 0 4px 10px rgba(0,0,0,0.05); font-family: 'Segoe UI', sans-serif; margin-bottom: 30px;">
  <div style="text-align: center; margin-bottom: 20px;">
    <h4 style="font-size: 1.8rem; color: #27ae60; text-align: center; margin-top: 20px; font-family: sans-serif;">
      UNIDAD [NÚMERO]: [NOMBRE DE LA UNIDAD]
    </h4>
  </div>

  <p style="line-height: 1.8; color: #2c3e50; font-size: 1.1rem; margin-bottom: 25px;">
    En esta unidad te introducirás a <strong>[TEMA GENERAL]</strong>, abordando los fundamentos de
    <strong>[CONTENIDOS PRINCIPALES]</strong>. El objetivo es que comprendas los conceptos clave
    antes de avanzar a la práctica integradora.
  </p>

  <h4 style="color: #27ae60; font-size: 1.5rem; margin-bottom: 15px; font-family: sans-serif;">
    ¿Cómo vas a trabajar esta unidad?
  </h4>
  <p style="font-size: 1.1rem; line-height: 1.8; margin-bottom: 15px;">
    A continuación, te presentamos el <strong>recorrido de aprendizaje</strong>. La unidad se
    organiza en secciones de <strong>validación de conocimientos</strong>, donde accederás a
    materiales, videos y cuestionarios. Al finalizar, integrarás todo en un
    <strong>Trabajo Práctico</strong>.
  </p>

  <h4 style="color: #27ae60; font-size: 1.5rem; margin-bottom: 15px; font-family: sans-serif;">
    Hoja de ruta – Unidad [NÚMERO]
  </h4>
  <ol style="font-size: 1.1rem; line-height: 1.8; padding-left: 25px; color: #2c3e50; margin-bottom: 25px;">
    <li><strong>Sección 1:</strong> [Tema]. Descripción breve + evaluación asociada.</li>
    <li><strong>Sección 2:</strong> [Tema]. Descripción breve + evaluación asociada.</li>
    <li><strong>Sección 3:</strong> [Tema]. Descripción breve + evaluación asociada.</li>
    <li><strong>Sección 4:</strong> [Tema]. Descripción breve + evaluación asociada.</li>
    <li><strong>Trabajo Práctico Integrador:</strong> Aplicación global de los contenidos aprendidos.</li>
  </ol>

  <div style="background-color: #f0f8f0; padding: 20px; border-radius: 10px; margin-bottom: 25px;
  border-left: 5px solid #27ae60;">
    <h4 style="color: #27ae60; font-size: 1.3rem; margin-bottom: 15px; margin-top: 0; font-family: sans-serif;">
      Distribución del tiempo con Técnica Pomodoro
    </h4>
    <p style="font-size: 1.05rem; color: #2c3e50; line-height: 1.7; margin-bottom: 15px;">
      Te recomendamos usar la <strong>técnica Pomodoro</strong> (25 min de estudio + 5 min de
      descanso) para maximizar tu concentración durante las sesiones de estudio y evaluación:
    </p>

    <!-- La tabla se completa RECIÉN al final, cuando ya se generaron todas las actividades y se
         conocen los tiempos reales de video/lectura/práctica de cada una. No completar antes. -->
    <table style="width: 100%; border-collapse: collapse; font-size: 1rem;">
      <thead>
        <tr style="background-color: #27ae60; color: white;">
          <th style="padding: 12px; border: 1px solid #d0d0d0;">Actividad</th>
          <th style="padding: 12px; text-align: center; border: 1px solid #d0d0d0;">Videos</th>
          <th style="padding: 12px; border: 1px solid #d0d0d0; text-align: center;">Pomodoros</th>
          <th style="padding: 12px; border: 1px solid #d0d0d0; text-align: center;">Tiempo Est.</th>
        </tr>
      </thead>
      <tbody>
        <tr style="background-color: #ffffff;">
          <td style="padding: 10px; border: 1px solid #d0d0d0;">
            <strong>Actividad 1</strong><br><span style="font-size:0.9rem;">[Tema]</span>
          </td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">X min</td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">2</td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">40–50 min</td>
        </tr>
        <tr style="background-color: #f8f9fa;">
          <td style="padding: 10px; border: 1px solid #d0d0d0;"><strong>Trabajo Práctico</strong></td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">-</td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">4–5</td>
          <td style="padding: 10px; border: 1px solid #d0d0d0; text-align: center;">120 min</td>
        </tr>
      </tbody>
      <tfoot>
        <tr style="background-color: #27ae60; color: white; font-weight: bold;">
          <td style="padding: 12px; border: 1px solid #d0d0d0;">TOTAL UNIDAD</td>
          <td style="padding: 12px; border: 1px solid #d0d0d0; text-align: center;">Teoría + Práctica</td>
          <td style="padding: 12px; border: 1px solid #d0d0d0; text-align: center;">~[TOTAL]</td>
          <td style="padding: 12px; border: 1px solid #d0d0d0; text-align: center;">~[HORAS] hs</td>
        </tr>
      </tfoot>
    </table>
    <p style="font-size: 0.95rem; color: #6c757d; margin-top: 15px; font-style: italic;">
      Los tiempos son estimados. Es importante aprobar cada instancia antes de avanzar.
    </p>
  </div>

  <p style="font-size: 1.1rem; line-height: 1.8; color: #2c3e50;">
    <strong>Herramientas:</strong> Utilizá los recursos y asistentes disponibles en cada sección
    para reforzar tu aprendizaje.
  </p>
  <p style="font-size: 1.1rem; text-align: center; margin-top: 25px;"><strong>¡Éxitos en esta unidad!</strong></p>
</div>
```

---

## Actividades

### Banner principal de la sección

→ `Actividades/00-descripcion-seccion.html` — Descripción de la sub-sección Actividades, **no es un Label**. Se genera una sola vez por unidad (no por actividad).

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>Actividades – [NOMBRE DE LA UNIDAD]</strong>
  </h2>
</div>
```

### Cuerpo para cada actividad (con tarjetas Infografía / PDF / IA)

→ `Actividades/actividad-N/actividad-N.html` — Label independiente. Lleva **solo** este bloque `<details>` — el bloque "Cuestionario de la Actividad" (más abajo) NO va acá, va aparte.

```html
<details style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <summary style="color: #1565c0; font-size: 1.5em; cursor: pointer;">
    Actividad [Nº] – [NOMBRE DE LA ACTIVIDAD]
  </summary>

  <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin-top: 20px;
  border-left: 4px solid #ff9800;">
    <p style="margin: 0; font-size: 1rem; color: #e65100;">
      <strong>Tiempo estimado:</strong> [TIEMPO TOTAL] (Videos: [X] min + Lectura: [X] min + Práctica: [X] min)
    </p>
  </div>
  <br>

  <p style="font-size: 1rem;">
    En esta actividad explorarás <strong>[CONTENIDO PRINCIPAL]</strong>, comprendiendo sus
    conceptos fundamentales y su aplicación práctica.
  </p>

  <p style="font-size: 1rem;"><strong>Temas que abordaremos:</strong></p>
  <ul style="padding-left: 20px; font-size: 1rem;">
    <li>[Tema 1]</li>
    <li>[Tema 2]</li>
    <li>[Tema 3]</li>
  </ul>

  <p style="font-size: 1rem;">Estos recursos te ayudarán a consolidar los contenidos:</p>
  <ul>
    <li><a href="URL_VIDEO_1" target="_blank" rel="noopener">Video 1 – [Título]</a></li>
    <li><a href="URL_VIDEO_2" target="_blank" rel="noopener">Video 2 – [Título]</a></li>
    <li><a href="URL_VIDEO_3" target="_blank" rel="noopener">Video 3 – [Título]</a></li>
  </ul>

  <p style="font-size: 1rem; margin-top: 20px; border-bottom: 1px solid #edf2f7; padding-bottom: 15px;">
    <strong>Seleccioná un recurso para comenzar:</strong>
  </p>

  <!-- Tarjetas de recursos: mismo formato para todas las actividades. Solo cambiar [ID] (único
       por actividad dentro de la unidad, ej. "u1-a1") y las URLs. -->
  <div style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center; margin-top: 20px;">

    <div id="btn-infografia-[ID]" style="flex: 1 1 140px; max-width: 180px; background: white;
    border-radius: 12px; border: 1px solid #e6fffa; cursor: pointer;" tabindex="0" role="button">
      <div style="background-color: #e6fffa; height: 80px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 40px;"></span>
      </div>
      <div style="padding: 12px; text-align: center;">
        <h5 style="margin: 0; color: #00796b;">Infografía</h5>
        <span style="font-size: 0.8em;">Ver esquema</span>
      </div>
    </div>

    <details id="details-infografia-[ID]" style="border: none;">
      <summary style="display:none;"></summary>
      <div class="infografia-overlay" style="position: fixed; inset: 0; background: rgba(0,0,0,0.85);
      z-index: 99999; display: flex; align-items: center; justify-content: center;">
        <div style="background: white; border-radius: 10px; max-width: 900px; width: 100%;">
          <div style="padding: 10px; display: flex; justify-content: space-between;">
            <strong>Infografía – [NOMBRE ACTIVIDAD]</strong>
            <button id="btn-cerrar-infografia-[ID]" type="button">CERRAR</button>
          </div>
          <div style="padding: 10px; text-align: center;">
            <img src="URL_IMAGEN_INFOGRAFIA" alt="Infografía" style="max-width:100%;">
          </div>
        </div>
      </div>
    </details>
    <script>
      (function() {
        var details = document.getElementById('details-infografia-[ID]');
        var openBtn = document.getElementById('btn-infografia-[ID]');
        var closeBtn = document.getElementById('btn-cerrar-infografia-[ID]');
        var overlay = details ? details.querySelector('.infografia-overlay') : null;
        if (!details || !openBtn) return;
        function openModal() { details.setAttribute('open', ''); }
        function closeModal() { details.removeAttribute('open'); }
        openBtn.addEventListener('click', function(e) { e.preventDefault(); openModal(); });
        openBtn.addEventListener('keydown', function(e) {
          if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); openModal(); }
        });
        if (closeBtn) closeBtn.addEventListener('click', function(e) { e.preventDefault(); closeModal(); });
        if (overlay) overlay.addEventListener('click', function(e) { if (e.target === overlay) closeModal(); });
        document.addEventListener('keydown', function(e) {
          if (e.key === 'Escape' && details.hasAttribute('open')) closeModal();
        });
      })();
    </script>

    <a href="URL_PDF" target="_blank" rel="noopener" style="flex: 1 1 140px; max-width: 180px;
    background: white; border-radius: 12px; border: 1px solid #fff5f5;">
      <div style="background-color: #fff5f5; height: 80px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 40px;"></span>
      </div>
      <div style="padding: 12px; text-align: center;">
        <h5 style="margin:0;">Lectura PDF</h5>
        <span style="font-size:0.8em;">Material obligatorio</span>
      </div>
    </a>

    <!-- URL_IA queda como placeholder hasta que el usuario suba el Notebook a mano y devuelva el link real -->
    <a href="URL_IA_NOTEBOOKLM" target="_blank" rel="noopener" style="flex: 1 1 140px; max-width: 180px;
    background: white; border-radius: 12px; border: 1px solid #faf5ff;">
      <div style="background-color: #faf5ff; height: 80px; display: flex; align-items: center; justify-content: center;">
        <span style="font-size: 40px;"></span>
      </div>
      <div style="padding: 12px; text-align: center;">
        <h5 style="margin:0;">Asistente IA</h5>
        <span style="font-size:0.8em;">Repaso interactivo</span>
      </div>
    </a>
  </div>

  <p style="margin-top: 20px; background-color: #e3f2fd; padding: 10px; border-radius: 6px;">
    <strong>Código de apoyo:</strong><br>
    <a href="URL_CODIGO_1" target="_blank">Archivo 1</a><br>
    <a href="URL_CODIGO_2" target="_blank">Archivo 2</a>
  </p>

  <div style="text-align: center; margin-top: 25px;">
    <p style="font-size: 1.1rem; font-weight: bold;">¡Pasá de la teoría a la acción!</p>
  </div>
</details>
```

Link útil para comprimir la infografía antes de subirla: https://www.iloveimg.com/es/comprimir-imagen

### Cuerpo actividad lúdica (opcional)

→ `Actividades/actividad-ludica.html` — Label independiente.

```html
<details style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <summary style="color: #1565c0; font-size: 1.5em; cursor: pointer;">
    Actividad Lúdica – [NOMBRE DE LA ACTIVIDAD]
  </summary>

  <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin-top: 20px;
  border-left: 4px solid #ff9800;">
    <p style="margin: 0; font-size: 1rem; color: #e65100;">
      <strong>Tiempo estimado:</strong> [DURACIÓN] (tipo de recurso / actividad)
    </p>
  </div>
  <br>

  <p style="font-size: 1rem;">
    En esta actividad participarás de una experiencia <strong>[TIPO DE EXPERIENCIA]</strong> donde
    pondrás en práctica tus conocimientos sobre <strong>[CONTENIDO PRINCIPAL]</strong>. Deberás
    resolver desafíos y tomar decisiones para avanzar y completar la misión.
  </p>

  <p style="font-size: 1rem;"><strong>Contenidos que pondrás en juego:</strong></p>
  <ul style="padding-left: 20px; font-size: 1rem;">
    <li>[Contenido 1]</li>
    <li>[Contenido 2]</li>
    <li>[Contenido 3]</li>
  </ul>

  <p style="font-size: 1rem;"><strong>Objetivo:</strong><br>[DESCRIPCIÓN DEL OBJETIVO DE LA ACTIVIDAD].</p>

  <p style="font-size: 1rem; margin-top: 20px; border-bottom: 1px solid #edf2f7; padding-bottom: 15px;">
    <strong>Accedé a la actividad interactiva:</strong>
  </p>

  <!-- Recurso principal: iframe de Genially / H5P / video interactivo -->
  <div style="position: relative; padding-bottom: 56.25%; height: 0; border-radius: 12px; overflow: hidden;">
    <iframe title="[TÍTULO DEL RECURSO]" src="[URL_DEL_RECURSO]"
      style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"
      frameborder="0" scrolling="yes" allowfullscreen="allowfullscreen"></iframe>
  </div>

  <div style="text-align: center; margin-top: 25px;">
    <p style="font-size: 1.1rem; font-weight: bold;">
      [MENSAJE FINAL MOTIVADOR]<br>¡Aprender también puede ser una experiencia divertida!
    </p>
  </div>
</details>
```

### Descripción para cada cuestionario (igual para todos)

→ `Actividades/actividad-N/cuestionario-actividad-N.html` — va en el campo **Descripción** del `mod_quiz` "Cuestionario – Actividad N" (con "Mostrar descripción en la página del curso" activado), **no en el Label de la actividad**.

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h4 style="color: #1565c0; font-size: 1.5em; text-align: left; font-family: sans-serif;">
    Cuestionario de la Actividad
  </h4>
  <p style="font-size: 1rem; text-align: left;">
    ¡Bienvenido/a al Cuestionario de la Actividad! Este es tu momento para demostrar todo lo que
    has aprendido en esta actividad.
  </p>
  <p style="font-size: 1rem; text-align: left;"><strong>Algunas sugerencias para brillar:</strong></p>
  <ul style="padding-left: 20px; font-size: 1rem; line-height: 1.6;">
    <li>Repasa todos los temas de la unidad para estar bien preparado/a. ¡La práctica hace al maestro!</li>
    <li>Si no obtienes el resultado esperado, no te preocupes. Puedes volver a intentarlo y mejorar. ¡La perseverancia es clave!</li>
  </ul>
  <p style="font-size: 1rem; text-align: left;">¡Éxitos en este desafío! Estamos seguros de que lo harás increíble.</p>
</div>
```

---

## Trabajo Práctico / Práctica

### Banner principal de la sección

→ `Practica/00-descripcion-seccion.html` — Descripción de la sub-sección Práctica, **no es un Label**.

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>Trabajo Práctico – [NOMBRE UNIDAD]</strong>
  </h2>
</div>
```

### Descripción del Trabajo Práctico

→ `Practica/consigna-practica.html` — Label independiente (ver Fase 3 de `SKILL.md`: lleva **solo** este bloque `<details>`, sin el banner de arriba).

```html
<details style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <summary style="color: #1565c0; font-size: 1.5em; cursor: pointer;">
    Trabajo Práctico Integrador: [NOMBRE DEL PROYECTO] [EMOJI]
  </summary>
  <div style="background-color: #fff3e0; padding: 15px; border-radius: 8px; margin-top: 20px;
  border-left: 4px solid #ff9800;">
    <p style="margin: 0; font-size: 1rem; color: #e65100;">
      <strong>Tiempo estimado:</strong> [TIEMPO TOTAL] (Videos: [X] min + Desarrollo: [X] min)
    </p>
  </div>
  <br>
  <p style="font-size: 1rem; text-align: left;">
    ¡Llegó el momento de aplicar todo lo aprendido en la <strong>[UNIDAD]</strong>! En esta
    actividad integradora vamos a construir los <strong>[FOCO PRINCIPAL]</strong> de nuestro
    proyecto <strong>"[NOMBRE DEL PROYECTO]"</strong>. [ACLARACIÓN DE ALCANCE].
  </p>
  <p style="font-size: 1rem; text-align: left;"><strong>Consigna: Deberás entregar [CANTIDAD] archivo(s):</strong></p>
  <ul style="padding-left: 20px; font-size: 1rem; line-height: 1.6;">
    <li><strong>[ARCHIVO 1]:</strong> [DESCRIPCIÓN DEL CONTENIDO / ESTRUCTURA].</li>
    <li><strong>[ARCHIVO 2]:</strong> [DESCRIPCIÓN DEL CONTENIDO / ESTRUCTURA].</li>
    <li><strong>Navegación:</strong> [REQUISITO DE ENLACES / INTERACCIÓN].</li>
  </ul>
  <p style="font-size: 1rem; text-align: left;">
    Sigue estos tutoriales paso a paso para construir la estructura base del proyecto:
  </p>
</details>
```

Este bloque puede quedar breve (resumen + link al PDF descargable) en vez de repetir la
consigna completa palabra por palabra — la consigna completa vive en el documento con
membrete que se convierte a PDF (`references/plantilla-pdf-practica.md`). Sumale un link
directo al recurso:

```html
<p style="margin-top: 20px; background-color: #e3f2fd; padding: 10px; border-radius: 6px; text-align: center;">
  <a href="URL_PDF_DOCUMENTO_PRACTICA" target="_blank" rel="noopener" style="font-weight: bold;">
    📄 Descargar la consigna completa (PDF)
  </a>
</p>
```

### Descripción de la tarea de entrega — variante Programación 1 (Python, archivo único)

→ `Practica/entrega-practica.html` — Descripción de la Tarea (`mod_assign`) de entrega, mismo archivo para las 3 variantes de abajo (se usa la que corresponda a la carrera/materia).

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h5 style="color: #1565c0; text-align: left; font-size: 1.2rem; margin-top: 0; font-family: sans-serif;">
    Trabajo Práctico: [NOMBRE_TP]
  </h5>
  <p style="font-size: 1rem; text-align: left;">
    Resuelva los ejercicios propuestos en la guía utilizando únicamente <strong>Python</strong>.
    Asegúrese de aplicar correctamente los conceptos trabajados en la unidad.<br><br>
    La resolución deberá desarrollarse en un único archivo <code>.py</code>, verificando su
    correcto funcionamiento antes de la entrega.
  </p>
  <p style="font-size: 1rem; margin-top: 15px;"><strong style="color: #1565c0;">Formato de Entrega:</strong></p>
  <div style="background-color: #ffffff; border: 1px solid #1565c0; border-left: 4px solid #1565c0;
  padding: 15px; border-radius: 6px; margin-bottom: 15px;">
    <p style="margin-top: 0; font-size: 1rem; color: #1565c0;"><strong>Contenido del archivo .zip:</strong></p>
    <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; font-family: monospace;
    font-size: 0.95rem; color: #333; margin-bottom: 0; border: 1px solid #e0e0e0; line-height: 1.4;">
Apellido_Nombre_TP1.zip
 Apellido_Nombre_TP1.py</pre>
  </div>
  <ul style="padding-left: 20px; font-size: 1rem; line-height: 1.6;">
    <li>Entregar un único archivo con extensión <strong>.zip</strong>.</li>
    <li>El archivo <strong>.zip</strong> debe contener únicamente el archivo <code>.py</code> con la resolución.</li>
    <li>Nombre sugerido: <strong>Apellido_Nombre_[NOMBRE_TP].zip</strong>.</li>
    <li>Subir el archivo en la sección <strong>"Archivos enviados"</strong> del aula virtual.</li>
    <li>Verificar que el programa ejecute correctamente antes de comprimir y enviar.</li>
  </ul>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Consejo:</strong> Ejecute el archivo para comprobar que no presente errores. Revise la
    claridad del código y utilice nombres de variables significativos.
  </div>
</div>
```

### Descripción de la tarea de entrega — variante Programación 2 (Java, paquetes)

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-family: sans-serif; color: #1a237e; line-height: 1.6;">
  <h5 style="color: #1565c0; text-align: left; font-size: 1.2rem; margin-top: 0; font-family: sans-serif;">
    Trabajo Práctico: [NOMBRE_DEL_TP]
  </h5>
  <p style="font-size: 1rem; text-align: left;">
    Resuelve los <strong>ejercicios propuestos</strong> del práctico de <strong>[TEMA / UNIDAD]</strong>.
    El objetivo de esta actividad es que pongas en práctica los conceptos trabajados, organizando
    correctamente tu código y aplicando buenas prácticas.<br><br>
    Una vez finalizado el práctico, deberás comprimir tu proyecto y subirlo al aula virtual
    siguiendo las indicaciones de formato de entrega.
  </p>
  <p style="font-size: 1rem; text-align: left;"><strong>¡Anímate a completar la guía y demostrar lo que sabes!</strong></p>
  <p style="font-size: 1rem; margin-top: 15px;"><strong style="color: #1565c0;">Formato de Entrega:</strong></p>
  <div style="background-color: #ffffff; border: 1px solid #1565c0; border-left: 4px solid #1565c0;
  padding: 15px; border-radius: 6px; margin-bottom: 15px;">
    <p style="margin-top: 0; font-size: 1rem; color: #1565c0;">
      <strong>Estructura esperada del proyecto:</strong><br>
      Deberás separar la resolución de cada ejercicio en <strong>paquetes distintos</strong>. Cada
      paquete debe contener sus clases y su propio método <code>main</code> para poder ejecutarlo
      de manera independiente.
    </p>
    <pre style="background-color: #f8f9fa; padding: 15px; border-radius: 6px; font-family: monospace;
    font-size: 0.95rem; color: #333; margin-bottom: 0; border: 1px solid #e0e0e0; line-height: 1.4;">
[CARPETA_PRINCIPAL]/
 [Subcarpeta_01]/
  [Archivo1.ext]
  [Archivo2.ext]
 [Subcarpeta_02]/
  [Archivo3.ext]
  [Archivo4.ext]
 [...]</pre>
  </div>
  <ul style="padding-left: 20px; font-size: 1rem; line-height: 1.6;">
    <li>Comprimir la carpeta raíz del proyecto en un archivo con formato <strong>.zip</strong>.</li>
    <li>Nombre del archivo: <strong>Apellido_Nombre_TP_[NOMBRE_DEL_TP].zip</strong>.</li>
    <li>En el buzón de entrega, cargue el archivo en la sección <strong>"Archivos enviados"</strong>.</li>
    <li><strong>Importante:</strong> antes de comprimir, asegúrese de <strong>eliminar</strong>
      carpetas de archivos binarios o dependencias (<code>out/</code>, <code>bin/</code>,
      <code>target/</code>) para evitar archivos excesivamente pesados.</li>
  </ul>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Consejo:</strong> Verifique que el archivo comprimido contenga todos sus archivos de
    fuente (<code>.java</code>) organizados en sus respectivos paquetes antes de la entrega final.
  </div>
</div>
```

### Descripción de la tarea de entrega — variante Programación 3 (Java, estructura modular tipo Maven/Gradle)

Mismo bloque que Programación 2, pero la estructura esperada del `<pre>` sigue el patrón
de proyecto modular real visto en el aula:

```
[NOMBRE_DEL_PROYECTO]/
 src/
  main/
   java/
    [paquete_principal]/
     dtos/
      [NombreDTO].java
     entities/
      [EntidadBase].java
      [Entidad1].java
      [Entidad2].java
      [...]
     enums/
      [Enum1].java
      [Enum2].java
      [...]
     Main.java
   resources/
 build.gradle
 settings.gradle
```

El texto de "Estructura esperada del proyecto" para esta variante dice: "Deberás
organizar el código respetando una **estructura clara y modular**. Las clases y
componentes deben estar separados en **paquetes o carpetas según su
responsabilidad**, para mantener el proyecto ordenado."

### Descripción resolución propuesta del Trabajo Práctico

→ `Practica/resolucion-propuesta.html` — Label independiente, **opcional** (solo si se sube una carpeta ZIP con la resolución comparativa).

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
margin-bottom: 20px; font-family: 'Segoe UI', sans-serif; color: #1a237e;">
  <h5 style="color: #1565c0; font-size: 1.2rem; margin-top: 0; font-family: sans-serif;">
    <strong>Comparé tus soluciones con las propuestas</strong>
  </h5>
  <p style="font-size: 1.05rem; text-align: left; color: #333;">
    Una vez que hayas entregado tu trabajo práctico, te invitamos a revisar las soluciones
    propuestas. La resolución se encuentra disponible en una <strong>carpeta en formato ZIP</strong>
    ubicada junto a esta sección, para que puedas descargarla y consultarla.
  </p>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Recordá:</strong> la programación ofrece múltiples caminos para resolver un mismo
    problema. Comparar tu solución con otras propuestas te permitirá reflexionar, aprender nuevas
    estrategias y mejorar tu forma de resolver ejercicios.
  </div>
</div>
```

---

## Microteaching

### Banner principal de la sección

→ `Microteaching/00-descripcion-seccion.html` — Descripción de la sub-sección Microteaching, **no es un Label**.

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>Microteaching – [TÍTULO DEL TEMA]</strong>
  </h2>
</div>
```

### Tarjeta introductoria (Material de la Microteaching)

→ `Microteaching/01-material-microteaching.html` — Label independiente.

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
margin-bottom: 20px; width: 100%; font-family: sans-serif; color: #1a237e;">
  <h3 style="text-align: left; font-size: 1.4rem; color: #1565c0; margin-top: 0;">Material de la Microteaching</h3>
  <p style="font-size: 1.1rem; text-align: left;">
    En esta sección vas a encontrar el material correspondiente a la <strong>microteaching de esta
    unidad</strong>. ¡No te lo pierdas! Es tu oportunidad para estar al tanto de los temas que vamos
    a trabajar y llegar al encuentro súper preparado/a.
  </p>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Recomendación:</strong> Revisá el contenido con tiempo y anotá todas tus dudas. ¡Así
    aprovechamos al máximo el encuentro!
  </div>
</div>
```

### Sección de contenido y enlaces

→ `Microteaching/02-contenido-enlaces.html` — Label independiente.

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
margin-bottom: 20px; width: 100%; font-family: sans-serif; color: #1a237e;">
  <h3 style="text-align: left; font-size: 1.4rem; color: #1565c0; margin-top: 0; font-family: sans-serif;">
    Microteaching – [UNIDAD]: [NOMBRE DE LA UNIDAD/TEMA]
  </h3>
  <p style="font-size: 1.1rem; text-align: left;">[BREVE DESCRIPCIÓN DEL VIDEO O CONTENIDO DE LA CLASE].</p>
  <p style="font-size: 1.1rem; text-align: left;">
    <strong>Accedé al video desde este enlace:</strong><br>
    <a href="[URL_VIDEO_MICROTEACHING]" target="_blank" rel="noopener" style="color: #1565c0; font-weight: bold;">
      Video Microteaching
    </a>
  </p>
  <p style="font-size: 1.1rem; text-align: left;">
    <strong>Descargá el código fuente desde este enlace:</strong><br>
    <a href="[URL_REPOSITORIO_CODIGO]" target="_blank" rel="noopener" style="color: #1565c0; font-weight: bold;">
      Link al código
    </a>
  </p>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Consejo:</strong> Si tenés dudas, podés escribir en el foro de la unidad.
  </div>
</div>
```

---

## Autoevaluación

### Banner principal de la sección

→ `Autoevaluacion/00-descripcion-seccion.html` — Descripción de la sub-sección Autoevaluación, **no es un Label**.

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>Autoevaluación – [NOMBRE UNIDAD]</strong>
  </h2>
</div>
```

### Descripción del cuestionario de autoevaluación (fija, no cambia entre unidades salvo la imagen)

→ `Autoevaluacion/01-autoevaluacion.html` — Label independiente.

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 20px; border-radius: 8px;
margin-bottom: 20px; width: 100%; font-family: sans-serif; color: #1a237e;">
  <h3 style="text-align: left; font-size: 1.4rem; color: #1565c0;">
    <img class="img-fluid" role="presentation" src="URL_IMAGEN" alt="Cuánto aprendimos" width="591" height="79">
  </h3>
  <p style="font-size: 1.1rem; text-align: left;">
    <strong>¡Es hora de autoevaluarte!</strong> A continuación, encontrarás una autoevaluación que
    te permitirá medir tus conocimientos adquiridos hasta el momento.
  </p>
  <p style="font-size: 1rem; text-align: left;">
    Si no obtienes el resultado esperado, ¡no te preocupes! Tendrás otra oportunidad para mejorar.
  </p>
  <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; border-left: 4px solid #1565c0; margin-top: 15px;">
    <strong>Consejo:</strong> No olvides repasar los conceptos antes de comenzar. ¡Mucho éxito en tu autoevaluación!
  </div>
</div>
```

La imagen usada (`URL_IMAGEN`) es la misma que la del componente que se está
actualizando — se reutiliza el mismo link, no se genera una nueva.

---

## Encuesta de cierre

### Banner principal de la sección

→ `EncuestaCierre/00-descripcion-seccion.html` — Descripción de la sub-sección Encuesta de cierre, **no es un Label**.

```html
<div style="text-align: center; padding: 20px 10px; border-bottom: 2px solid #FFFFFF;
margin-bottom: 20px; background-color: #001855;">
  <h2 style="color: #ffffff; font-size: 2rem; font-family: 'Segoe UI', sans-serif; margin: 0;">
    <strong>Encuesta de cierre – [NOMBRE UNIDAD]</strong>
  </h2>
</div>
```

### Descripción de la encuesta (fija, no modificar salvo el nombre de la unidad en el banner)

→ `EncuestaCierre/01-encuesta-cierre.html` — va en la Descripción de la Encuesta (`mod_feedback`) existente.

```html
<div style="background-color: #f5f7fa; border: 1px solid #cfd8dc; padding: 15px; border-radius: 8px;
margin-bottom: 20px; font-size: 1rem; color: #1a237e; font-family: sans-serif; line-height: 1.6;">
  <p style="text-align: left;">
    <strong>¡Hola, estudiante!</strong><br><br>
    Gracias por tu participación en esta unidad. Nos gustaría conocer tu opinión para seguir
    mejorando el curso y brindarte una mejor experiencia de aprendizaje.<br><br>
    A continuación, te haremos un par de preguntas para evaluar:
  </p>
  <ul style="list-style: none; padding-left: 0; margin-top: 10px;">
    <li>El desempeño del tutor</li>
    <li>El contenido de la unidad</li>
  </ul>
  <div style="background-color: #e3f2fd; border-left: 4px solid #1565c0; padding: 10px; border-radius: 5px; margin-top: 15px;">
    Recuerda que esta encuesta es <strong>anónima</strong>, por lo que tus respuestas no estarán
    asociadas a tu identidad.
  </div>
  <br>
  <p style="text-align: left;">Por favor, responde con sinceridad. Tu opinión es muy importante para nosotros.</p>
</div>
```

---

## Nombres de sub-pestañas y títulos de referencia (del PDF oficial)

Sub-pestañas: Introducción · Actividades · Actividad lúdica · Práctica · Autoevaluación · Encuesta de cierre.

Otros títulos usados dentro de las secciones: Avisos · Foro social · Encuesta · Espacio para
consultas y dudas · Consultas actividad · Cuestionario de Actividad · Trabajo Práctico · Foro de
consultas TP · Actividad de cierre unidad · Autoevaluación unidad · Consultas autoevaluación ·
Tu opinión nos interesa.
