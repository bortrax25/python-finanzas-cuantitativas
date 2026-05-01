# U13: Módulos, Paquetes y Arquitectura de Proyecto

> **Lectura previa:** [U12: Funciones Avanzadas — Lambda, Decoradores](./U12-funciones-avanzadas.md)
> **Próxima unidad:** [U14: Errores y Logging Profesional](./U14-errores-logging.md)

---

## 1. Teoría

### 1.1 Módulos — Archivos `.py` reutilizables

Un **módulo** es cualquier archivo Python. Todo el código que escribiste se puede importar.

```python
# finanzas.py (módulo)
def interes_compuesto(capital, tasa, anios):
    return capital * (1 + tasa/100) ** anios

def cagr(vi, vf, anios):
    return ((vf/vi) ** (1/anios) - 1) * 100

# main.py
import finanzas                          # Importa todo el módulo
from finanzas import interes_compuesto    # Importa función específica
from finanzas import interes_compuesto, cagr
import finanzas as fin                   # Alias
```

### 1.2 Paquetes — Directorios con `__init__.py`

Un paquete es un directorio con módulos organizados temáticamente:

```
quantlib/
├── __init__.py
├── pricing.py       # Funciones de valoración (bonos, opciones)
├── riesgo.py        # VaR, CVaR, volatilidad
├── datos.py         # Lectura/escritura de archivos
└── utils.py         # Utilidades generales
```

```python
# quantlib/__init__.py — expone las funciones principales del paquete
from .pricing import valoracion_bono, black_scholes_call
from .riesgo import var_historico, sharpe_ratio, max_drawdown
from .datos import leer_csv_precios, guardar_json

__version__ = "0.1.0"
```

```python
# Uso del paquete
from quantlib import valoracion_bono, sharpe_ratio
# ó
import quantlib
precio = quantlib.valoracion_bono(1000, 5, 4, 10)
```

### 1.3 `if __name__ == "__main__":` — Punto de entrada

```python
# calculadora.py
def sumar(a, b):
    return a + b

if __name__ == "__main__":
    # Solo se ejecuta si corremos: python calculadora.py
    # NO se ejecuta si hacemos: import calculadora
    print("Probando calculadora...")
    print(f"5 + 3 = {sumar(5, 3)}")
```

### 1.4 `requirements.txt` y `pyproject.toml`

**requirements.txt** — dependencias del proyecto:

```
numpy>=1.24
pandas>=2.0
matplotlib>=3.7
scipy>=1.11
```

```bash
# Instalar dependencias de un proyecto
pip install -r requirements.txt
```

**pyproject.toml** — metadatos del proyecto (moderno):

```toml
[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[project]
name = "quantlib"
version = "0.1.0"
description = "Librería de finanzas cuantitativas"
requires-python = ">=3.12"
dependencies = [
    "numpy>=1.24",
    "pandas>=2.0",
    "scipy>=1.11",
]

[project.optional-dependencies]
dev = ["pytest>=7.0", "ruff", "black"]
```

### 1.5 Estructura de proyecto profesional

```
quant-desk/
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── README.md
├── quantlib/                  # Paquete principal
│   ├── __init__.py
│   ├── pricing/
│   │   ├── __init__.py
│   │   ├── bonos.py
│   │   └── derivados.py
│   ├── riesgo/
│   │   ├── __init__.py
│   │   ├── var.py
│   │   └── metricas.py
│   ├── datos/
│   │   ├── __init__.py
│   │   └── io.py
│   └── utils.py
├── notebooks/                 # Jupyter notebooks exploratorios
├── datos/                     # Datos de mercado
└── tests/                     # Tests unitarios
    ├── test_pricing.py
    ├── test_riesgo.py
    └── test_datos.py
```

### 1.6 Organización típica de un desk cuantitativo

En Citadel, Jane Street o JP Morgan, el código se organiza por función:

| Sub-módulo | Responsabilidad | Ejemplo de funciones |
|-----------|----------------|---------------------|
| `pricing` | Valoración de instrumentos | `valoracion_bono()`, `black_scholes()` |
| `riesgo` | Métricas de riesgo | `var_historico()`, `cvar()`, `sharpe_ratio()` |
| `datos` | Ingesta y limpieza de datos | `leer_csv_precios()`, `descargar_yfinance()` |
| `utils` | Utilidades generales | `cagr()`, `interes_compuesto()`, `timer()` |

---

## 2. Práctica

### 2.1 Ejercicio guiado: Crear el paquete `quantlib/`

```python
# Paso 1: Crear estructura de directorios
# quantlib/__init__.py, quantlib/pricing.py, quantlib/riesgo.py, quantlib/datos.py

# quantlib/pricing.py
def valoracion_bono(valor_nominal, cupon_pct, tasa_mercado, anios):
    cupon = valor_nominal * (cupon_pct / 100)
    tasa = tasa_mercado / 100
    vp_cupones = sum(cupon / (1 + tasa) ** t for t in range(1, anios + 1))
    vp_nominal = valor_nominal / (1 + tasa) ** anios
    return vp_cupones + vp_nominal

def cuota_prestamo(monto, tasa_anual, plazo_meses):
    i = (tasa_anual / 100) / 12
    return monto * (i * (1 + i) ** plazo_meses) / ((1 + i) ** plazo_meses - 1)

# quantlib/riesgo.py
def sharpe_ratio(rendimiento, tasa_libre, volatilidad):
    return (rendimiento - tasa_libre) / volatilidad

def var_historico(rendimientos, confianza=0.95):
    ordenados = sorted(rendimientos)
    indice = int(len(ordenados) * (1 - confianza))
    return -ordenados[indice]

# quantlib/datos.py
import csv
import json
from pathlib import Path

def leer_csv_precios(ruta):
    with open(ruta, "r") as f:
        return list(csv.DictReader(f))

def guardar_json(datos, ruta):
    Path(ruta).parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w") as f:
        json.dump(datos, f, indent=2)
```

### 2.2 Ejercicio guiado: Usar el paquete

```python
# main.py — punto de entrada del proyecto
from quantlib.pricing import valoracion_bono, cuota_prestamo
from quantlib.riesgo import sharpe_ratio, var_historico

# Valorar bono
bono = valoracion_bono(1000, 5, 4, 10)
print(f"Bono: ${bono:,.2f}")

# Calcular riesgo
rendimientos = [1.2, -0.5, 2.1, -3.8, 0.9, -1.2, 2.5, -0.8]
print(f"Sharpe: {sharpe_ratio(12, 4, 18):.2f}")
print(f"VaR 95%: {var_historico(rendimientos):.2f}%")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Estructura de un desk cuantitativo real

```
desk-fixed-income/
├── src/
│   ├── pricing/
│   │   ├── bonds.py          # Valoración de bonos, YTM, duration
│   │   ├── swaps.py          # IRS, CDS
│   │   └── options.py        # Caps, floors, swaptions
│   ├── risk/
│   │   ├── market_risk.py    # VaR, stress testing
│   │   ├── credit_risk.py    # PD, LGD, EAD
│   │   └── greeks.py         # Delta, Gamma, Vega
│   ├── data/
│   │   ├── bloomberg.py      # Conexión Bloomberg API
│   │   ├── reuters.py        # Conexión Reuters
│   │   └── curves.py         # Curvas de rendimiento
│   └── utils/
│       ├── date_utils.py     # Calendarios de días hábiles
│       └── math_utils.py     # Interpolación, optimización
├── config/
│   └── desk_config.yaml       # Configuración del desk
├── notebooks/
│   └── daily_pnl.ipynb        # P&L diario
└── tests/
    └── test_pricing.py
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-3/U13_ejercicios.py`

1. **Crear submódulo:** Implementa las funciones de un submódulo `riesgo.py` con VaR, Sharpe, volatilidad.

2. **`if __name__ == "__main__"`:** Escribe un script que se comporte diferente como módulo vs script.

3. **Estructura de paquete:** Organiza funciones existentes en un paquete `quantlib/` con submódulos.

4. **Importar y usar:** Importa y usa funciones de tu paquete, demostrando diferentes formas de import.

---

## 5. Resumen

| Concepto | Sintaxis / Archivo |
|---------|-------------------|
| Módulo | `import modulo` |
| Función específica | `from modulo import funcion` |
| Paquete | Directorio con `__init__.py` |
| Entry point | `if __name__ == "__main__":` |
| Dependencias | `requirements.txt` |
| Metadatos | `pyproject.toml` |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre `import modulo` y `from modulo import funcion`?
2. ¿Para qué sirve `__init__.py`?
3. ¿Qué hace `if __name__ == "__main__":`?
4. ¿Qué diferencia hay entre `requirements.txt` y `pyproject.toml`?

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U13.md`: imports, __init__.py, if __name__, requirements.txt, pyproject.toml
> - `project-U13.md`: Estructura del paquete quantlib/, desk cuantitativo real
