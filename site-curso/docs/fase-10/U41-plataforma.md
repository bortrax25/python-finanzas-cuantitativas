# U41: Proyecto — Plataforma de Análisis Cuantitativo Completa

> **Lectura previa:** [U40: Infraestructura y Producción](../fase-9/U40-infraestructura.md)
> **Próxima unidad:** [U42: Proyecto — Sistema de Trading Cuantitativo End-to-End](./U42-sistema-trading.md)

---

## 1. Visión General del Proyecto

Construirás una **plataforma web interactiva** para análisis financiero que integre todos los conocimientos del curso. Esta plataforma será tu proyecto insignia para portafolio profesional — el equivalente a un "capstone project" de MIT.

### 1.1 Objetivos de Aprendizaje

Al completar este proyecto, serás capaz de:

1. Diseñar e implementar una aplicación web financiera end-to-end
2. Integrar múltiples módulos de análisis en una interfaz unificada
3. Generar reportes profesionales automatizados
4. Presentar análisis cuantitativos de forma visual e interactiva
5. Estructurar un proyecto Python de nivel profesional

### 1.2 Tecnologías

| Componente | Tecnología | Justificación |
|------------|-----------|---------------|
| **Frontend** | Streamlit | Rápido, Python nativo, ideal para dashboards financieros |
| **Datos** | yfinance, pandas | Descarga y manipulación de datos de mercado |
| **Análisis Fundamental** | pandas, numpy | Cálculo de ratios, DCF, DuPont |
| **Análisis Técnico** | pandas, numpy | Indicadores, patrones, señales |
| **Portafolio** | PyPortfolioOpt, scipy | Optimización, frontera eficiente |
| **Riesgo** | scipy, numpy | VaR, CVaR, stress testing |
| **Reportes** | fpdf2 o reportlab | Generación de PDF profesionales |
| **Visualización** | plotly, matplotlib | Gráficos interactivos |

### 1.3 Arquitectura

```
plataforma/
├── README.md              # Especificación del proyecto (este documento)
├── requirements.txt       # Dependencias
├── main.py                # Punto de entrada (Streamlit app)
├── config.py              # Configuración global
├── data/
│   ├── __init__.py
│   └── descargador.py     # Módulo de descarga de datos (yfinance)
├── fundamental/
│   ├── __init__.py
│   ├── ratios.py          # 30+ ratios financieros
│   ├── dcf.py             # Modelo DCF completo
│   └── dupont.py          # Análisis DuPont (3 y 5 factores)
├── tecnico/
│   ├── __init__.py
│   ├── indicadores.py     # SMA, EMA, RSI, MACD, Bollinger
│   ├── senales.py         # Generación de señales buy/sell
│   └── patrones.py        # Detección de patrones chartistas
├── portafolio/
│   ├── __init__.py
│   ├── optimizador.py     # Markowitz, HRP, Risk Parity
│   └── frontera.py        # Cálculo de frontera eficiente
├── riesgo/
│   ├── __init__.py
│   ├── var.py             # VaR histórico, paramétrico, Monte Carlo
│   ├── stress.py          # Stress testing (escenarios históricos)
│   └── metricas.py        # Sharpe, Sortino, drawdown, Calmar
├── reportes/
│   ├── __init__.py
│   └── generador_pdf.py   # Generación de reporte PDF
├── ui/
│   ├── __init__.py
│   └── componentes.py     # Componentes Streamlit reutilizables
└── tests/
    ├── test_ratios.py
    ├── test_dcf.py
    ├── test_var.py
    └── test_optimizador.py
```

---

## 2. Módulos Requeridos

### 2.1 Módulo de Selección de Activos (data/)

**Requisitos:**
- Descargar datos de Yahoo Finance para cualquier ticker
- Soportar múltiples tickers simultáneamente
- Permitir selección de rango de fechas
- Mostrar tabla de precios descargados
- Cache de datos para evitar descargas repetidas (`@st.cache_data`)

```python
# Ejemplo de interfaz esperada
def descargar_datos(tickers, fecha_inicio, fecha_fin):
    """
    Descarga datos OHLCV de Yahoo Finance.
    
    Retorna:
        DataFrame MultiIndex con columnas (Open, High, Low, Close, Volume)
    """
    pass
```

### 2.2 Módulo de Análisis Fundamental (fundamental/)

**Requisitos:**

**Ratios (ratios.py):**
- Profitability: ROE, ROA, Gross Margin, Net Margin, EBITDA Margin
- Liquidity: Current Ratio, Quick Ratio, Cash Ratio
- Leverage: Debt/Equity, Debt/EBITDA, Interest Coverage
- Efficiency: Asset Turnover, Inventory Turnover, Receivables Turnover
- Valuation: P/E, P/B, EV/EBITDA, P/S, PEG, Dividend Yield

**DCF (dcf.py):**
- Proyectar Free Cash Flow a 5 años
- Calcular WACC (CAPM + costo de deuda)
- Valor terminal (Gordon Growth + Exit Multiple)
- Enterprise Value → Equity Value → Precio por acción
- Tabla de sensibilidad WACC × Growth Rate

**DuPont (dupont.py):**
- ROE = Net Margin × Asset Turnover × Equity Multiplier (3 factores)
- ROE = Tax Burden × Interest Burden × EBIT Margin × Asset Turnover × Leverage (5 factores)

### 2.3 Módulo de Análisis Técnico (tecnico/)

**Requisitos:**
- SMA (10, 20, 50, 200), EMA (12, 26)
- Bollinger Bands (20, 2σ)
- RSI (14), MACD (12, 26, 9)
- Volume, VWAP
- Señales: cruce de medias móviles, RSI sobrecompra/sobreventa, MACD crossover
- Gráfico de velas japonesas con indicadores superpuestos (plotly)

### 2.4 Módulo de Portafolio (portafolio/)

**Requisitos:**
- Frontera eficiente (10,000 portafolios simulados)
- Portafolio de mínima varianza
- Portafolio de máximo Sharpe ratio (tangente)
- Risk Parity
- Hierarchical Risk Parity (HRP)
- Comparación visual de estrategias
- Tabla de pesos óptimos
- Gráfico de torta (pie chart) de asignación

### 2.5 Módulo de Riesgo (riesgo/)

**Requisitos:**
- VaR por 3 métodos: histórico, paramétrico (normal), Monte Carlo (10,000 simulaciones)
- CVaR / Expected Shortfall
- Stress testing con escenarios predefinidos:
  - Crisis 2008: -38% S&P 500
  - COVID 2020: -34% en 1 mes
  - Dot-com 2000: -49% Nasdaq
- Backtesting VaR: Kupiec test (proportion of failures)
- Matriz de correlación con heatmap

### 2.6 Módulo de Reportes (reportes/)

**Requisitos:**
- Generar PDF profesional que incluya:
  1. Portada con logo, fecha, ticker analizado
  2. Resumen ejecutivo (1 página)
  3. Análisis fundamental (ratios, DuPont, DCF)
  4. Análisis técnico (gráficos de indicadores)
  5. Optimización de portafolio (pesos, frontera)
  6. Gestión de riesgo (VaR, stress test)
- Tablas formateadas, gráficos embebidos
- Descargable desde la interfaz

---

## 3. Interfaz de Usuario (Streamlit)

La aplicación debe tener una barra lateral (`st.sidebar`) con las siguientes secciones:

```
📊 PLATAFORMA DE ANÁLISIS CUANTITATIVO
─────────────────────────────────────
📈 Selección de Activos
   ├── Ticker(s): [________]
   ├── Fecha inicio: [________]
   ├── Fecha fin: [________]
   └── [Descargar Datos]

💰 Análisis Fundamental
   ├── Ratios Financieros
   ├── Modelo DCF
   └── Análisis DuPont

📉 Análisis Técnico
   ├── Gráfico de Velas
   ├── Indicadores
   └── Señales de Trading

🎯 Optimización de Portafolio
   ├── Frontera Eficiente
   ├── Max Sharpe
   └── Risk Parity

⚠️ Gestión de Riesgo
   ├── Value at Risk (VaR)
   ├── Stress Testing
   └── Backtesting

📄 Generar Reporte PDF
```

---

## 4. Entregables

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Especificación completa del proyecto |
| `requirements.txt` | Todas las dependencias con versiones |
| `main.py` | Aplicación Streamlit funcional con todas las secciones |
| `config.py` | Configuración centralizada (paths, defaults) |
| `data/descargador.py` | Descarga y cache de datos |
| `fundamental/ratios.py` | 30+ ratios financieros |
| `fundamental/dcf.py` | Modelo DCF completo |
| `fundamental/dupont.py` | Análisis DuPont |
| `tecnico/indicadores.py` | Indicadores técnicos |
| `tecnico/senales.py` | Generación de señales |
| `portafolio/optimizador.py` | Optimización de portafolio |
| `riesgo/var.py` | Cálculo de VaR |
| `riesgo/stress.py` | Stress testing |
| `reportes/generador_pdf.py` | Generación de reporte PDF |
| `ui/componentes.py` | Componentes Streamlit reutilizables |

---

## 5. Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Funcionalidad** | 30% | Todos los módulos funcionan correctamente |
| **Código** | 25% | Limpio, documentado (docstrings), type hints, sin errores |
| **Visualización** | 20% | Gráficos profesionales, interactivos, bien etiquetados |
| **Reporte PDF** | 15% | PDF completo, bien formateado, profesional |
| **Arquitectura** | 10% | Estructura modular, imports limpios, configuración centralizada |

---

## 6. Recursos y Referencias

- **FinanceToolkit:** github.com/JerBouma/FinanceToolkit (inspiración de ratios)
- **PyPortfolioOpt:** github.com/PyPortfolio/PyPortfolioOpt
- **Streamlit docs:** docs.streamlit.io
- **Plotly finance:** plotly.com/python/candlestick-charts/
- **fpdf2:** pypi.org/project/fpdf2/

---

> 📝 **Knowledge Wiki:** Al terminar este proyecto, guarda en memoria:
> - Streamlit es ideal para dashboards financieros: rápido de prototipar, Python nativo
> - La arquitectura modular (data, fundamental, tecnico, portafolio, riesgo, reportes) permite escalar cada módulo independientemente
> - El caché de Streamlit (`@st.cache_data`) es crítico para no re-descargar datos cada vez que el usuario interactúa
> - Un reporte PDF profesional automatizado es un diferenciador clave en entrevistas
