# Curso: Python para Finanzas Cuantitativas

> **43 unidades · 11 fases · Desde cero hasta portafolio profesional**
> Inspirado en MIT 6.390, MIT 18.06, y MIT ML Tree

---

## 🎯 Meta del Curso

Formarte como programador Python de alto nivel preparado para roles junior en:
- **Investment Banking** (JP Morgan IBD): DCF, LBO, financial modeling
- **Private Equity** (JP Morgan PE): LBO modeling, valoración, due diligence
- **Quantitative Finance** (Citadel, Jane Street): factor models, ML, trading algorítmico

Al terminar las 43 unidades podrás:
1. Valorizar empresas como un analista de JP Morgan
2. Construir modelos LBO como un asociado de Private Equity
3. Implementar modelos de factores y pricing como un quant de Citadel
4. Hacer backtesting de estrategias de trading algorítmico
5. Usar ML para predicción financiera
6. Presentar un portafolio de proyectos en entrevistas

---

## 🗺️ Mapa del Curso

```
🌳 Python para Finanzas Cuantitativas (43 unidades, 11 fases)
│
├── 🔧 FASE 0 — Entorno y Herramientas (U00–U01)
│   ├── U00 — Preparando tu entorno de trabajo profesional
│   └── U01 — Jupyter Notebooks y el flujo de trabajo cuantitativo
│
├── 🧱 FASE 1 — Fundamentos con Contexto Financiero (U02–U06)
│   ├── U02 — Variables, tipos de datos y el lenguaje de los mercados
│   ├── U03 — Operadores: la aritmética de Wall Street
│   ├── U04 — Entrada, salida y manejo de errores básico
│   ├── U05 — Condicionales: reglas de negocio y señales de trading
│   └── U06 — Bucles: iterando sobre series de tiempo
│
├── 📊 FASE 2 — Estructuras de Datos para Finanzas (U07–U10)
│   ├── U07 — Listas y tuplas: series de precios y registros financieros
│   ├── U08 — Diccionarios: portafolios y datos estructurados
│   ├── U09 — Conjuntos y strings avanzados para datos financieros
│   └── U10 — Archivos y datos: CSV, JSON y datos de mercado
│
├── ⚙️ FASE 3 — Funciones y Programación Profesional (U11–U14)
│   ├── U11 — Funciones: construyendo tu librería financiera
│   ├── U12 — Funciones avanzadas: lambda, decoradores y closures
│   ├── U13 — Módulos, paquetes y arquitectura de proyecto
│   └── U14 — Manejo de errores y logging profesional
│
├── 🏛️ FASE 4 — OOP para Finanzas (U15–U18)
│   ├── U15 — Clases y objetos: modelando instrumentos financieros
│   ├── U16 — Herencia y polimorfismo: jerarquía de instrumentos
│   ├── U17 — Métodos especiales y data classes
│   └── U18 — Patrones de diseño en finanzas cuantitativas
│
├── 🔬 FASE 5 — Stack Científico (U19–U23)
│   ├── U19 — NumPy: computación numérica de alto rendimiento
│   ├── U20 — Pandas fundamentos: el DataFrame como hoja de cálculo
│   ├── U21 — Pandas avanzado: análisis de series financieras
│   ├── U22 — Visualización financiera con Matplotlib y Plotly
│   └── U23 — Obtención de datos: APIs y web scraping financiero
│
├── 💰 FASE 6 — Matemáticas Financieras y Valoración (U24–U28)
│   ├── U24 — Valor del dinero en el tiempo y renta fija
│   ├── U25 — Análisis de estados financieros con Python
│   ├── U26 — Valoración de empresas: DCF y comparables
│   ├── U27 — Modelo LBO y Private Equity
│   └── U28 — Derivados: opciones y modelos de pricing
│
├── 📈 FASE 7 — Gestión de Portafolios y Riesgo (U29–U32)
│   ├── U29 — Teoría moderna de portafolios (Markowitz)
│   ├── U30 — Modelos de factores y asset pricing
│   ├── U31 — Gestión de riesgo: VaR, CVaR y stress testing
│   └── U32 — Optimización avanzada de portafolios (HRP, Risk Parity)
│
├── 📐 FASE 8 — Métodos Cuantitativos y Econometría (U33–U36)
│   ├── U33 — Probabilidad, estadística y distribuciones financieras
│   ├── U34 — Series de tiempo: ARIMA y volatilidad (GARCH)
│   ├── U35 — Econometría financiera: regresión y panel data
│   └── U36 — SQL para datos financieros
│
├── 🤖 FASE 9 — ML y Trading Algorítmico (U37–U40)
│   ├── U37 — Machine Learning para finanzas: fundamentos
│   ├── U38 — Machine Learning avanzado: métodos cuantitativos
│   ├── U39 — Algorithmic trading: estrategias y backtesting
│   └── U40 — Infraestructura y producción
│
└── 🚀 FASE 10 — Proyectos Profesionales (U41–U43)
    ├── U41 — Plataforma de análisis cuantitativo completa
    ├── U42 — Sistema de trading cuantitativo end-to-end
    └── U43 — Recursos, comunidad y ruta profesional
```

---

## 📋 Cómo usar este curso

1. **Secuencialmente**: cada unidad asume que dominas la anterior.
2. **Verifica tu aprendizaje**: cada unidad tiene su ✅ Autoevaluación (5 preguntas).
3. **Consulta el glosario**: [`GLOSARIO.md`](./GLOSARIO.md) para 200+ términos.
4. **Marca tu progreso**: [`PROGRESO.md`](./PROGRESO.md) con 43 checkboxes.
5. **Explora visualmente**: abre [`arbol-aprendizaje.html`](./arbol-aprendizaje.html) en tu navegador.

---

## 📁 Estructura del proyecto

```
documentacion/
├── README.md                      ← Este archivo
├── GLOSARIO.md                    ← 200+ términos
├── PROGRESO.md                    ← Checklist 43 unidades
├── arbol-aprendizaje.html         ← Árbol interactivo offline
├── datos/
│   └── precios_ejemplo.csv        ← 252 filas de mercado (OHLCV)
├── teoria/
│   ├── fase-0/    U00–U01
│   ├── fase-1/    U02–U06
│   ├── fase-2/    U07–U10
│   ├── fase-3/    U11–U14
│   ├── fase-4/    U15–U18
│   ├── fase-5/    U19–U23
│   ├── fase-6/    U24–U28
│   ├── fase-7/    U29–U32
│   ├── fase-8/    U33–U36
│   ├── fase-9/    U37–U40
│   └── fase-10/   U41–U42
├── ejercicios/
│   └── fase-N/    (ejercicios + soluciones por unidad)
└── proyectos/
    ├── plataforma/     Proyecto U41
    └── trading-system/ Proyecto U42
```

---

## 📚 Librerías utilizadas

| Fase | Librerías |
|------|----------|
| FASE 0-4 | Python estándar (no requiere pip install) |
| FASE 5 | `numpy`, `pandas`, `matplotlib`, `plotly`, `mplfinance`, `seaborn`, `yfinance`, `requests` |
| FASE 6 | `numpy-financial`, `scipy` |
| FASE 7 | `PyPortfolioOpt`, `statsmodels`, `linearmodels` |
| FASE 8 | `arch`, `pmdarima`, `sqlalchemy` |
| FASE 9 | `scikit-learn`, `xgboost`, `lightgbm`, `torch` |
| FASE 10 | `streamlit` o `dash` |

---

## 📖 Bibliografía

| Recurso | Tipo |
|---------|------|
| Python.org — Documentación oficial | Referencia |
| *Python for Finance* — Yves Hilpisch | Libro |
| *Introduction to Linear Algebra* — Gilbert Strang | Libro (MIT 18.06) |
| *Advances in Financial Machine Learning* — Marcos López de Prado | Libro |
| *Valuation* — McKinsey & Company | Referencia (DCF/LBO) |
| Yahoo Finance (`yfinance`), FRED | Datos reales |

---

## 🧠 Knowledge Wiki

Este proyecto usa el sistema de memoria descrito en `CLAUDE.md`.
Después de cada unidad, guarda lo aprendido en:
```
~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/
```

---

> *"The main focus of machine learning is making decisions or predictions based on data."*
> — MIT 6.390, Lecture 1
>
> *"Si puedes modelar un DCF, puedes entrevistar en cualquier banco de inversión."*
> — JP Morgan IBD VP
