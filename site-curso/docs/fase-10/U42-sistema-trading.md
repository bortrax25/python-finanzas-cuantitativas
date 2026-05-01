# U42: Proyecto — Sistema de Trading Cuantitativo End-to-End

> **Lectura previa:** [U41: Proyecto — Plataforma de Análisis Cuantitativo](./U41-plataforma.md)
> **Próxima unidad:** *Fin del curso — ¡Felicitaciones!*

---

## 1. Visión General del Proyecto

Construirás un **sistema de trading cuantitativo completo** que integre ingesta de datos, feature engineering, modelos de machine learning, backtesting con costos de transacción, y generación de tear sheets profesionales. Este proyecto demuestra que puedes construir un sistema de inversión sistemática de principio a fin.

### 1.1 Objetivos de Aprendizaje

1. Diseñar un pipeline de datos robusto para trading
2. Implementar feature engineering avanzado para modelos predictivos
3. Entrenar y validar 3 estrategias de ML con TimeSeriesSplit
4. Backtestear con costos de transacción realistas
5. Integrar gestión de riesgo en el proceso de inversión
6. Generar tear sheets de calidad profesional (estilo pyfolio)

### 1.2 Tecnologías

| Componente | Tecnología |
|------------|-----------|
| **Pipeline de datos** | pandas, yfinance, SQLite |
| **Feature engineering** | pandas, numpy, ta (technical analysis) |
| **ML Models** | scikit-learn, XGBoost, LightGBM |
| **Backtesting** | Framework propio (U39) + vectorización |
| **Risk Management** | numpy, scipy |
| **Tear Sheet** | matplotlib, seaborn, fpdf2 |
| **Orquestación** | APScheduler (diario) |

### 1.3 Arquitectura

```
trading-system/
├── README.md              # Especificación del proyecto
├── requirements.txt       # Dependencias
├── config.py              # Configuración global
├── pipeline.py            # Orquestador principal
├── data/
│   ├── __init__.py
│   ├── ingesta.py         # Descarga de datos de mercado
│   ├── limpieza.py        # Validación, imputación, outliers
│   └── almacenamiento.py  # Interfaz con SQLite/PostgreSQL
├── features/
│   ├── __init__.py
│   ├── ingenieria.py      # Feature engineering financiero
│   ├── tecnicas.py        # Indicadores técnicos (RSI, MACD, etc.)
│   └── seleccion.py       # Selección de features (importancia, PCA)
├── modelos/
│   ├── __init__.py
│   ├── base.py            # Clase base para modelos
│   ├── random_forest.py   # Modelo 1: Random Forest
│   ├── xgboost_model.py   # Modelo 2: XGBoost
│   ├── lightgbm_model.py  # Modelo 3: LightGBM
│   └── ensemble.py        # Ensemble de los 3 modelos
├── backtest/
│   ├── __init__.py
│   ├── motor.py            # Motor de backtesting vectorizado
│   ├── costos.py           # Modelo de costos de transacción
│   ├── metricas.py         # Sharpe, Sortino, Calmar, etc.
│   └── walk_forward.py     # Walk-forward cross-validation
├── riesgo/
│   ├── __init__.py
│   ├── posicionamiento.py # Position sizing (Kelly, risk parity, etc.)
│   ├── limites.py          # Stop-loss, take-profit, trailing stops
│   └── var_cvar.py         # VaR y CVaR del portafolio
├── reportes/
│   ├── __init__.py
│   ├── tear_sheet.py       # Tear sheet completo
│   └── graficos.py         # Equity curves, drawdown, heatmaps
└── tests/
    ├── test_features.py
    ├── test_modelos.py
    ├── test_backtest.py
    └── test_riesgo.py
```

---

## 2. Módulos Requeridos

### 2.1 Pipeline de Datos (data/)

**Requisitos:**
- Descargar datos OHLCV para un universo de 20+ tickers del S&P 500
- Ventana: mínimo 10 años de datos diarios
- Validación automática: precios negativos, gaps sospechosos, días sin datos
- Almacenar en SQLite con schema normalizado
- Actualización diaria incremental (solo descargar fechas nuevas)

### 2.2 Feature Engineering (features/)

**Requisitos — mínimo 30 features:**

| Categoría | Features |
|-----------|---------|
| **Retornos** | Retornos 1d, 5d, 10d, 21d, 63d |
| **Volatilidad** | Vol rolling 5d, 10d, 21d, 63d |
| **Momentum** | Mom 5d, 10d, 21d, 63d, 126d, 252d |
| **Medias Móviles** | SMA 10, 20, 50, 200; distancia a SMA |
| **Técnicos** | RSI 14, MACD, Bollinger %B, ATR 14 |
| **Volumen** | Volumen / media 20d, volumen / media 50d |
| **Cross-sectional** | Rank de momentum en el universo, z-score cross-sectional |

**Target (3 horizontes):**
- `target_5d`: dirección del retorno a 5 días (0/1)
- `target_21d`: dirección a 1 mes
- `target_63d`: dirección a 3 meses

### 2.3 Modelos ML (modelos/)

**Requisitos:**

Cada modelo debe implementar la interfaz:

```python
class ModeloBase:
    def entrenar(self, X_train, y_train, X_val, y_val):
        """Entrena con early stopping en validation set."""
        pass
    
    def predecir(self, X):
        """Retorna probabilidades de clase 1 (subida)."""
        pass
    
    def feature_importance(self):
        """Retorna DataFrame con importancia de features."""
        pass
    
    def reentrenar(self, X, y):
        """Reentrena con todo el histórico (para producción)."""
        pass
```

**Los 3 modelos:**
1. **Random Forest:** Baseline sólido, interpretable, feature importance gratis
2. **XGBoost:** Gradient boosting, regularización L1/L2, manejo de missing values
3. **LightGBM:** Más rápido, leaf-wise growth, categóricas nativas

**Validación:**
- Walk-forward: reentrenar cada 6 meses con datos hasta ese momento
- TimeSeriesSplit con 5 folds en cada ventana de entrenamiento
- Early stopping basado en validation loss (no en test)

### 2.4 Backtesting (backtest/)

**Requisitos del motor de backtesting:**

```python
class MotorBacktest:
    def __init__(self, precios, tasa_libre_riesgo=0.03):
        ...
    
    def ejecutar(self, senales, capital_inicial=1_000_000,
                 comision=0.001, slippage=0.0005):
        """
        Ejecuta backtest completo.
        
        Parámetros:
            senales: DataFrame con probabilidades de subida por día/activo
            capital_inicial: capital inicial
            comision: costo de transacción (10 bps)
            slippage: deslizamiento (5 bps)
        
        Retorna:
            Diccionario con equity curve, trades, métricas
        """
        pass
    
    def generar_tear_sheet(self):
        """Genera tear sheet completo."""
        pass
```

**Costos de transacción:**
- Comisión fija: 10 bps por trade
- Slippage: 5 bps (modelo simple: proporcional a volatilidad)
- Market impact: 2 bps adicionales para órdenes > 5% del volumen diario

**Estrategia de ejecución:**
1. Cada día, el modelo predice probabilidad de subida para cada activo
2. Comprar top 5 activos con mayor probabilidad (long-only, equally weighted)
3. Vender al día siguiente si el activo sale del top 5
4. Máximo 5 posiciones simultáneas, capital equitativo

### 2.5 Gestión de Riesgo (riesgo/)

**Requisitos:**

- **Position sizing:** 
  - Equal weight (baseline)
  - Inverse volatility (1/σ)
  - Risk parity (equal risk contribution)
  - Kelly criterion (simplificado)

- **Stop-loss:**
  - Fixed: -5% desde entrada
  - Trailing: -10% desde el máximo desde entrada
  - Time-based: salir después de N días si no hay ganancia

- **Límites:**
  - Máxima exposición por activo: 25%
  - Máxima exposición por sector: 40%
  - Máximo drawdown diario: -3% (si se activa, liquidar todo)

### 2.6 Tear Sheet (reportes/)

**Requisitos del tear sheet (estilo pyfolio):**

Debe incluir:
1. **Equity curve** con benchmark (S&P 500 buy & hold)
2. **Drawdown chart** (underwater plot)
3. **Monthly returns heatmap**
4. **Rolling Sharpe (12 meses)**
5. **Distribución de retornos diarios** con normal overlay
6. **Top 10 mejores/peores días**
7. **Tabla de métricas:**
   - Retorno total, retorno anualizado
   - Volatilidad anualizada
   - Sharpe ratio, Sortino ratio
   - Max drawdown, Calmar ratio
   - Win rate, profit factor
   - Alpha, beta vs benchmark
   - Information ratio

---

## 3. Flujo de Trabajo Diario

```
1. 18:00 — Descargar datos del día (cierre del mercado)
2. 18:05 — Validar y limpiar datos nuevos
3. 18:10 — Almacenar en SQLite
4. 18:15 — Recalcular features para todo el universo
5. 18:20 — Predecir señales con los 3 modelos
6. 18:25 — Ensemble de predicciones (promedio de probabilidades)
7. 18:30 — Seleccionar top 5 activos para comprar mañana
8. 18:35 — Verificar límites de riesgo
9. 18:40 — Generar órdenes para el día siguiente
10. 18:45 — Enviar resumen por email
```

---

## 4. Entregables

| Archivo | Descripción |
|---------|-------------|
| `README.md` | Documento de arquitectura y uso |
| `requirements.txt` | Dependencias |
| `config.py` | Parámetros globales (tickers, horizonte, risk limits) |
| `pipeline.py` | Orquestador del flujo diario |
| `data/` | Módulos de ingesta, limpieza y almacenamiento |
| `features/` | Feature engineering, indicadores, selección |
| `modelos/` | RF, XGBoost, LightGBM, ensemble |
| `backtest/` | Motor, costos, métricas, walk-forward |
| `riesgo/` | Position sizing, stop-loss, VaR |
| `reportes/` | Tear sheet, gráficos |
| `tests/` | Tests unitarios para cada módulo |

---

## 5. Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| **Pipeline** | 20% | Datos limpios, actualización automática, sin errores |
| **Features** | 20% | 30+ features, correctamente calculadas, sin look-ahead bias |
| **Modelos** | 20% | 3 modelos con walk-forward validation, early stopping |
| **Backtest** | 20% | Motor correcto, costos realistas, métricas completas |
| **Riesgo** | 10% | Position sizing, stop-loss, límites implementados |
| **Tear Sheet** | 10% | Visualizaciones profesionales, todas las métricas |

---

## 6. Notas Importantes

### ⚠️ Errores que DEBES evitar:

1. **Look-ahead bias:** NUNCA uses datos del futuro para calcular features, entrenar, o predecir. Si tu backtest es perfecto, probablemente tienes look-ahead bias.

2. **Survivorship bias:** Si usas el S&P 500 actual como universo, estás ignorando empresas que quebraron o fueron removidas del índice.

3. **Transaction costs:** Sin costos de transacción, cualquier estrategia高频 parece rentable. Siempre incluye comisiones y slippage.

4. **Overfitting:** Si tu modelo tiene accuracy > 60% en datos financieros, algo está mal. Accuracy 51-55% es realista.

5. **Data snooping:** Probar 100 combinaciones de parámetros en TODO el histórico y reportar la mejor es hacer trampa. Usa walk-forward.

---

## 7. Recursos y Referencias

- **pyfolio:** github.com/quantopian/pyfolio (inspiración de tear sheets)
- **QuantResearch:** github.com/letianzj/QuantResearch (ejemplos de estrategias)
- **ML for Trading:** github.com/stefan-jansen/machine-learning-for-trading (libro de referencia)
- **QuantConnect:** quantconnect.com (inspiración de arquitectura)

---

> 📝 **Knowledge Wiki:** Al terminar este proyecto, guarda en memoria:
> - Un sistema de trading real tiene 6 componentes: datos → features → modelos → backtest → riesgo → reportes
> - El look-ahead bias es el error más común y más peligroso en finanzas cuantitativas
> - Walk-forward es la única forma honesta de validar estrategias
> - Accuracy > 55% en predicción de dirección de mercado es sospechoso; si lo ves, busca el bug
> - Los costos de transacción y slippage pueden convertir una estrategia "rentable" en una perdedora
> - La gestión de riesgo (position sizing + stop-loss) es tan importante como la señal (alpha)
