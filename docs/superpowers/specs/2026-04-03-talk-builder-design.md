# Talk Builder — Design Spec

## Overview

Plugin multi-skill para Claude Code que guía la creación de presentaciones académicas/médicas de forma sistemática y reproducible. Funciona en CLI, Desktop y Cowork.

El usuario invoca `/talk` y un orquestador lo guía fase a fase, desde el briefing inicial hasta la generación de PPTX y documentos de soporte.

## Principios de diseño

- **Un solo punto de entrada:** `/talk` orquesta todo. Los sub-skills son accesibles individualmente pero no es necesario recordarlos.
- **La carpeta de trabajo es el estado:** el orquestador detecta qué archivos existen para saber en qué fase está el proyecto.
- **Config en dos niveles:** global (estilo personal) con override local por charla.
- **Assets personales en ruta elegida por el usuario:** independientes del plugin, sobreviven a actualizaciones.
- **Iterativo, no lineal:** cada fase tiene checkpoint. Se puede volver atrás.
- **Referencias sagradas:** nada inventado, todo verificable con DOI/PMID.
- **Storytelling como diferenciador:** no slides informativas — emociones, mensaje, narrativa.
- **Idioma del plugin:** todos los SKILL.md, references y documentación interna del plugin en inglés (idioma nativo de Claude, mayor precisión). El output generado para el usuario se adapta al idioma que configure en su `config.yaml` o `talk.yaml`.

---

## Arquitectura

### Plugin (repositorio GitHub)

```
talk-builder/
├── plugin.json
├── .gitignore
├── config.example.yaml
├── skills/
│   ├── talk/SKILL.md                # Orquestador principal
│   ├── talk-setup/SKILL.md          # Setup interactivo inicial
│   ├── talk-briefing/SKILL.md       # Fase 1: Wizard interactivo
│   ├── talk-vision/SKILL.md         # Fase 2: Enfoque personal
│   ├── talk-research/SKILL.md       # Fase 3: Investigación (iterativa)
│   ├── talk-assets/SKILL.md         # Fase 4: Assets visuales
│   ├── talk-narrative/SKILL.md      # Fase 5: Estructura narrativa + storytelling
│   ├── talk-slides/SKILL.md         # Fase 6: Generación PPTX
│   ├── talk-study-doc/SKILL.md      # Fase 7: Documentos de estudio
│   └── talk-script/SKILL.md         # Fase 8: Script del presentador
├── references/
│   ├── storytelling-guide.md        # ABT, Sparkline, STAR, SCR, conectores, aperturas, cierres
│   ├── slide-design-guide.md        # Assertion-Evidence, Presentation Zen, glance test
│   ├── data-storytelling.md         # Knaflic, Rosling, Tufte, datos con narrativa
│   └── pacing-guide.md             # Templates de timing: 10, 15, 20, 30 min
└── assets/
    └── README.md                    # Instrucciones sobre qué va aquí
```

### Assets personales (ruta elegida por el usuario)

`/talk-setup` pregunta al usuario dónde quiere guardar sus assets personales. La ruta elegida se almacena en el config. Ejemplo si elige `~/Documents/talk-builder/`:

```
~/Documents/talk-builder/           # (o la ruta que el usuario elija)
├── config.yaml                      # Estilo personal (fonts, colores, preferencias)
├── example-slides/                  # Presentaciones de referencia para aprender estilo
│   └── (archivos .pptx/.key)
└── fixed-slides/                    # Slides reutilizables (contacto, disclosures, etc.)
    └── (archivos .pptx/.key)
```

El `config.yaml` contiene:

```yaml
assets_path: "~/Documents/talk-builder"   # Ruta elegida por el usuario en /talk-setup

style:
  fonts:
    title: "Montserrat Bold"
    body: "Open Sans"
  colors:
    primary: "#1A365D"
    accent: "#E53E3E"
    background: "#FFFFFF"
  language: "en"
  narrative_style: "conversational"
  complexity_default: "moderate"

style_analysis:
  layout: ""          # Generado por talk-setup al analizar tus slides
  title_style: ""
  color_usage: ""
  typography: ""
  visual_density: ""
  notes: ""
```

### Carpeta de trabajo (una por charla)

```
mi-charla-sobre-X/
├── talk.yaml                        # Config local (override del global)
├── vision.md                        # Enfoque, ideas, emociones
├── pdfs/                            # Papers aportados por el usuario
├── images/                          # Figuras extraídas + propuestas generativas
│   ├── autor-año-figN-descripción.png        # Figura extraída
│   ├── autor-año-figN-descripción-page.pdf   # Página completa del paper
│   ├── [GENERATE]-descripción.txt            # Prompt para Midjourney/Gemini
│   └── image-map.md                          # Mapa: qué imagen va en qué slide
├── research.md                      # Investigación consolidada
├── narrative.md                     # Estructura de slides aprobada
├── presentation.pptx                # Presentación final
├── article-summaries.docx           # Resumen 200-300 palabras por paper
├── study-document.docx              # Documento exhaustivo de estudio
└── speaker-script.docx              # Script del presentador
```

### .gitignore del plugin

```
config.yaml
assets/example-slides/*
assets/fixed-slides/*
!assets/README.md
```

### Cadena de prioridad de config

`talk.yaml` (local por charla) > `config.yaml` (global personal)

El local puede sobreescribir cualquier campo del global: fonts, colores, idioma, lo que sea.

---

## Dependencias

- **poppler-utils** (`brew install poppler`): para extracción de imágenes de PDFs (`pdfimages`, `pdftoppm`)
- **MCPs remotos** (ya disponibles en Claude): PubMed, Consensus
- **Claude nativo**: lectura de PDFs, generación de PPTX y DOCX

`/talk-setup` verifica que poppler esté instalado y guía la instalación si no.

---

## Skills — Detalle por fase

### `/talk` — Orquestador principal

**Trigger:** el usuario invoca `/talk`
**Comportamiento:**

1. Verifica que `config.yaml` existe en la ruta de assets. Si no, redirige a `/talk-setup`.
2. Escanea la carpeta de trabajo actual buscando archivos de estado:
   - `talk.yaml` → briefing hecho
   - `vision.md` → visión definida
   - `research.md` → research hecho
   - `images/` con contenido → assets listos
   - `narrative.md` → narrativa aprobada
   - `presentation.pptx` → slides generadas
   - `study-document.docx` + `article-summaries.docx` → docs de estudio generados
   - `speaker-script.docx` → script generado
3. Muestra estado del proyecto con checklist visual (fase completada / pendiente).
4. Propone la siguiente fase.
5. Ofrece la opción de saltar a otra fase o volver a una anterior.
6. Invoca el sub-skill correspondiente.

### `/talk-setup` — Setup interactivo inicial

**Trigger:** primera ejecución o invocación directa
**Input:** nada
**Output:** `<ruta-elegida>/config.yaml` + estructura de carpetas

1. Pregunta al usuario dónde quiere guardar sus assets personales (ej. `~/Documents/talk-builder/`, `~/talks-config/`, lo que prefiera).
2. Crea la carpeta elegida con subcarpetas `example-slides/` y `fixed-slides/`.
3. Pregunta interactivamente:
   - Idioma por defecto
   - Font de títulos
   - Font de cuerpo
   - Color primario (hex)
   - Color de acento (hex)
   - Nivel de complejidad por defecto
3. Pregunta si tiene presentaciones de referencia → indica dónde ponerlas.
4. Pregunta si tiene slides fijas (contacto, disclosures, etc.) → indica dónde ponerlas.
5. Si hay slides de ejemplo, las analiza y genera `style_analysis` en el config.
6. Verifica que `poppler-utils` está instalado. Si no, guía la instalación.
7. Genera `config.yaml`.

### `/talk-briefing` — Fase 1: Wizard interactivo

**Input:** nada (o carpeta vacía)
**Output:** `talk.yaml`

Preguntas guiadas una a una:

1. Tema de la charla
2. Duración disponible (10, 15, 20, 30 min)
3. Tipo de audiencia (especialistas, médicos generales, congreso internacional, formación interna, mixta)
4. Idioma de la presentación
5. Nivel de complejidad científica (básico, moderado, avanzado)
6. ¿Tienes papers propios o bibliografía específica? → ponlos en `pdfs/`
7. ¿Quieres búsqueda de literatura con PubMed/Consensus?
8. ¿Es una charla nueva o mejorar una existente? → si existente, ponerla en la carpeta
9. ¿Incluir slide de disclosures? ¿Contacto al final? (slides fijas)

Genera `talk.yaml` con todas las respuestas estructuradas.

### `/talk-vision` — Fase 2: Enfoque personal

**Input:** `talk.yaml`
**Output:** `vision.md`

Conversación abierta e interactiva:

1. ¿Qué mensaje principal quieres que la audiencia se lleve?
2. ¿Qué ángulo o enfoque? (clínico, investigación, provocador, inspiracional...)
3. ¿Hay una historia personal, caso clínico o anécdota como hilo conductor?
4. ¿Qué emociones quieres generar? (curiosidad, urgencia, esperanza, sorpresa...)
5. ¿Ideas específicas de slides o momentos que ya visualizas?
6. ¿Qué NO quieres que la charla sea?

Consolida en `vision.md`.

### `/talk-research` — Fase 3: Investigación (iterativa)

**Input:** `talk.yaml` + `vision.md` + `pdfs/` (opcional, pueden llegar en cualquier momento)
**Output:** `research.md`

Fase iterativa en loop:

1. Lanza queries a PubMed y Consensus basándose en tema + visión.
2. Muestra resultados interactivamente — el usuario elige cuáles incluir.
3. Lee PDFs que el usuario haya puesto en `pdfs/`.
4. Consolida en `research.md`: hallazgos clave, datos, citas con referencia completa (DOI/PMID).
5. Revisión conjunta: el skill identifica huecos ("Tienes datos de prevalencia pero no de tratamiento").
6. El usuario puede:
   - Pedir más búsquedas específicas
   - Agregar nuevos PDFs a `pdfs/` en cualquier momento
   - Redirigir el enfoque
7. Itera hasta que el usuario esté satisfecho.
8. Verifica que no haya claims sin referencia.

### `/talk-assets` — Fase 4: Assets visuales

**Input:** `research.md` + `pdfs/`
**Output:** carpeta `images/` poblada + `image-map.md`

1. Extrae imágenes de PDFs con enfoque híbrido:
   - Primero `pdfimages` para imágenes embebidas a calidad original.
   - Si faltan figuras (vectoriales/compuestas), convierte página a alta resolución (300dpi) con `pdftoppm`.
   - El usuario indica qué zona cropear manteniendo siempre aspect ratio.
2. Para cada figura extraída genera dos archivos:
   - `autor-año-figN-descripción.png` — figura para usar en slides
   - `autor-año-figN-descripción-page.pdf` — página completa del paper como referencia
3. Muestra las figuras al usuario, que elige cuáles conservar.
4. Propone imágenes de alto impacto para generar externamente:
   - Genera prompts listos para Midjourney/Gemini.
   - Los guarda como `[GENERATE]-descripción.txt`.
5. Genera `image-map.md`: mapa de qué imagen va en qué slide (sugerencia).

### `/talk-narrative` — Fase 5: Estructura narrativa + storytelling

**Input:** `talk.yaml` + `vision.md` + `research.md` + `images/`
**Output:** `narrative.md`

Usa `references/storytelling-guide.md`, `references/slide-design-guide.md` y `references/pacing-guide.md`.

1. Selecciona template de timing según duración (de `pacing-guide.md`).
2. Aplica ABT como estructura macro.
3. Usa Sparkline para ritmo emocional (what is / what could be).
4. Planifica un STAR moment (~2/3 de la charla).
5. Diseña apertura según visión (cold open, caso clínico, estadística, pregunta provocadora).
6. Diseña cierre (callback a la apertura, visión de futuro, call to action).
7. Escribe conectores narrativos (Bridge) entre cada slide.
8. Cada slide en `narrative.md` tiene:
   - Número y título (formato assertion-evidence)
   - Contenido propuesto
   - Imagen sugerida (referencia a `images/`)
   - Conector (Bridge) al siguiente slide
   - Timing estimado
9. Aplica Rule of Three: máximo 3 mensajes clave.
10. Presenta la estructura al usuario para revisión. Itera hasta aprobación.

### `/talk-slides` — Fase 6: Generación PPTX

**Input:** `narrative.md` + `images/` + `config.yaml` + `talk.yaml`
**Output:** `presentation.pptx`

1. Lee config de estilo (global + override local).
2. Lee `style_analysis` del config y slides de ejemplo si necesita validar.
3. Genera PPTX slide por slide según `narrative.md`.
4. Aplica principios de `slide-design-guide.md`.
5. Inserta imágenes de `images/`.
6. Inserta slides fijas si se indicaron en briefing (disclosures, contacto).
7. Presenta resultado para revisión.

Nota: el usuario afinará el resultado final en Keynote (reposicionar imágenes, ajustes visuales finos).

### `/talk-study-doc` — Fase 7: Documentos de estudio

**Input:** `research.md` + `narrative.md`
**Output:** `study-document.docx` + `article-summaries.docx`

**study-document.docx:**
- Contenido exhaustivo del tema en profundidad.
- Organizado por secciones de la charla.
- Incluye datos que no entraron en la presentación (útiles para Q&A).
- Referencias completas.

**article-summaries.docx:**
- Resumen de 200-300 palabras por cada paper utilizado.
- Hallazgo principal, metodología, relevancia para la charla.
- Referencia completa con DOI/PMID.

### `/talk-script` — Fase 8: Script del presentador

**Input:** `narrative.md` + `presentation.pptx`
**Output:** `speaker-script.docx`

Usa `references/teleprompter-format.md` (en `talk-script/references/`).

**Sección 1 — Tabla de preparación:**
- Tabla slide por slide: número, título, qué decir (prosa natural conversacional), conector (Bridge) a la siguiente, timing.
- Prosa natural, frases cortas, sin guiones largos, vocabulario accesible (idioma según config).

**Sección 2 — Teleprompter:**
- Texto formateado para leer en pantalla.
- Líneas cortas (5-7 palabras).
- Marcadores de [PAUSA].
- Palabras clave en MAYÚSCULAS para énfasis.
- Transiciones marcadas.

---

## Frameworks de storytelling incorporados

Documentados en `references/storytelling-guide.md`:

| Framework | Autor | Uso en el plugin |
|---|---|---|
| ABT (And, But, Therefore) | Randy Olson | Estructura macro de toda la narrativa |
| Sparkline (what is / what could be) | Nancy Duarte | Ritmo emocional a lo largo de la charla |
| STAR Moment | Nancy Duarte | Un momento memorable planificado (~2/3) |
| Assertion-Evidence | Michael Alley | Diseño de cada slide (título = conclusión) |
| SCR (Situation, Complication, Resolution) | Barbara Minto | Alternativa al ABT para framear problemas |
| Rule of Three | Clásica | Máximo 3 mensajes clave |
| Patient Story Bookend | Medicina | Abrir con caso humano, cerrar volviendo |
| Nested Loops | Narrativa clásica | Historia dentro de historia |
| SUCCESs | Chip & Dan Heath | Test de cada slide (simple, unexpected, concrete...) |
| Callback Connectors | Narrativa | Conectores que referencian lo anterior |

**Técnicas de apertura:** cold open, estadística impactante, pregunta provocadora, historia personal, afirmación contraria.

**Técnicas de cierre:** callback, visión de futuro, call to action, cita de paciente.

**Pacing:** templates por duración (10, 15, 20, 30 min), attention resets cada 10 min, bookend heavy (lo importante al inicio y al final).

---

## Distribución e instalación

1. Código fuente en repositorio GitHub.
2. Instalación: `/plugin install talk-builder@<marketplace>`.
3. Primera ejecución: `/talk-setup` configura assets personales.
4. Uso diario: `/talk` en una carpeta vacía o con trabajo en progreso.
