# Sistema de Trading Cuantitativo End-to-End

> **Unidad:** U42 — Fase 10  
> **Tipo:** Proyecto Integrador Avanzado  
> **Stack:** pandas + scikit-learn + XGBoost + LightGBM + SQLite

---

## Descripción

Sistema completo de trading cuantitativo que integra:
1. **Pipeline de datos:** Descarga, validación y almacenamiento de precios
2. **Feature engineering:** 30+ features financieras para ML
3. **3 modelos ML:** Random Forest, XGBoost, LightGBM con ensemble
4. **Backtest:** Motor vectorizado con costos de transacción
5. **Risk management:** Position sizing, stop-loss, límites
6. **Tear sheet:** Reporte de performance completo (estilo pyfolio)

El sistema está diseñado para correr diariamente después del cierre del mercado, generando señales de trading para el día siguiente.

---

## Instalación

```bash
cd documentacion/proyectos/trading-system
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Ejecución

```bash
# Pipeline diario completo
python pipeline.py

# Solo backtest (sin descarga de datos)
python pipeline.py --backtest-only

# Con fechas específicas
python pipeline.py --start 2015-01-01 --end 2024-12-31
```

---

## Estructura del Proyecto

```
trading-system/
├── README.md
├── requirements.txt
├── config.py                # Parámetros globales
├── pipeline.py              # Orquestador principal
├── data/
│   ├── ingesta.py           # Descarga de datos de mercado
│   ├── limpieza.py          # Validación e imputación
│   └── almacenamiento.py    # Interfaz SQLite
├── features/
│   ├── ingenieria.py        # Feature engineering financiero
│   ├── tecnicas.py          # Indicadores técnicos
│   └── seleccion.py         # Selección de features
├── modelos/
│   ├── base.py              # Clase base ModeloBase
│   ├── random_forest.py     # Modelo RF
│   ├── xgboost_model.py     # Modelo XGBoost
│   ├── lightgbm_model.py    # Modelo LightGBM
│   └── ensemble.py          # Ensemble de modelos
├── backtest/
│   ├── motor.py             # Motor de backtesting
│   ├── costos.py            # Modelo de costos
│   ├── metricas.py          # Métricas de performance
│   └── walk_forward.py      # Walk-forward validation
├── riesgo/
│   ├── posicionamiento.py   # Position sizing
│   ├── limites.py           # Stop-loss, take-profit
│   └── var_cvar.py          # VaR del portafolio
├── reportes/
│   ├── tear_sheet.py        # Tear sheet completo
│   └── graficos.py          # Gráficos (equity, drawdown)
└── tests/
    ├── test_features.py
    ├── test_modelos.py
    ├── test_backtest.py
    └── test_riesgo.py
```

---

## Flujo de Trabajo

### Pipeline Diario

```
18:00 → Descargar datos del día
18:05 → Validar y limpiar
18:10 → Almacenar en SQLite
18:15 → Recalcular features
18:20 → Predecir con 3 modelos
18:25 → Ensemble de predicciones
18:30 → Seleccionar top 5 activos
18:35 → Verificar límites de riesgo
18:40 → Generar órdenes
18:45 → Enviar resumen por email
```

### Backtest Completo

```
1. Cargar 10+ años de datos históricos
2. Walk-forward: reentrenar cada 6 meses
3. Cada período: features → predicciones → top 5 → backtest
4. Acumular equity curve
5. Generar tear sheet final
```

---

## Estrategia de Trading

- **Tipo:** Long-only, equally weighted
- **Universo:** 20+ acciones del S&P 500
- **Señal:** Probabilidad de subida (modelo ML) en horizonte de 5 días
- **Ejecución:** Comprar top 5 activos con mayor probabilidad
- **Rebalanceo:** Diario (vender si sale del top 5)
- **Costos:** 10 bps comisión + 5 bps slippage

---

## Métricas de Performance Esperadas

| Métrica | Objetivo Realista |
|---------|-------------------|
| Sharpe Ratio | 0.3 — 0.8 |
| Max Drawdown | -15% — -30% |
| Win Rate | 50% — 55% |
| Profit Factor | 1.1 — 1.5 |
| Retorno Anual Exceso | 3% — 10% vs benchmark |

---

## Modelos ML

### Random Forest
- Baseline sólido e interpretable
- Hiperparámetros: n_estimators=200, max_depth=5, min_samples_leaf=20

### XGBoost
- Gradient boosting con regularización L1/L2
- Hiperparámetros: learning_rate=0.01, max_depth=5, reg_alpha=0.1

### LightGBM
- Leaf-wise boosting (más rápido)
- Hiperparámetros: learning_rate=0.01, num_leaves=31, reg_alpha=0.1

### Ensemble
- Promedio simple de probabilidades de los 3 modelos
- Opcional: pesos dinámicos basados en performance reciente

---

## Gestión de Riesgo

### Position Sizing
- **Equal Weight:** 20% capital por posición (5 posiciones)
- **Inverse Volatility:** Capital ∝ 1/σ (menos en activos volátiles)
- **Kelly Criterion:** f = (p * b - q) / b (simplificado)

### Stop-Loss
- **Fixed:** -5% desde precio de entrada
- **Trailing:** -10% desde máximo alcanzado
- **Time-based:** Salir después de 10 días sin ganancia > 1%

### Límites
- Max exposición por activo: 25%
- Max posiciones simultáneas: 5
- Max drawdown diario: -3% (circuit breaker)

---

## Tear Sheet (Reporte Final)

El tear sheet debe incluir visualizaciones profesionales:

1. Equity curve con benchmark
2. Drawdown (underwater plot)
3. Monthly returns heatmap
4. Rolling Sharpe (12 meses)
5. Distribución de retornos diarios
6. Top 10 mejores/peores días
7. Tabla resumen de métricas

---

## ⚠️ Errores a Evitar

- **Look-ahead bias:** Nunca usar datos futuros para features
- **Survivorship bias:** Universo debe reflejar composición histórica
- **Transaction costs:** Siempre incluir comisiones y slippage
- **Overfitting:** Accuracy > 60% es sospechoso
- **Data snooping:** Walk-forward validation obligatorio

---

## Referencia

Ver `documentacion/teoria/fase-10/U42-sistema-trading.md` para la especificación completa.
