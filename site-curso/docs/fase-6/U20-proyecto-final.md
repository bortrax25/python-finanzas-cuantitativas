# U20: Proyecto Final Integrador

> **Lectura previa:** [U19: Modelos de riesgo](./U19-modelos-riesgo.md)

## Construye tu Propio Analizador Financiero

Aplica todo lo aprendido en un solo proyecto.

### Objetivo

Crear un programa completo que:
1. Cargue datos de mercado (CSV o API)
2. Calcule métricas de rendimiento, riesgo y valuación
3. Genere un reporte de análisis

### Módulos del proyecto

```
mi_analizador/
├── __init__.py
├── datos.py          # Carga y limpieza de datos
├── metricas.py       # Cálculos financieros
├── riesgo.py         # VaR, CVaR, Monte Carlo
├── bonos.py          # Valoración de bonos
├── reporte.py        # Generación de reportes
└── main.py           # Punto de entrada
```

### Requisitos mínimos

- [ ] Cargar datos históricos de al menos 3 activos
- [ ] Calcular rendimientos, volatilidad, Sharpe
- [ ] Matriz de correlación y covarianza
- [ ] Optimizar portafolio (mínima varianza y máximo Sharpe)
- [ ] VaR del portafolio por método histórico y paramétrico
- [ ] Valorar un bono corporativo
- [ ] Generar reporte en consola y CSV
- [ ] Usar funciones con type hints y docstrings
- [ ] Estructura modular con `if __name__ == "__main__"`

### Esqueleto inicial

```python
# main.py
import numpy as np
import pandas as pd
from metricas import rendimiento, volatilidad, sharpe_ratio
from riesgo import var_historico, var_parametrico
from bonos import precio_bono, ytm

def main():
    # 1. Cargar datos
    precios = pd.read_csv("precios.csv", index_col=0, parse_dates=True)

    # 2. Calcular métricas
    retornos = precios.pct_change().dropna()
    ret_anual = rendimiento(retornos) * 252
    vol_anual = volatilidad(retornos) * np.sqrt(252)
    sharpe = sharpe_ratio(ret_anual, 0.04, vol_anual)

    # 3. Riesgo
    var_95_hist = var_historico(retornos, 95)
    var_95_param = var_parametrico(retornos, 95)

    # 4. Reporte
    print("=== Reporte de Análisis Financiero ===")
    print(f"Retorno anual: {ret_anual.mean():.2%}")
    print(f"Volatilidad anual: {vol_anual.mean():.2%}")
    print(f"Sharpe Ratio: {sharpe.mean():.2f}")
    print(f"VaR 95% Histórico: {var_95_hist:.2%}")
    print(f"VaR 95% Paramétrico: {var_95_param:.2%}")

if __name__ == "__main__":
    main()
```

### Datos de ejemplo

Crea un CSV con este formato:
```csv
Date,AAPL,MSFT,TSLA
2024-01-01,150.00,280.00,900.00
2024-01-02,152.00,282.00,895.00
...
```

### Rúbrica de autoevaluación

| Criterio | Peso |
|---------|------|
| Carga datos correctamente | 10% |
| Cálculos financieros correctos | 25% |
| Métodos de riesgo implementados | 20% |
| Optimización de portafolio | 20% |
| Código modular y documentado | 15% |
| Reporte generado | 10% |

---

> 🎉 **¡Felicidades!** Has completado las 20 unidades del curso Python para Finanzas Cuantitativas. Este proyecto final demuestra que dominas desde variables hasta modelos de riesgo.
