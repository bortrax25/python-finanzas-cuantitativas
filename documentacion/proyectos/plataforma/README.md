# Plataforma de Análisis Cuantitativo Completa

> **Unidad:** U41 — Fase 10  
> **Tipo:** Proyecto Integrador Capstone  
> **Stack:** Streamlit + pandas + scipy + plotly + fpdf2

---

## Descripción

Plataforma web interactiva para análisis financiero end-to-end. Integra:
1. Selección y descarga de activos
2. Análisis fundamental (ratios, DCF, DuPont)
3. Análisis técnico (indicadores, patrones, señales)
4. Optimización de portafolio (Markowitz, HRP, Risk Parity)
5. Gestión de riesgo (VaR, stress testing)
6. Generación de reporte PDF profesional

---

## Instalación

```bash
cd documentacion/proyectos/plataforma
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
streamlit run main.py
```

---

## Estructura del Proyecto

```
plataforma/
├── README.md
├── requirements.txt
├── main.py              # Punto de entrada de la app Streamlit
├── config.py            # Configuración global
├── data/
│   └── descargador.py   # Descarga de datos con yfinance + cache
├── fundamental/
│   ├── ratios.py        # 30+ ratios financieros
│   ├── dcf.py           # Modelo DCF (FCFF, WACC, valor terminal)
│   └── dupont.py        # Análisis DuPont 3 y 5 factores
├── tecnico/
│   ├── indicadores.py   # SMA, EMA, RSI, MACD, Bollinger, VWAP
│   ├── senales.py       # Señales de compra/venta
│   └── patrones.py      # Patrones de velas (doji, hammer, engulfing)
├── portafolio/
│   ├── optimizador.py   # Markowitz, HRP, Risk Parity
│   └── frontera.py      # Frontera eficiente + simulación Monte Carlo
├── riesgo/
│   ├── var.py           # VaR histórico, paramétrico, Monte Carlo
│   ├── stress.py        # Stress testing (escenarios 2008, COVID, dot-com)
│   └── metricas.py      # Sharpe, Sortino, drawdown, Calmar
├── reportes/
│   └── generador_pdf.py # Generación de PDF con fpdf2
├── ui/
│   └── componentes.py   # Componentes Streamlit reutilizables
└── tests/
    ├── test_ratios.py
    ├── test_dcf.py
    ├── test_var.py
    └── test_optimizador.py
```

---

## Funcionalidades por Módulo

### data/descargador.py
- `descargar_datos(tickers, inicio, fin)` → DataFrame OHLCV
- Cache con `@st.cache_data` (Streamlit)
- Soporte para cualquier ticker de Yahoo Finance
- Datos de ejemplo si falla la conexión

### fundamental/ratios.py
- `calcular_ratios(df_financiero)` → DataFrame de 30+ ratios
- Profitability, Liquidity, Leverage, Efficiency, Valuation
- Comparación con promedios del sector

### fundamental/dcf.py
- `modelo_dcf(ticker, datos_financieros)` → valor intrínseco por acción
- Proyección FCFF 5 años, WACC, valor terminal
- Tabla de sensibilidad WACC × Crecimiento

### portafolio/optimizador.py
- `optimizar_portafolio(retornos, metodo)` → pesos óptimos
- Métodos: equal_weight, min_varianza, max_sharpe, risk_parity, hrp
- Frontera eficiente con 10,000 simulaciones

### riesgo/var.py
- `calcular_var(retornos, metodo, confianza)` → VaR
- Métodos: historico, parametrico, monte_carlo
- CVaR / Expected Shortfall

### reportes/generador_pdf.py
- `generar_reporte(ticker, analisis)` → archivo PDF
- 6 secciones con gráficos y tablas
- Formato profesional listo para imprimir

---

## Dependencias Principales

Ver `requirements.txt` para lista completa. Principales:
- streamlit, pandas, numpy, scipy
- yfinance, plotly, matplotlib, seaborn
- fpdf2, PyPortfolioOpt

---

## Notas de Desarrollo

- **Variables en español snake_case:** `precio_cierre`, `tasa_interes`, `flujo_caja`
- **Docstrings NumPy-style:** descripción, parámetros, retorna, ejemplos
- **Type hints:** en todas las funciones públicas
- **Tests:** mínimo 2 tests por módulo con pytest

---

## Referencia

Ver `documentacion/teoria/fase-10/U41-plataforma.md` para la especificación completa.
