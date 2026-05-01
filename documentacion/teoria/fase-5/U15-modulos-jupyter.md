# U15: Módulos, Paquetes e Introducción a Jupyter

> **Lectura previa:** [U14: args, kwargs, lambda y scope](./U14-avanzado-funciones.md)
> **Próxima unidad:** [U16: NumPy y Pandas para finanzas](../fase-6/U16-numpy-pandas.md)

---

## 1. Teoría

### 1.1 Módulos — Archivos `.py` reutilizables

Un **módulo** es cualquier archivo Python. Puedes importar sus funciones en otros archivos.

```python
# finanzas.py (módulo)
def interes_compuesto(capital, tasa, anios):
    return capital * (1 + tasa/100) ** anios

def cagr(vi, vf, anios):
    return ((vf/vi) ** (1/anios) - 1) * 100

# main.py (usa el módulo)
import finanzas

monto = finanzas.interes_compuesto(10000, 8, 10)

# Importar funciones específicas
from finanzas import interes_compuesto, cagr

# Importar todo (no recomendado)
from finanzas import *

# Alias
import finanzas as fin
```

### 1.2 Paquetes — Directorios con módulos

Un paquete es un directorio con un archivo `__init__.py` y múltiples módulos.

```
📁 mi_libreria/
├── __init__.py
├── bonos.py
├── acciones.py
└── riesgo.py
```

```python
# __init__.py
from .bonos import valoracion_bono
from .acciones import sharpe_ratio
from .riesgo import var_historico

# Uso
from mi_libreria import valoracion_bono, var_historico
```

### 1.3 `if __name__ == "__main__":` — Punto de entrada

Permite que un archivo funcione como módulo Y como script.

```python
# calculadora.py
def sumar(a, b):
    return a + b

if __name__ == "__main__":
    # Solo se ejecuta si corremos python calculadora.py
    print("Probando calculadora...")
    print(sumar(5, 3))
```

### 1.4 Bibliotecas estándar útiles

```python
import math
math.sqrt(16)        # 4.0
math.log(100)        # logaritmo natural

from datetime import date, timedelta
hoy = date.today()
ayer = hoy - timedelta(days=1)

import json
datos = {"AAPL": 175.50, "MSFT": 310.00}
json_str = json.dumps(datos, indent=2)
recuperado = json.loads(json_str)

import random
random.seed(42)
precio = 100 * (1 + random.gauss(0.08, 0.15))
```

### 1.5 Introducción a Jupyter Notebooks

Los **Jupyter Notebooks** (`.ipynb`) combinan código, texto Markdown, ecuaciones LaTeX y gráficos en un solo documento interactivo.

**Ventajas en finanzas:**
- Iteración rápida en análisis exploratorio
- Visualizaciones inline (matplotlib)
- Documentación narrativa del análisis
- Estándar en la industria

```python
# En una celda de Jupyter:
import pandas as pd
import matplotlib.pyplot as plt

# Cargar datos
df = pd.read_csv("precios.csv")

# Visualizar
df["Close"].plot(title="Precio de cierre")
plt.show()
```

**Atajos Jupyter:**
| Atajo | Acción |
|-------|--------|
| `Shift + Enter` | Ejecutar celda |
| `Ctrl + Enter` | Ejecutar y quedarse |
| `a` / `b` | Insertar celda arriba/abajo |
| `dd` | Eliminar celda |
| `m` / `y` | Markdown / Code |

---

## 2. Práctica

### 2.1 Organizar el proyecto

```bash
# Estructura recomendada para FASE 6
ZED/
├── mis_funciones/
│   ├── __init__.py
│   ├── finanzas.py       # Cálculos financieros
│   └── analisis.py       # Análisis de datos
└── notebooks/
    └── U16_intro.ipynb   # Notebook de prácticas
```

### 2.2 Crear primer notebook

```python
# Celda 1: Markdown
# # Mi Primer Notebook Financiero
# Análisis de precios históricos

# Celda 2: Código
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Crear datos de ejemplo
fechas = pd.date_range("2024-01-01", periods=100)
precios = 100 * (1 + np.random.randn(100).cumsum() * 0.02)

df = pd.DataFrame({"Fecha": fechas, "Precio": precios})
df.set_index("Fecha", inplace=True)

# Graficar
df["Precio"].plot(figsize=(10, 4), title="Simulación de Precio")
plt.ylabel("Precio ($)")
plt.grid(True)
plt.show()

# Celda 3: Cálculos
retornos = df["Precio"].pct_change().dropna()
print(f"Retorno promedio diario: {retornos.mean():.4%}")
print(f"Volatilidad diaria: {retornos.std():.4%}")
print(f"Sharpe Ratio (anualizado, rf=4%): {((retornos.mean()*252 - 0.04) / (retornos.std() * 252**0.5)):.2f}")
```

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Módulo | `import mi_modulo` |
| Paquete | `from mi_pkg import func` |
| Entry point | `if __name__ == "__main__":` |
| JSON | `json.dumps/dumps` |
| Jupyter | `.ipynb`, Shift+Enter |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre `import modulo` y `from modulo import funcion`?
2. ¿Qué hace `if __name__ == "__main__":`?
3. ¿Para qué sirven los notebooks en finanzas?

---

> 📝 **Knowledge Wiki:** Guarda `reference-U15.md` (estructura proyecto, comandos Jupyter).
