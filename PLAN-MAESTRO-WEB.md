# PLAN MAESTRO: Sitio Web del Curso — Estilo MIT 6.390

> **Propósito de este documento:** Todas las instrucciones necesarias para que agentes de IA independientes (sin contexto previo) construyan un sitio web local profesional con las notas del curso "Python para Finanzas Cuantitativas". El resultado debe verse y funcionar como https://introml.mit.edu/notes/ pero construido con MkDocs Material.

---

## 1. CONTEXTO

### 1.1 ¿Qué estamos construyendo?

Un sitio web estático local que presenta las 43 unidades del curso "Python para Finanzas Cuantitativas" de forma navegable, con búsqueda, modo oscuro, fórmulas LaTeX renderizadas, bloques de código con botón copiar, y estética académica tipo MIT.

### 1.2 Referencia visual

- **Sitio objetivo:** https://introml.mit.edu/notes/ (MIT 6.390 Intro to Machine Learning)
- **Características clave del sitio MIT que debemos replicar:**
  - Sidebar izquierdo con capítulos colapsables
  - TOC (tabla de contenidos) en el lado derecho por sección
  - Toggle claro/oscuro
  - Fórmulas LaTeX renderizadas inline y en display
  - Bloques de código con syntax highlighting y botón copiar
  - Breadcrumbs arriba
  - Navegación prev/next al fondo de cada página
  - Búsqueda integrada
  - Tipografía limpia y académica

### 1.3 ¿Dónde vive el proyecto?

```
/Users/miguelangelquispetito/Desktop/ZED/
```

El sitio web se construye DENTRO de este directorio, como un subdirectorio del proyecto existente.

### 1.4 ¿Qué contenido ya existe?

Los archivos `.md` de teoría del curso están en `documentacion/teoria/`. **El contenido puede estar en proceso de creación** — algunos archivos pueden existir y otros no. El sitio web debe funcionar con los archivos que existan en el momento de la construcción.

**Inventario de archivos .md existentes al momento de escribir este plan:**

```
documentacion/README.md
documentacion/PROGRESO.md
documentacion/GLOSARIO.md
documentacion/teoria/fase-0/U00-setup.md
documentacion/teoria/fase-1/U01-variables-tipos.md
documentacion/teoria/fase-1/U02-operadores-python.md
documentacion/teoria/fase-1/U03-entrada-salida.md
documentacion/teoria/fase-1/U04-estructuras-control.md
documentacion/teoria/fase-2/U05-condicionales-if.md
documentacion/teoria/fase-2/U06-condicionales-anidados.md
documentacion/teoria/fase-3/U07-for-range.md
documentacion/teoria/fase-3/U08-while-control.md
documentacion/teoria/fase-3/U09-for-anidados.md
documentacion/teoria/fase-4/U10-listas-tuplas.md
documentacion/teoria/fase-4/U11-diccionarios-sets.md
documentacion/teoria/fase-4/U12-archivos-csv.md
documentacion/teoria/fase-5/U13-funciones-basicas.md
documentacion/teoria/fase-5/U14-avanzado-funciones.md
documentacion/teoria/fase-5/U15-modulos-jupyter.md
documentacion/teoria/fase-6/U16-numpy-pandas.md
documentacion/teoria/fase-6/U17-calculos-financieros.md
documentacion/teoria/fase-6/U18-valoracion-bonos.md
documentacion/teoria/fase-6/U19-modelos-riesgo.md
documentacion/teoria/fase-6/U20-proyecto-final.md
```

**NOTA IMPORTANTE:** El curso está siendo rediseñado de 20 a 43 unidades (ver `PLAN-MAESTRO-CURSO.md`). Los archivos `.md` pueden tener numeración vieja o nueva dependiendo del momento de ejecución. El agente que construya el sitio debe:
1. Escanear `documentacion/teoria/` para encontrar TODOS los `.md` que existan
2. Leer el H1 (`# título`) de cada uno para determinar el título real
3. Organizarlos en la navegación según la fase (carpeta padre)

### 1.5 Stack tecnológico (DECIDIDO, NO CAMBIAR)

| Componente | Tecnología | Razón |
|------------|-----------|-------|
| Generador | **MkDocs** >= 1.6 | Toma `.md` puros, una sola dependencia pip |
| Tema | **Material for MkDocs** >= 9.5 | Look-and-feel superior, features enterprise |
| Fórmulas | **MathJax 3** (vía `pymdownx.arithmatex`) | Soporte completo LaTeX ($...$ y $$...$$) |
| Código | **Pygments** (built-in en Material) | Syntax highlighting + botón copiar |
| Imágenes | **mkdocs-glightbox** | Lightbox/zoom al hacer clic |
| Búsqueda | **Built-in** de Material | Del lado del cliente, sin servidor |
| Lenguaje | **Python >= 3.10** | Ya instalado en el sistema |
| **PROHIBIDO** | Node.js, Docker, Quarto, Hugo, Jekyll | Solo Python |

---

## 2. ESTRUCTURA FINAL DEL REPOSITORIO

Después de ejecutar este plan, el proyecto debe tener esta estructura EXACTA:

```
ZED/
├── CLAUDE.md                           ← NO TOCAR
├── PLAN-MAESTRO-CURSO.md               ← NO TOCAR
├── PLAN-MAESTRO-WEB.md                 ← ESTE ARCHIVO
├── ejercicios_for_anidados.py          ← NO TOCAR
│
├── site-curso/                         ← NUEVO: todo el sitio web vive aquí
│   ├── mkdocs.yml                      ← Configuración principal
│   ├── requirements.txt                ← Dependencias Python
│   ├── README.md                       ← Instrucciones para correr el sitio
│   ├── .gitignore                      ← Ignorar site/, .venv/, __pycache__
│   ├── docs/                           ← Contenido del sitio
│   │   ├── index.md                    ← Página de inicio del curso
│   │   ├── progreso.md                 ← Tracker de progreso (copia de PROGRESO.md)
│   │   ├── glosario.md                 ← Glosario (copia de GLOSARIO.md)
│   │   ├── bibliografia.md             ← Recursos y referencias
│   │   ├── assets/
│   │   │   ├── extra.css               ← CSS personalizado (estética MIT)
│   │   │   └── extra.js                ← MathJax config + SPA re-render
│   │   ├── images/                     ← Imágenes del curso (si hay)
│   │   ├── fase-0/                     ← Notas Fase 0
│   │   │   ├── index.md                ← Portada de fase
│   │   │   ├── U00-setup.md
│   │   │   └── U01-jupyter.md
│   │   ├── fase-1/                     ← Notas Fase 1
│   │   │   ├── index.md
│   │   │   ├── U02-variables-tipos.md
│   │   │   ├── U03-operadores.md
│   │   │   ├── U04-io-errores.md
│   │   │   ├── U05-condicionales.md
│   │   │   └── U06-bucles.md
│   │   ├── fase-2/                     ← ... y así hasta fase-10
│   │   │   ├── index.md
│   │   │   └── [UXX-nombre.md ...]
│   │   ├── fase-3/ ... fase-10/
│   │   └── ejercicios/                 ← (opcional) ejercicios embebidos
│   ├── overrides/                      ← Template overrides (opcional)
│   └── site/                           ← OUTPUT generado (gitignored)
│
└── documentacion/                      ← FUENTE ORIGINAL — NO MODIFICAR
    ├── README.md
    ├── PROGRESO.md
    ├── GLOSARIO.md
    ├── teoria/fase-N/UXX-nombre.md     ← Archivos fuente originales
    └── ejercicios/fase-N/UXX_*.py
```

### 2.1 ¿Por qué `site-curso/` separado?

1. No contaminar la carpeta `documentacion/` que es la fuente de verdad del contenido
2. El sitio web es un **consumidor** del contenido, no el contenido mismo
3. Los archivos `.md` se COPIAN (o symlinkan) desde `documentacion/teoria/` a `site-curso/docs/`
4. Si el contenido del curso cambia, se re-copia y se reconstruye

---

## 3. INSTRUCCIONES DE EJECUCIÓN PASO A PASO

### PASO 1: Crear estructura de carpetas

```bash
cd /Users/miguelangelquispetito/Desktop/ZED

# Crear directorio raíz del sitio
mkdir -p site-curso/docs/assets
mkdir -p site-curso/docs/images
mkdir -p site-curso/overrides

# Crear carpetas por fase dentro de docs/
for i in $(seq 0 10); do
    mkdir -p "site-curso/docs/fase-$i"
done

# Crear carpeta opcional de ejercicios embebidos
mkdir -p site-curso/docs/ejercicios
```

### PASO 2: Crear `site-curso/requirements.txt`

Contenido EXACTO:

```
mkdocs>=1.6
mkdocs-material>=9.5
pymdown-extensions>=10.7
mkdocs-glightbox>=0.4
mkdocs-git-revision-date-localized-plugin>=1.2
mkdocs-minify-plugin>=0.8
```

### PASO 3: Crear `site-curso/mkdocs.yml`

Este es el archivo de configuración central. **Debe crearse con este contenido exacto**, y luego el `nav:` se completa dinámicamente según los archivos que existan:

```yaml
site_name: "Python para Finanzas Cuantitativas — Notas del Curso"
site_description: "Curso completo de Python aplicado a finanzas cuantitativas. 43 unidades desde fundamentos hasta DCF, LBO, opciones, ML y trading algorítmico."
site_author: "Bortrax25"
site_url: "http://localhost:8000"

theme:
  name: material
  language: es
  custom_dir: overrides
  palette:
    - media: "(prefers-color-scheme: light)"
      scheme: default
      primary: indigo
      accent: amber
      toggle:
        icon: material/brightness-7
        name: Cambiar a modo oscuro
    - media: "(prefers-color-scheme: dark)"
      scheme: slate
      primary: indigo
      accent: amber
      toggle:
        icon: material/brightness-4
        name: Cambiar a modo claro
  font:
    text: Inter
    code: JetBrains Mono
  features:
    - navigation.instant
    - navigation.instant.prefetch
    - navigation.tracking
    - navigation.tabs
    - navigation.tabs.sticky
    - navigation.sections
    - navigation.expand
    - navigation.path
    - navigation.indexes
    - navigation.top
    - navigation.footer
    - toc.follow
    - search.suggest
    - search.highlight
    - search.share
    - content.code.copy
    - content.code.annotate
    - content.tabs.link
    - content.tooltips
  icon:
    repo: fontawesome/brands/github

extra_css:
  - assets/extra.css

extra_javascript:
  - assets/extra.js
  - https://unpkg.com/mathjax@3/es5/tex-mml-chtml.js

markdown_extensions:
  - abbr
  - admonition
  - attr_list
  - def_list
  - footnotes
  - md_in_html
  - tables
  - toc:
      permalink: true
      permalink_title: "Enlace permanente"
      toc_depth: 4
  - pymdownx.arithmatex:
      generic: true
  - pymdownx.betterem
  - pymdownx.caret
  - pymdownx.details
  - pymdownx.highlight:
      anchor_linenums: true
      line_spans: __span
      pygments_lang_class: true
  - pymdownx.inlinehilite
  - pymdownx.keys
  - pymdownx.mark
  - pymdownx.smartsymbols
  - pymdownx.snippets
  - pymdownx.superfences:
      custom_fences:
        - name: mermaid
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
  - glightbox
  - minify:
      minify_html: true

extra:
  generator: false

# ==============================================================
# NAVEGACIÓN
# ==============================================================
# INSTRUCCIÓN PARA EL AGENTE: Completar esta sección escaneando
# los archivos .md que existan en docs/ al momento de construir.
# Solo incluir archivos que realmente existan.
# Usar el título H1 de cada archivo como label.
# ==============================================================
nav:
  - Inicio: index.md
  - Progreso: progreso.md
  - Glosario: glosario.md

  - "Fase 0 — Entorno":
    - fase-0/index.md
    # Agregar aquí cada UXX-nombre.md que exista en docs/fase-0/

  - "Fase 1 — Fundamentos":
    - fase-1/index.md
    # Agregar aquí cada UXX-nombre.md que exista en docs/fase-1/

  - "Fase 2 — Estructuras de Datos":
    - fase-2/index.md

  - "Fase 3 — Funciones":
    - fase-3/index.md

  - "Fase 4 — OOP":
    - fase-4/index.md

  - "Fase 5 — NumPy, Pandas, Viz":
    - fase-5/index.md

  - "Fase 6 — Valoración":
    - fase-6/index.md

  - "Fase 7 — Portafolios y Riesgo":
    - fase-7/index.md

  - "Fase 8 — Econometría":
    - fase-8/index.md

  - "Fase 9 — ML y Trading":
    - fase-9/index.md

  - "Fase 10 — Proyectos":
    - fase-10/index.md

  - Bibliografía: bibliografia.md
```

### PASO 4: Crear `site-curso/docs/assets/extra.css`

CSS personalizado para estética académica tipo MIT:

```css
/* ===================================================
   TIPOGRAFÍA ACADÉMICA — estilo MIT 6.390
   =================================================== */

/* Cuerpo: serif académico para lectura prolongada */
.md-typeset {
  font-family: "Iowan Old Style", "Palatino Linotype", Palatino,
               "Book Antiqua", Georgia, serif;
  line-height: 1.75;
  font-size: 0.85rem;
}

/* H1: borde inferior como separador visual */
.md-typeset h1 {
  font-weight: 700;
  letter-spacing: -0.02em;
  border-bottom: 2px solid var(--md-primary-fg-color);
  padding-bottom: 0.4rem;
}

/* H2: espacio superior generoso para separar secciones */
.md-typeset h2 {
  font-weight: 600;
  margin-top: 2.5rem;
  padding-bottom: 0.2rem;
  border-bottom: 1px solid var(--md-default-fg-color--lightest);
}

/* H3: sin borde, solo peso */
.md-typeset h3 {
  font-weight: 600;
  margin-top: 1.8rem;
}

/* ===================================================
   CÓDIGO
   =================================================== */

.md-typeset pre > code {
  font-size: 0.78rem;
  line-height: 1.55;
}

.md-typeset code {
  font-size: 0.82em;
}

/* ===================================================
   ADMONICIONES (tips, warnings, notas)
   =================================================== */

.md-typeset .admonition,
.md-typeset details {
  border-radius: 0.4rem;
  border-left-width: 4px;
}

/* ===================================================
   TABLAS
   =================================================== */

.md-typeset table:not([class]) {
  font-size: 0.78rem;
}

.md-typeset table:not([class]) th {
  background: var(--md-default-fg-color--lightest);
  font-weight: 600;
}

/* ===================================================
   FÓRMULAS MATEMÁTICAS
   =================================================== */

.md-typeset .arithmatex {
  overflow-x: auto;
  padding: 0.4rem 0;
}

/* Fórmulas display centradas con margen */
.md-typeset .MathJax_Display {
  margin: 1.2rem 0 !important;
}

/* ===================================================
   LAYOUT
   =================================================== */

/* Anchura más generosa para contenido con fórmulas y tablas */
.md-grid {
  max-width: 1280px;
}

/* ===================================================
   IMÁGENES
   =================================================== */

.md-typeset img {
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  display: block;
  margin: 1.2rem auto;
}

[data-md-color-scheme="slate"] .md-typeset img {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.4);
}

/* ===================================================
   BLOCKQUOTES (citas, tips financieros)
   =================================================== */

.md-typeset blockquote {
  border-left: 4px solid var(--md-accent-fg-color);
  background: var(--md-code-bg-color);
  padding: 0.6rem 1rem;
  border-radius: 0 6px 6px 0;
  font-style: italic;
}

/* ===================================================
   FOOTER — ocultar "Made with Material"
   =================================================== */

.md-footer-meta {
  display: none;
}

/* ===================================================
   SIDEBAR — unidades como items compactos
   =================================================== */

.md-nav__item .md-nav__link {
  font-size: 0.78rem;
}
```

### PASO 5: Crear `site-curso/docs/assets/extra.js`

```javascript
// ==========================================================
// MathJax 3 — Configuración para LaTeX inline y display
// ==========================================================
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

// ==========================================================
// Re-renderizar fórmulas después de navegación SPA
// (Material for MkDocs usa navigation.instant = SPA)
// ==========================================================
document$.subscribe(() => {
  if (typeof MathJax !== "undefined" && MathJax.typesetPromise) {
    MathJax.typesetPromise();
  }
});
```

### PASO 6: Crear `site-curso/docs/index.md`

Página de inicio del sitio. Contenido EXACTO a crear:

```markdown
---
hide:
  - navigation
  - toc
---

# Python para Finanzas Cuantitativas

**Notas del Curso — 43 Unidades**

---

Bienvenido al curso de **Python aplicado a finanzas cuantitativas**. Este material cubre desde los fundamentos de programación hasta modelos de valoración, gestión de portafolios, econometría financiera, machine learning y trading algorítmico.

El objetivo es que al terminar, tengas el conocimiento técnico para desempeñarte en roles de:

- **Investment Banking** — Valoración DCF, LBO, análisis de estados financieros
- **Private Equity** — Modelos LBO, due diligence, retornos del sponsor
- **Finanzas Cuantitativas** — Factor models, gestión de riesgo, trading algorítmico

---

## Mapa del Curso

| Fase | Nombre | Unidades | Enfoque |
|------|--------|----------|---------|
| 0 | Entorno y Herramientas | U00–U01 | Setup, Jupyter, Git |
| 1 | Fundamentos de Python | U02–U06 | Variables, operadores, condicionales, bucles |
| 2 | Estructuras de Datos | U07–U10 | Listas, diccionarios, sets, archivos |
| 3 | Funciones y Módulos | U11–U14 | Funciones, decoradores, paquetes, testing |
| 4 | Programación Orientada a Objetos | U15–U18 | Clases, herencia, patrones de diseño |
| 5 | Stack Científico | U19–U23 | NumPy, Pandas, visualización, APIs |
| 6 | Valoración Financiera | U24–U28 | TVM, DCF, LBO, opciones (Black-Scholes) |
| 7 | Portafolios y Riesgo | U29–U32 | Markowitz, factores, VaR, HRP |
| 8 | Econometría y SQL | U33–U36 | GARCH, panel data, Fama-MacBeth, SQL |
| 9 | ML y Trading | U37–U40 | Scikit-learn, XGBoost, backtesting, infra |
| 10 | Proyectos Integradores | U41–U42 | Plataforma completa, sistema de trading |

---

## Cómo usar este sitio

- **Sidebar izquierdo**: navega por fases y unidades
- **Barra de búsqueda** (++f++ o ++slash++): busca cualquier concepto
- **Modo oscuro**: toggle arriba a la derecha
- **Fórmulas**: renderizadas con LaTeX ($E = mc^2$)
- **Código**: con syntax highlighting y botón copiar

---

## Correr en local

```bash
cd site-curso
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
mkdocs serve
```

Abre [http://localhost:8000](http://localhost:8000)
```

### PASO 7: Crear `index.md` para cada fase

Cada carpeta `docs/fase-N/` necesita un `index.md` que sirve como portada de la sección. Formato:

```markdown
# Fase N — Nombre de la Fase

> Unidades UXX a UYY

## Contenido de esta fase

| Unidad | Tema | Conceptos clave |
|--------|------|----------------|
| UXX | Título | concepto 1, concepto 2 |
| UYY | Título | concepto 3, concepto 4 |

## Prerequisitos

Haber completado la Fase N-1.

## Librerías nuevas en esta fase

- `libreria1` — para qué se usa
- `libreria2` — para qué se usa
```

**Contenido específico de cada `index.md`:**

#### `docs/fase-0/index.md`
```markdown
# Fase 0 — Entorno y Herramientas

> Unidades U00 a U01

Configura tu entorno de desarrollo profesional e instala Jupyter para el flujo de trabajo cuantitativo.

| Unidad | Tema |
|--------|------|
| U00 | Entorno profesional: Python, VS Code, Git, venv |
| U01 | Jupyter Notebooks y Google Colab |
```

#### `docs/fase-1/index.md`
```markdown
# Fase 1 — Fundamentos de Python con Contexto Financiero

> Unidades U02 a U06

Aprende Python desde cero usando ejemplos del mundo financiero: precios, tasas, rendimientos, señales de trading.

| Unidad | Tema |
|--------|------|
| U02 | Variables, tipos de datos y el lenguaje de los mercados |
| U03 | Operadores: la aritmética de Wall Street |
| U04 | Entrada, salida y manejo de errores |
| U05 | Condicionales: reglas de negocio y señales de trading |
| U06 | Bucles: iterando sobre series de tiempo |
```

#### `docs/fase-2/index.md`
```markdown
# Fase 2 — Estructuras de Datos para Finanzas

> Unidades U07 a U10

| Unidad | Tema |
|--------|------|
| U07 | Listas y tuplas: series de precios y registros OHLCV |
| U08 | Diccionarios: portafolios y datos estructurados |
| U09 | Conjuntos y strings avanzados para datos financieros |
| U10 | Archivos: CSV, JSON y datos de mercado |
```

#### `docs/fase-3/index.md`
```markdown
# Fase 3 — Funciones, Módulos y Programación Profesional

> Unidades U11 a U14

| Unidad | Tema |
|--------|------|
| U11 | Funciones: construyendo tu librería financiera |
| U12 | Lambda, decoradores y closures |
| U13 | Módulos, paquetes y arquitectura de proyecto |
| U14 | Manejo de errores y logging profesional |
```

#### `docs/fase-4/index.md`
```markdown
# Fase 4 — Programación Orientada a Objetos para Finanzas

> Unidades U15 a U18

| Unidad | Tema |
|--------|------|
| U15 | Clases y objetos: modelando instrumentos financieros |
| U16 | Herencia y polimorfismo: jerarquía de instrumentos |
| U17 | Métodos especiales y data classes |
| U18 | Patrones de diseño en finanzas cuantitativas |
```

#### `docs/fase-5/index.md`
```markdown
# Fase 5 — Stack Científico: NumPy, Pandas y Visualización

> Unidades U19 a U23

| Unidad | Tema |
|--------|------|
| U19 | NumPy: computación numérica de alto rendimiento |
| U20 | Pandas fundamentos: Series y DataFrames |
| U21 | Pandas avanzado: análisis de series financieras |
| U22 | Visualización financiera (Matplotlib, Plotly) |
| U23 | Obtención de datos: APIs y web scraping financiero |
```

#### `docs/fase-6/index.md`
```markdown
# Fase 6 — Matemáticas Financieras y Valoración

> Unidades U24 a U28

| Unidad | Tema |
|--------|------|
| U24 | Valor del dinero en el tiempo y renta fija |
| U25 | Análisis de estados financieros con Python |
| U26 | Valoración de empresas: DCF y comparables |
| U27 | Modelo LBO y Private Equity |
| U28 | Derivados: opciones y modelos de pricing |
```

#### `docs/fase-7/index.md`
```markdown
# Fase 7 — Gestión de Portafolios y Riesgo

> Unidades U29 a U32

| Unidad | Tema |
|--------|------|
| U29 | Teoría moderna de portafolios (Markowitz) |
| U30 | Modelos de factores y asset pricing |
| U31 | Gestión de riesgo: VaR, CVaR y stress testing |
| U32 | Optimización avanzada de portafolios |
```

#### `docs/fase-8/index.md`
```markdown
# Fase 8 — Métodos Cuantitativos y Econometría

> Unidades U33 a U36

| Unidad | Tema |
|--------|------|
| U33 | Probabilidad, estadística y distribuciones financieras |
| U34 | Series de tiempo: ARIMA y volatilidad (GARCH) |
| U35 | Econometría financiera: regresión y panel data |
| U36 | SQL para datos financieros |
```

#### `docs/fase-9/index.md`
```markdown
# Fase 9 — Machine Learning y Trading Algorítmico

> Unidades U37 a U40

| Unidad | Tema |
|--------|------|
| U37 | Machine learning para finanzas: fundamentos |
| U38 | ML avanzado: XGBoost, PCA, autoencoders |
| U39 | Algorithmic trading: estrategias y backtesting |
| U40 | Infraestructura y producción |
```

#### `docs/fase-10/index.md`
```markdown
# Fase 10 — Proyectos Integradores

> Unidades U41 a U42

| Unidad | Tema |
|--------|------|
| U41 | Plataforma de análisis cuantitativo completa |
| U42 | Sistema de trading cuantitativo end-to-end |
```

### PASO 8: Copiar archivos .md de teoría a docs/

**Script exacto para copiar los archivos fuente:**

```bash
cd /Users/miguelangelquispetito/Desktop/ZED

# Copiar cada archivo .md de teoria/ a la carpeta correspondiente en site-curso/docs/
for fase_dir in documentacion/teoria/fase-*/; do
    fase_name=$(basename "$fase_dir")
    for md_file in "$fase_dir"*.md; do
        if [ -f "$md_file" ]; then
            cp "$md_file" "site-curso/docs/$fase_name/$(basename "$md_file")"
        fi
    done
done

# Copiar documentos globales
cp documentacion/PROGRESO.md site-curso/docs/progreso.md
cp documentacion/GLOSARIO.md site-curso/docs/glosario.md

echo "Archivos copiados."
```

**DESPUÉS de copiar**, el agente debe:
1. Listar todos los `.md` copiados con `find site-curso/docs -name "*.md" | sort`
2. Leer el H1 de cada uno: `head -1 <archivo>`
3. Actualizar el `nav:` en `mkdocs.yml` con los archivos que realmente existan

### PASO 9: Actualizar nav: en mkdocs.yml dinámicamente

El agente debe generar la sección `nav:` basándose ÚNICAMENTE en los archivos que existan. Formato:

```yaml
nav:
  - Inicio: index.md
  - Progreso: progreso.md
  - Glosario: glosario.md

  - "Fase 0 — Entorno":
    - fase-0/index.md
    - "U00: Preparando tu Entorno": fase-0/U00-setup.md

  - "Fase 1 — Fundamentos":
    - fase-1/index.md
    - "U01: Variables y Tipos": fase-1/U01-variables-tipos.md
    - "U02: Operadores": fase-1/U02-operadores-python.md
    # ... solo archivos que existan

  # ... etc para cada fase que tenga archivos
```

**Reglas del nav:**
- El label de cada entry es el título H1 del archivo (sin el `#`)
- Si una fase no tiene ningún archivo `.md` (aparte del `index.md`), incluirla igual con solo el index
- Mantener el orden numérico de las unidades (U00, U01, U02...)
- No inventar archivos que no existan

### PASO 10: Crear `site-curso/docs/bibliografia.md`

```markdown
# Bibliografía y Recursos

## Libros

| Libro | Autor | Uso en el curso |
|-------|-------|----------------|
| *Python for Finance* | Yves Hilpisch | Referencia general |
| *Introduction to Linear Algebra* | Gilbert Strang | Fundamentos matemáticos |
| *Options, Futures, and Other Derivatives* | John Hull | Derivados (U28) |
| *Investment Valuation* | Aswath Damodaran | Valoración (U25-U27) |

## Repositorios de Referencia

| Repo | Tema |
|------|------|
| [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit) | 150+ ratios financieros |
| [PyPortfolioOpt](https://github.com/PyPortfolio/PyPortfolioOpt) | Optimización de portafolios |
| [QuantResearch](https://github.com/letianzj/QuantResearch) | Estrategias cuantitativas |
| [linearmodels](https://github.com/bashtage/linearmodels) | Econometría (panel data) |
| [fin-model-course](https://github.com/nickderobertis/fin-model-course) | Modelamiento financiero |
| [MIT 18.06](https://github.com/mitmath/1806) | Álgebra lineal |

## APIs de Datos

| Fuente | Uso |
|--------|-----|
| Yahoo Finance (`yfinance`) | Precios históricos |
| FRED (`fredapi`) | Datos macroeconómicos |
| Alpha Vantage | Datos en tiempo real |
| Twelve Data | Multi-asset data |
```

### PASO 11: Crear `site-curso/README.md`

```markdown
# Python para Finanzas Cuantitativas — Sitio Web

Sitio web estático con las notas del curso, generado con MkDocs Material.

## Requisitos

- Python >= 3.10

## Instalación

\```bash
python -m venv .venv
source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt
\```

## Servir en local (con hot-reload)

\```bash
mkdocs serve
\```

Abre http://localhost:8000

## Construir sitio estático

\```bash
mkdocs build
\```

El sitio se genera en `site/`. Puedes abrir `site/index.html` directamente.

## Actualizar contenido

Si los archivos .md en `documentacion/teoria/` cambian:

\```bash
# Desde la raíz del proyecto ZED/
bash copiar-contenido.sh    # (o copiar manualmente)
cd site-curso
mkdocs build
\```
```

### PASO 12: Crear `site-curso/.gitignore`

```
.venv/
__pycache__/
site/
*.pyc
.DS_Store
```

### PASO 13: Instalar dependencias y verificar

```bash
cd /Users/miguelangelquispetito/Desktop/ZED/site-curso

# Crear venv e instalar
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Build estricto — debe completar sin errores
mkdocs build --strict

# Si hay warnings, resolverlos antes de continuar
```

### PASO 14: Servir y verificar visualmente

```bash
mkdocs serve
# Abrir http://localhost:8000
```

**Checklist de verificación:**

- [ ] El sitio carga sin errores en http://localhost:8000
- [ ] El sidebar izquierdo muestra todas las fases con sus unidades
- [ ] Las tabs superiores funcionan (Inicio, Fase 0, Fase 1, etc.)
- [ ] El toggle claro/oscuro funciona
- [ ] La búsqueda (tecla `f` o `/`) encuentra contenido
- [ ] Los bloques de código Python tienen syntax highlighting
- [ ] Los bloques de código tienen botón "copiar"
- [ ] Las fórmulas LaTeX renderizan (si hay `$...$` o `$$...$$` en el contenido)
- [ ] Los links prev/next aparecen al fondo de cada página
- [ ] Las imágenes (si hay) se muestran con lightbox al hacer clic
- [ ] El breadcrumb muestra la ruta correcta
- [ ] Las tablas se ven bien formateadas
- [ ] Los admonitions (💡, ⚠️, etc.) se ven como cajas coloreadas
- [ ] El `index.md` de cada fase muestra la tabla de unidades
- [ ] El glosario y progreso son navegables

### PASO 15: Reportar resultado

El agente debe reportar:

```
RESULTADO:
- Archivos .md integrados: XX
- Fases con contenido: XX de 11
- Unidades con contenido: XX de 43
- Build status: ✅ sin errores / ❌ con N warnings
- Fórmulas LaTeX: ✅ renderizando / ❌ no encontradas
- Búsqueda: ✅ funcional
- Links rotos: [lista si hay]
```

---

## 4. REGLAS ESTRICTAS PARA EL AGENTE EJECUTOR

1. **NO modificar archivos en `documentacion/`** — es la fuente de verdad. Solo copiar.
2. **NO modificar `CLAUDE.md`, `PLAN-MAESTRO-CURSO.md`, `ejercicios_for_anidados.py`**
3. **NO cambiar el stack** — si algo falla, diagnosticar y arreglar dentro de MkDocs Material.
4. **NO inventar contenido** — si un archivo `.md` no existe, no crear contenido ficticio para llenarlo. Solo crear los `index.md` de cada fase.
5. **NO reescribir los textos del usuario** — el trabajo es presentación, no redacción.
6. **Si un archivo `.md` tiene emojis (💡, ⚠️, ✅)** — dejarlos tal cual, MkDocs Material los renderiza bien.
7. **Si una decisión es ambigua** — elegir la opción más conservadora.
8. **Ejecutar paso a paso** — no intentar hacer todo de golpe. Completar cada paso, verificar, luego seguir.

---

## 5. CÓMO MANTENER EL SITIO ACTUALIZADO

Cuando se creen nuevas unidades del curso (nuevos archivos `.md` en `documentacion/teoria/`):

1. Copiar el nuevo archivo a `site-curso/docs/fase-N/`
2. Agregar la entrada correspondiente en `nav:` de `mkdocs.yml`
3. Ejecutar `mkdocs build --strict` para verificar
4. Ejecutar `mkdocs serve` para ver el resultado

**Script de actualización automática** (crear como `site-curso/actualizar.sh`):

```bash
#!/bin/bash
# Actualizar contenido del sitio desde la fuente
cd "$(dirname "$0")/.."

# Copiar teoría
for fase_dir in documentacion/teoria/fase-*/; do
    fase_name=$(basename "$fase_dir")
    mkdir -p "site-curso/docs/$fase_name"
    for md_file in "$fase_dir"*.md; do
        [ -f "$md_file" ] && cp "$md_file" "site-curso/docs/$fase_name/"
    done
done

# Copiar docs globales
cp documentacion/PROGRESO.md site-curso/docs/progreso.md
cp documentacion/GLOSARIO.md site-curso/docs/glosario.md

echo "Contenido actualizado. Ejecuta 'mkdocs serve' desde site-curso/"
echo "IMPORTANTE: Actualiza el nav: en mkdocs.yml si se agregaron nuevos archivos."
```

---

## 6. DIFERENCIAS CON EL SITIO MIT 6.390

| Aspecto | MIT 6.390 | Nuestro sitio |
|---------|-----------|--------------|
| Motor | Quarto | MkDocs Material |
| Formato fuente | `.qmd` | `.md` |
| Fórmulas | KaTeX | MathJax 3 |
| Hosting | introml.mit.edu | localhost:8000 |
| Idioma | Inglés | Español |
| Contenido | ML (12 capítulos) | Finanzas cuantitativas (43 unidades) |
| Navegación | Sidebar colapsable | Sidebar + tabs + breadcrumbs |
| Código | Copy button | Copy button + annotations |
| Búsqueda | Sí | Sí (client-side) |
| Dark mode | Sí | Sí |

Lo que nuestro sitio tiene **extra** vs MIT:
- Tabs superiores por fase (navegación más rápida)
- Breadcrumbs
- Checklist de progreso integrado
- Glosario navegable
- Diagrams (Mermaid) si se necesitan
- Lightbox para imágenes

---

## 7. TROUBLESHOOTING

### Error: "Plugin 'git-revision-date-localized' not found"
→ El proyecto no es un repo git. Solución: eliminar el plugin de `mkdocs.yml` o ejecutar `git init` en `site-curso/`.

### Error: fórmulas LaTeX no renderizan
→ Verificar que `extra.js` carga MathJax. Verificar que `pymdownx.arithmatex` está en `markdown_extensions` con `generic: true`.

### Error: "Navigation file not found"
→ El `nav:` referencia un archivo que no existe. Verificar con `find site-curso/docs -name "*.md"` y ajustar `nav:`.

### Error: CSS/JS no carga
→ Verificar que `extra_css` y `extra_javascript` en `mkdocs.yml` apuntan a `assets/extra.css` y `assets/extra.js` (rutas relativas a `docs/`).

### Warning: "Prefix" en busqueda
→ Normal, no afecta funcionalidad. Ignorar.
