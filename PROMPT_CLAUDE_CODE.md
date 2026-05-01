# Prompt para Claude Code: Construir un sitio de notas tipo MIT 6.390 a partir de archivos Markdown

## Contexto y rol

Actúas como **ingeniero de software senior** especializado en sitios estáticos de documentación técnica, con experiencia construyendo material educativo al nivel del MIT OpenCourseWare. Vas a transformar una carpeta de archivos `.md` (notas de un curso de **Python aplicado a finanzas**) en un sitio web local de calidad profesional, navegable y agradable de leer, inspirado en https://introml.mit.edu/notes/ del curso 6.390 del MIT.

**Mi prioridad es: máxima calidad visual y de UX con la mínima cantidad de tecnologías y configuración.** No quiero un stack pesado. Quiero algo que arranque con un solo comando y que cualquier persona pueda clonar y ejecutar.

---

## Stack obligatorio (ya decidido, no cambiar)

- **MkDocs + Material for MkDocs** (Python). Es la opción óptima:
  - Toma archivos `.md` puros, sin necesidad de convertirlos a otro formato.
  - Una única dependencia instalable con `pip`.
  - Look-and-feel igual o superior al sitio del MIT 6.390.
  - Soporte nativo para LaTeX/KaTeX (crítico porque hay fórmulas financieras: VAN, TIR, Black-Scholes, regresiones, etc.).
  - Resaltado de sintaxis para Python.
  - Búsqueda integrada del lado del cliente.
  - Modo claro/oscuro automático.
  - Hot-reload en local con `mkdocs serve`.
- **Python ≥ 3.10** (asumir que ya está instalado).
- **Sin Node.js, sin Docker, sin Quarto, sin Hugo, sin Jekyll.** Solo Python.

---

## Estructura del repositorio que debes crear

Mi carpeta actual contiene archivos `.md` (algunos con imágenes en subcarpetas, posiblemente). Debes:

1. **NO mover ni renombrar mis archivos `.md` originales.** Trabaja sobre ellos donde están o cópialos a `docs/` preservando estructura.
2. Crear esta estructura final en la raíz del proyecto:

```
.
├── mkdocs.yml                  # Configuración principal
├── requirements.txt            # Dependencias Python
├── README.md                   # Instrucciones para correr el sitio
├── .gitignore                  # Ignorar site/ y __pycache__
├── docs/                       # AQUÍ van todos los .md (copiados o referenciados)
│   ├── index.md                # Página de inicio (crear si no existe)
│   ├── assets/                 # CSS y JS personalizados
│   │   ├── extra.css
│   │   └── extra.js
│   ├── images/                 # Imágenes del curso (si aplica)
│   └── [todos mis .md aquí, organizados por tema]
└── overrides/                  # (opcional) overrides de plantilla
```

---

## Pasos que debes ejecutar (en este orden exacto)

### Paso 1 — Inspección y planificación

1. Lista TODOS los archivos `.md` en la carpeta actual usando `find . -name "*.md" -type f`.
2. Examina las primeras líneas de cada uno para entender:
   - Si tienen título en `# H1`.
   - Si hay un orden lógico (numeración tipo `01_intro.md`, `02_pandas.md`).
   - Si referencian imágenes (`![](...)`) y dónde están.
3. **Antes de escribir nada**, muéstrame:
   - El listado de archivos detectados.
   - Una propuesta de **agrupación por secciones** (ej: "Fundamentos", "Análisis de datos con Pandas", "Visualización", "Finanzas cuantitativas", "Modelos predictivos", "Apéndices").
   - El orden propuesto del `nav` en `mkdocs.yml`.
4. **Espera mi confirmación** antes de continuar al Paso 2.

### Paso 2 — Crear `requirements.txt`

```txt
mkdocs>=1.6
mkdocs-material>=9.5
pymdown-extensions>=10.7
mkdocs-glightbox>=0.4
mkdocs-git-revision-date-localized-plugin>=1.2
mkdocs-minify-plugin>=0.8
```

### Paso 3 — Crear `mkdocs.yml` con configuración profesional

La configuración debe incluir, como mínimo:

```yaml
site_name: Python Aplicado a Finanzas — Notas del Curso
site_description: Notas completas del curso de Python aplicado a finanzas cuantitativas
site_author: Bortrax25
site_url: http://localhost:8000

# Repositorio (déjalo placeholder, lo edito yo después si quiero)
# repo_url: https://github.com/usuario/repo
# repo_name: usuario/repo

theme:
  name: material
  language: es
  palette:
    # Modo claro
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-7
        name: Cambiar a modo oscuro
    # Modo oscuro
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: indigo
      toggle:
        icon: material/brightness-4
        name: Cambiar a modo claro
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant         # SPA-like, sin recargas
    - navigation.instant.prefetch
    - navigation.tracking        # URL refleja sección activa
    - navigation.tabs            # Pestañas superiores por sección top
    - navigation.tabs.sticky
    - navigation.sections        # Secciones expandidas en sidebar
    - navigation.expand
    - navigation.path            # Breadcrumbs
    - navigation.indexes         # index.md hace de portada de sección
    - navigation.top             # Botón "back to top"
    - navigation.footer          # Botones prev/next abajo
    - toc.follow                 # TOC scrollea con el contenido
    - toc.integrate              # (opcional) TOC integrado en sidebar
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy          # Botón copiar en bloques de código
    - content.code.annotate      # Anotaciones en código
    - content.tabs.link          # Pestañas sincronizadas
    - content.tooltips
  icon:
    repo: fontawesome/brands/github

extra_css:
  - assets/extra.css

extra_javascript:
  - assets/extra.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

markdown_extensions:
  # Básicos
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
      permalink_title: Enlace permanente a esta sección
      toc_depth: 4
  # PyMdown (los buenos)
  - pymdownx.arithmatex:        # LaTeX / fórmulas matemáticas
      generic: true
  - pymdownx.betterem
  - pymdownx.caret
  - pymdownx.details             # <details> colapsables
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys                # ++ctrl+c++
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid          # Diagramas
          class: mermaid
          format: !!python/name:pymdownx.superfences.fence_code_format
  - pymdownx.tabbed:
      alternate_style: true
  - pymdownx.tasklist:
      custom_checkbox: true
  - pymdownx.tilde

plugins:
  - search:
      lang:
        - es
        - en
  - glightbox                    # Lightbox para imágenes (clic = zoom)
  - git-revision-date-localized:
      enable_creation_date: true
      type: date
      fallback_to_build_date: true
  - minify:
      minify_html: true

extra:
  generator: false
  social:
    - icon: fontawesome/brands/github
      link: https://github.com/

# nav: SE GENERA EN EL PASO 1, completa aquí con la estructura propuesta
nav:
  - Inicio: index.md
  # ... el resto se completa según los archivos detectados
```

### Paso 4 — Crear `docs/assets/extra.css`

CSS personalizado para acercar la estética al MIT (tipografía serif para cuerpo, mejor legibilidad, anchos cómodos):

```css
/* Tipografía serif al estilo MIT (Palatino-like) para el cuerpo */
.md-typeset {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino, "Book Antiqua", Georgia, serif;
  line-height: 1.7;
  font-size: 0.85rem;
}

/* Headings con peso visual claro */
.md-typeset h1 {
  font-weight: 700;
  letter-spacing: -0.02em;
  border-bottom: 2px solid var(--md-primary-fg-color);
  padding-bottom: 0.4rem;
}

.md-typeset h2 {
  font-weight: 600;
  margin-top: 2.5rem;
}

/* Bloques de código más cómodos */
.md-typeset pre > code {
  font-size: 0.78rem;
  line-height: 1.55;
}

/* Admoniciones más elegantes */
.md-typeset .admonition,
.md-typeset details {
  border-radius: 0.4rem;
  border-left-width: 4px;
}

/* Tablas con mejor presentación */
.md-typeset table:not([class]) {
  font-size: 0.78rem;
}

/* Fórmulas matemáticas: que respiren */
.md-typeset .arithmatex {
  overflow-x: auto;
  padding: 0.4rem 0;
}

/* Anchura de contenido más generosa para fórmulas largas */
.md-grid {
  max-width: 1280px;
}

/* Imágenes centradas y con sombra suave */
.md-typeset img {
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: block;
  margin: 1.2rem auto;
}

/* Modo oscuro: ajustes finos */
[data-md-color-scheme="slate"] .md-typeset img {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
}

/* Citas más visuales */
.md-typeset blockquote {
  border-left: 4px solid var(--md-accent-fg-color);
  background: var(--md-code-bg-color);
  padding: 0.6rem 1rem;
  border-radius: 0 6px 6px 0;
}
```

### Paso 5 — Crear `docs/assets/extra.js`

```javascript
// Configuración de MathJax para LaTeX inline ($...$) y display ($$...$$)
window.MathJax = {
  tex: {
    inlineMath: [["\\(", "\\)"], ["$", "$"]],
    displayMath: [["\\[", "\\]"], ["$$", "$$"]],
    processEscapes: true,
    processEnvironments: true
  },
  options: {
    ignoreHtmlClass: ".*|",
    processHtmlClass: "arithmatex"
  }
};

// Re-renderizar fórmulas tras navegación SPA de Material
document$.subscribe(() => {
  if (typeof MathJax !== "undefined" && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});
```

### Paso 6 — Crear `docs/index.md`

Si no tengo ya un archivo de portada, crea uno con:
- Título grande del curso.
- Breve descripción (2–3 párrafos) del contenido del curso de Python aplicado a finanzas.
- Tabla o lista de secciones principales con enlaces.
- Sección "Cómo navegar las notas" (búsqueda, modo oscuro, etc.).
- Footer con instrucciones de cómo correr en local.

Si ya existe un `index.md` o `README.md` apto, adáptalo respetando el contenido original.

### Paso 7 — Procesamiento de los archivos `.md` existentes

1. Copia todos mis `.md` a `docs/` preservando subcarpetas.
2. Si encuentras imágenes en subcarpetas, cópialas a `docs/images/` o respeta la ruta original siempre que funcione.
3. **NO modifiques el contenido** de mis archivos salvo que sea estrictamente necesario para que rendericen bien:
   - Si hay rutas de imágenes rotas, corrígelas.
   - Si hay encabezados duplicados que romperían el TOC, repórtamelos pero NO los toques sin permiso.
4. **No reescribas mis textos.** No "mejores" mi redacción. Tu trabajo es la presentación, no el contenido.

### Paso 8 — Crear `README.md` del proyecto

Con instrucciones claras para correrlo:

````markdown
# Python Aplicado a Finanzas — Notas

Sitio web estático con las notas del curso, generado con MkDocs Material.

## Requisitos

- Python ≥ 3.10

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate     # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Servir en local (con hot-reload)

```bash
mkdocs serve
```

Abre http://localhost:8000

## Construir sitio estático

```bash
mkdocs build
```

El sitio se genera en `site/`. Puedes abrir `site/index.html` o servirlo
con cualquier servidor estático.
````

### Paso 9 — Crear `.gitignore`

```
.venv/
__pycache__/
site/
*.pyc
.DS_Store
```

### Paso 10 — Verificación final

1. Ejecuta `pip install -r requirements.txt` (en un venv si es posible).
2. Ejecuta `mkdocs build --strict` y resuelve cualquier warning.
3. Ejecuta `mkdocs serve` y verifica que arranca en `http://localhost:8000`.
4. Reporta:
   - Número total de archivos `.md` integrados.
   - Estructura final del `nav`.
   - Cualquier link roto o imagen faltante detectada.
   - Confirmación de que las fórmulas matemáticas renderizan (si encuentras `$...$` en algún archivo).

---

## Reglas estrictas de comportamiento

1. **Modo planificador primero, ejecutor después.** En el Paso 1 solo planifica y muéstrame el plan. No empieces a crear archivos hasta que confirme.
2. **No inventes contenido.** Si una sección no tiene `.md` correspondiente, no la incluyas en el `nav`.
3. **No modifiques mis archivos `.md` originales** salvo lo estrictamente necesario y reportándolo.
4. **Output mínimo, código máximo.** Cuando ejecutes, no me expliques cada línea; solo reporta lo que hiciste y cualquier problema.
5. **Si algo del stack no funciona**, no cambies a otra tecnología. Diagnostica el error y arréglalo dentro de MkDocs Material.
6. **Si una decisión es ambigua** (ej: cómo agrupar archivos con nombres poco claros), pregúntame antes de decidir tú.

---

## Criterio de éxito

Cuando termines, debo poder:

1. Clonar/abrir la carpeta.
2. Ejecutar `pip install -r requirements.txt`.
3. Ejecutar `mkdocs serve`.
4. Ver mis notas en `http://localhost:8000` con:
   - Sidebar navegable con todas las secciones.
   - Búsqueda funcional.
   - Modo claro/oscuro.
   - Fórmulas matemáticas renderizadas.
   - Bloques de código de Python con resaltado y botón copiar.
   - Imágenes con lightbox al hacer clic.
   - Estética limpia, tipografía agradable, anchos de lectura cómodos.

**Empieza ahora con el Paso 1.**
