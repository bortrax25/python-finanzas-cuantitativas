# Python para Finanzas Cuantitativas

**Curso completo de Python aplicado a finanzas cuantitativas. 43 unidades desde fundamentos hasta DCF, LBO, opciones, ML y trading algorítmico.**

[![Site](https://img.shields.io/badge/site-localhost:8000-gold)](http://localhost:8000)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://python.org)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## 🎯 ¿Qué es esto?

Un curso educativo que te lleva desde `print("Hola, mercados financieros")` hasta:

- **Investment Banking**: Valoración DCF, LBO, análisis de estados financieros
- **Private Equity**: Modelos LBO, IRR/MOIC, due diligence
- **Finanzas Cuantitativas**: Factor models, gestión de riesgo, trading algorítmico
- **Machine Learning**: Random Forest, XGBoost, autoencoders aplicados a mercados

---

## 🚀 Arrancar en local (2 minutos)

```bash
# 1. Clonar
git clone <este-repo>.git
cd ZED/site-curso

# 2. Entorno virtual
python3 -m venv .venv
source .venv/bin/activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Servir
mkdocs serve
```

Abre **[http://localhost:8000](http://localhost:8000)**

---

## 📂 Estructura

```
ZED/
├── site-curso/           ← Sitio web (MkDocs Material)
│   ├── mkdocs.yml        ← Configuración del sitio
│   ├── docs/             ← Contenido (.md teórico + ejercicios)
│   │   ├── index.md      ← Landing page
│   │   ├── fase-0/...fase-10/  ← 11 fases con teoría
│   │   ├── ejercicios/   ← 99+ ejercicios con soluciones
│   │   └── assets/       ← CSS + JS
│   └── requirements.txt  ← Solo 5 dependencias Python
│
├── documentacion/        ← Fuente de contenido
│   ├── teoria/           ← 43+ archivos .md de teoría
│   ├── ejercicios/       ← 99+ archivos .py de ejercicios
│   ├── README.md         ← Índice maestro del curso
│   ├── PROGRESO.md       ← Checklist de 43 unidades
│   ├── GLOSARIO.md       ← 250+ términos
│   └── BIBLIOGRAFIA.md   ← Recursos y referencias
│
├── PLAN-MAESTRO-CURSO.md  ← Especificación completa del curso
├── PLAN-MAESTRO-WEB.md    ← Especificación del sitio web
└── CLAUDE.md              ← Guía para agentes de IA
```

---

## 🌳 Navegación del Sitio

| Fase | Contenido | Unidades |
|------|----------|----------|
| 🔧 0 | Entorno y Herramientas | U00–U01 |
| 🧱 1 | Fundamentos de Python | U02–U06 |
| 📊 2 | Estructuras de Datos | U07–U10 |
| ⚙️ 3 | Funciones y Módulos | U11–U14 |
| 🏛️ 4 | OOP para Finanzas | U15–U18 |
| 🔬 5 | Stack Científico | U19–U23 |
| 💰 6 | Valoración Financiera | U24–U28 |
| 📈 7 | Portafolios y Riesgo | U29–U32 |
| 📐 8 | Econometría | U33–U36 |
| 🤖 9 | ML y Trading | U37–U40 |
| 🚀 10 | Proyectos Finales | U41–U43 |

---

## 🎨 Diseño

Inspirado en [MIT 6.390](https://introml.mit.edu/notes/) y construido con:

- **MkDocs Material** — generador de sitios estáticos
- **MathJax 3** — fórmulas LaTeX
- **Tipografía**: Playfair Display + Crimson Text + Fira Code
- **Estética "Financial Editorial"**: navy, cream, gold

---

## 📦 Dependencias

Solo 5 paquetes Python (sin Node.js, sin Docker):

```
mkdocs>=1.6
mkdocs-material>=9.5
pymdown-extensions>=10.7
mkdocs-glightbox>=0.4
mkdocs-minify-plugin>=0.8
```

---

## 📝 Licencia

MIT — Ver [LICENSE](LICENSE)
