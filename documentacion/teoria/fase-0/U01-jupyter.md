# U01: Jupyter Notebooks y el Flujo de Trabajo Cuantitativo

> **Lectura previa:** [U00: Preparando tu entorno profesional](./U00-setup.md)
> **Próxima unidad:** [U02: Variables, tipos de datos y el lenguaje de los mercados](../fase-1/U02-variables-tipos.md)

---

## 1. Teoría

### 1.1 ¿Qué es Jupyter Notebook?

Un **Jupyter Notebook** (`.ipynb`) es un documento interactivo que combina:
- **Código** (Python, R, Julia)
- **Texto** (Markdown con formato)
- **Ecuaciones** (LaTeX)
- **Gráficos** (matplotlib, plotly)
- **Tablas** (DataFrames de pandas)

En finanzas es el estándar para research y análisis exploratorio. En Citadel, los quants usan notebooks para probar hipótesis, visualizar señales de trading y documentar sus hallazgos antes de llevar el código a producción.

```python
# Ejemplo: una celda en Jupyter
import matplotlib.pyplot as plt
import numpy as np

# Simular precio de una acción con GBM
precio = 100
precios = [precio]
for _ in range(252):
    precio *= np.exp(0.0008 + 0.015 * np.random.randn())
    precios.append(precio)

plt.plot(precios)
plt.title("Simulación de Precio con GBM (1 año)")
plt.ylabel("Precio ($)")
plt.grid(True)
plt.show()
```

### 1.2 Jupyter Notebook vs Jupyter Lab

| Característica | Jupyter Notebook | Jupyter Lab |
|---------------|-----------------|-------------|
| Interfaz | Navegador, un archivo por pestaña | IDE completo con paneles |
| Editor de texto | No | Sí (archivos .py, .md) |
| Terminal | No | Sí, integrada |
| Múltiples notebooks | Pestañas del navegador | Paneles arrastrables |
| Extensiones | Vía nbextensions | Vía JupyterLab extensions |
| Consola Python | No | Sí, interactiva |

**Recomendación:** Jupyter Lab para trabajo serio. Instálalo con:

```bash
pip install jupyterlab
jupyter lab
```

### 1.3 Celdas: Código vs Markdown

Jupyter tiene dos tipos de celdas:

**Celda de código (Code):**
```python
# Ejecuta con Shift+Enter
capital = 10000
tasa = 0.08
monto = capital * (1 + tasa) ** 5
print(f"Monto final: ${monto:,.2f}")
```

**Celda Markdown:**
```markdown
## Análisis de Portafolio

Este notebook analiza el rendimiento del portafolio **Q1 2024**.

| Activo | Peso | Rendimiento |
|--------|------|-------------|
| AAPL   | 30%  | +15.2%      |
| MSFT   | 25%  | +22.1%      |

La fórmula del Sharpe Ratio es:

$$Sharpe = \frac{R_p - R_f}{\sigma_p}$$
```

> 💡 Usa Markdown para **documentar tu análisis**. En banca, un notebook sin texto es ilegible para tu MD. Explica qué hipótesis pruebas y por qué.

### 1.4 Atajos de teclado esenciales

| Atajo | Acción |
|-------|--------|
| `Shift + Enter` | Ejecutar celda y avanzar |
| `Ctrl + Enter` | Ejecutar celda sin avanzar |
| `Alt + Enter` | Ejecutar y crear nueva celda abajo |
| `Esc + a` | Insertar celda arriba |
| `Esc + b` | Insertar celda abajo |
| `Esc + dd` | Eliminar celda |
| `Esc + m` | Convertir a Markdown |
| `Esc + y` | Convertir a Code |
| `Esc + 0 0` | Reiniciar kernel |
| `Tab` | Autocompletado |

### 1.5 Magics — Comandos especiales de Jupyter

Los **magics** son comandos que empiezan con `%` o `%%` y extienden Jupyter:

**Magics de línea (`%`):**

```python
# %timeit — medir tiempo de ejecución (CRÍTICO en finanzas)
import numpy as np
datos = list(range(1000000))

%timeit sum(datos)           # Python puro
%timeit np.sum(datos)        # NumPy vectorizado
# Output típico:
# 3.45 ms ± 45 µs per loop (Python)
# 245 µs ± 3 µs per loop (NumPy) ← ~14× más rápido

# %matplotlib inline — gráficos dentro del notebook
%matplotlib inline
import matplotlib.pyplot as plt

# %who — listar variables definidas
a = 10
b = "finanzas"
%who
# a   b

# %reset — eliminar todas las variables y empezar de cero
%reset -f
```

**Magics de celda (`%%`):**

```python
# %%timeit — medir tiempo de toda la celda
%%timeit
total = 0
for i in range(10000):
    total += i ** 2

# %%writefile — guardar celda como archivo .py
%%writefile mi_funcion.py
def interes_compuesto(capital, tasa, anios):
    return capital * (1 + tasa/100) ** anios
```

> 💡 `%timeit` es tu mejor amigo como quant. Siempre que optimices un cálculo (pricing de opciones, VaR Monte Carlo, backtesting), úsalo para comparar implementaciones.

### 1.6 Google Colab — Jupyter en la nube

Google Colaboratory (Colab) es Jupyter alojado en Google, gratuito, con GPU incluida.

**Ventajas:**
- Sin instalación
- GPU/TPU gratis para ML financiero
- Compartir como Google Docs
- Montar Google Drive para datos

**Desventajas:**
- Límite de 12 horas por sesión
- Datos sensibles no deben subirse (compliance)
- Menos control que local

```python
# En Colab, montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Leer datos desde Drive
import pandas as pd
df = pd.read_csv("/content/drive/MyDrive/datos/precios.csv")
```

### 1.7 El flujo de trabajo cuantitativo en notebooks

Un quant típico en Citadel o Jane Street sigue este ciclo en Jupyter:

1. **Cargar datos** — precios, fundamentales, datos macro
2. **Explorar** — visualizaciones rápidas, estadísticas descriptivas
3. **Hipotetizar** — "si el VIX sube, el momentum funciona mejor"
4. **Testear** — código para validar la hipótesis con datos históricos
5. **Visualizar** — gráficos que cuenten la historia
6. **Documentar** — Markdown explicando hallazgos y limitaciones
7. **Extraer** — mover funciones probadas a archivos `.py` para producción

---

## 2. Práctica

### 2.1 Ejercicio guiado: Crear y ejecutar un notebook

```bash
# Instalar Jupyter Lab si no lo tienes
pip install jupyterlab

# Iniciar
cd ~/Desktop/ZED
jupyter lab
```

En el navegador, crea un nuevo notebook (`Python 3`) y escribe:

**Celda 1 (Markdown):**
```markdown
# Mi Primer Notebook Financiero

Este notebook analiza el rendimiento de un portafolio simulado.

**Autor:** [Tu nombre]
**Fecha:** [Fecha actual]
```

**Celda 2 (Código):**
```python
import numpy as np
import matplotlib.pyplot as plt

# Simular 252 días de precios (1 año de trading)
np.random.seed(42)
precio_inicial = 100
rendimientos = np.random.normal(0.0008, 0.015, 252)
precios = precio_inicial * np.exp(np.cumsum(rendimientos))

# Graficar
plt.figure(figsize=(12, 5))
plt.plot(precios, linewidth=1.5)
plt.title("Simulación de Precio — 1 Año de Trading", fontsize=14)
plt.xlabel("Día de Trading")
plt.ylabel("Precio ($)")
plt.grid(True, alpha=0.3)
plt.show()
```

**Celda 3 (Código):**
```python
# Calcular estadísticas
retornos_diarios = (precios[1:] - precios[:-1]) / precios[:-1]
rendimiento_total = (precios[-1] - precios[0]) / precios[0] * 100
volatilidad_anual = np.std(retornos_diarios) * np.sqrt(252) * 100
sharpe = (np.mean(retornos_diarios) * 252 - 0.04) / (np.std(retornos_diarios) * np.sqrt(252))

print(f"Precio inicial: ${precios[0]:.2f}")
print(f"Precio final: ${precios[-1]:.2f}")
print(f"Rendimiento total: {rendimiento_total:.2f}%")
print(f"Volatilidad anualizada: {volatilidad_anual:.2f}%")
print(f"Sharpe Ratio: {sharpe:.2f}")
```

**Output:**
```
Precio inicial: $100.00
Precio final: $122.34
Rendimiento total: 22.34%
Volatilidad anualizada: 23.82%
Sharpe Ratio: 0.73
```

### 2.2 Ejercicio guiado: Usar magics

```python
# Medir operaciones vectorizadas vs loops
import numpy as np

datos = np.random.randn(1_000_000)

print("Suma con Python puro:")
%timeit sum(datos)

print("\nSuma con NumPy:")
%timeit np.sum(datos)

print("\nMódulo con Python puro:")
%timeit [abs(x) for x in datos[:10000]]

print("\nMódulo con NumPy:")
%timeit np.abs(datos[:10000])
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 ¿Cómo usan los quants los notebooks?

En Jane Street, un quant research sigue este flujo típico en Jupyter:

```python
# Celda 1: Cargar datos del S&P 500
import yfinance as yf
import pandas as pd

tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
datos = yf.download(tickers, start="2023-01-01", end="2024-01-01")["Adj Close"]

# Celda 2: Explorar retornos
retornos = datos.pct_change().dropna()
retornos.describe()

# Celda 3: Matriz de correlación (heatmap)
import seaborn as sns
plt.figure(figsize=(8, 6))
sns.heatmap(retornos.corr(), annot=True, cmap="coolwarm", center=0)
plt.title("Matriz de Correlación — S&P 5")
plt.show()

# Celda 4: Hipótesis — ¿AAPL lidera los movimientos?
# Si AAPL sube > 1%, ¿los demás también suben?
senal = retornos["AAPL"] > 0.01
for ticker in tickers[1:]:
    prob = (retornos.loc[senal, ticker] > 0).mean()
    print(f"Si AAPL sube >1%, {ticker} sube el {prob:.0%} de las veces")
```

### 3.2 Notebooks en entrevistas técnicas

Muchos procesos de selección para roles cuantitativos (Citadel, Two Sigma, HRT) incluyen un "take-home project" en Jupyter. Te dan datos y piden análisis. Un buen notebook:

1. Explica qué hipótesis pruebas y por qué (Markdown)
2. Muestra limpieza de datos (valores nulos, outliers)
3. Visualiza hallazgos clave
4. Concluye con recomendaciones accionables
5. El código es limpio, con funciones reutilizables

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios están en `documentacion/ejercicios/fase-0/U01_ejercicios.py`

1. **Primer notebook financiero:** Crea un notebook que cargue precios desde un CSV simulado y grafique la evolución del precio.

2. **Magics y performance:** Usa `%timeit` para comparar el cálculo de la volatilidad con un loop `for` vs con NumPy (simulado con listas).

3. **Reporte interactivo:** Simula un reporte de análisis de portafolio que muestre tabla de rendimientos y gráfico de torta de pesos (usa matplotlib).

4. **Flujo cuantitativo:** Escribe un script que tome una lista de precios, calcule retornos, volatilidad, y Sharpe ratio, todo documentado con comentarios estilo notebook.

---

## 5. Resumen

| Concepto | Ejemplo / Atajo |
|---------|----------------|
| Notebook | `.ipynb` que combina código + Markdown + gráficos |
| Jupyter Lab | IDE completo con paneles y terminal |
| Ejecutar celda | `Shift + Enter` |
| Markdown | `Esc + m` |
| Code | `Esc + y` |
| `%timeit` | Medir tiempo de ejecución |
| `%matplotlib inline` | Gráficos dentro del notebook |
| `%%writefile` | Guardar celda como `.py` |
| Google Colab | Jupyter en la nube con GPU gratis |

---

## ✅ Autoevaluación

1. ¿Cuál es la diferencia entre Jupyter Notebook y Jupyter Lab?
2. ¿Qué hace el magic `%timeit` y por qué es útil en finanzas?
3. ¿Cómo conviertes una celda de código a Markdown?
4. ¿Por qué los quants documentan sus notebooks con Markdown?
5. Crea un notebook que simule 100 precios diarios y grafique el drawdown.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - `reference-U01.md`: Atajos de Jupyter, magics esenciales, flujo de trabajo cuantitativo
> - `project-U01.md`: Primer notebook financiero con simulación de precios y análisis
