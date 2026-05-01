# ✅ Soluciones: U12 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U12_soluciones)

---

```python
# U12: SOLUCIONES — Funciones Avanzadas: Lambda, Decoradores y Closures

# ============================================================
# Ejercicio 1: Filtro y Ranking con Lambda
# ============================================================
print("=== Ejercicio 1: Filtro y Ranking con Lambda ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
    ("PFE", 14, 5),
    ("NVDA", 45, 30),
    ("BAC", 8, 9),
]

value_growth = list(filter(lambda a: a[1] < 15 and a[2] > 10, acciones))
print(f"Value+Growth: {value_growth}")

top_crecimiento = sorted(acciones, key=lambda a: a[2], reverse=True)
print(f"Top crecimiento: {top_crecimiento}")


# ============================================================
# Ejercicio 2: Ranking por Sharpe
# ============================================================
print("\\n=== Ejercicio 2: Ranking por Sharpe ===")
rf = 4
activos = [
    {"ticker": "AAPL", "retorno": 15.2, "volatilidad": 22.1},
    {"ticker": "MSFT", "retorno": 18.5, "volatilidad": 20.8},
    {"ticker": "TSLA", "retorno": 25.0, "volatilidad": 45.3},
    {"ticker": "JPM", "retorno": 10.8, "volatilidad": 18.2},
    {"ticker": "XOM", "retorno": 8.5, "volatilidad": 15.5},
    {"ticker": "NVDA", "retorno": 30.0, "volatilidad": 40.0},
]

for a in activos:
    a["sharpe"] = (a["retorno"] - rf) / a["volatilidad"]

ranking = sorted(activos, key=lambda a: a["sharpe"], reverse=True)

print("Ranking por Sharpe (rf=4%):")
for i, a in enumerate(ranking, start=1):
    print(f"{i}. {a['ticker']} Sharpe={a['sharpe']:.2f} (ret={a['retorno']:.1f}%, vol={a['volatilidad']:.1f}%)")


# ============================================================
# Ejercicio 3: Decorador @medir_tiempo
# ============================================================
print("\\n=== Ejercicio 3: Decorador @medir_tiempo ===")
import time
from functools import wraps

def medir_tiempo(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        inicio = time.perf_counter()
        resultado = func(*args, **kwargs)
        duracion = time.perf_counter() - inicio
        print(f"[TIMER] {func.__name__}: {duracion:.6f}s")
        return resultado
    return wrapper

@medir_tiempo
def calcular_var_historico(rendimientos, confianza=0.95):
    """VaR histórico como el percentil (1-confianza) de los rendimientos."""
    ordenados = sorted(rendimientos)
    indice = int(len(ordenados) * (1 - confianza))
    return -ordenados[indice]

rendimientos = [1.2, -0.5, 2.1, -3.8, 0.9, -1.2, 2.5, -0.8, 1.5, -2.3,
                0.7, -1.1, 3.2, -0.4, 1.8, -2.0, 0.5, -1.5, 2.8, -0.6]
var_95 = calcular_var_historico(rendimientos, 0.95)
print(f"VaR 95%: {var_95:.2f}%")


# ============================================================
# Ejercicio 4: Decorador @registrar_operacion
# ============================================================
print("\\n=== Ejercicio 4: Decorador @registrar_operacion ===")
from datetime import datetime

def registrar_operacion(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {func.__name__}({args}, {kwargs})")
        resultado = func(*args, **kwargs)
        print(f"[{timestamp}] Resultado: {resultado}")
        return resultado
    return wrapper

@registrar_operacion
def ejecutar_trade(ticker, tipo, cantidad, precio):
    return {"ticker": ticker, "monto_total": cantidad * precio}

resultado = ejecutar_trade("AAPL", "compra", 100, 175.50)
print(f"Resultado final: {resultado}")
```

---

> [📥 Descargar archivo .py](U12_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
