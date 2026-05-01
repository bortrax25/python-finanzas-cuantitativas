# ✅ Soluciones: U01 — Fase 0

> [← Volver a ejercicios Fase 0](index.md) | [📥 Descargar .py](U01_soluciones)

---

```python
# U01: SOLUCIONES — Jupyter Notebooks y Flujo de Trabajo Cuantitativo

# ============================================================
# Ejercicio 1: Simulación de precios y gráfico
# ============================================================
print("=== Ejercicio 1: Simulación de Precios ===")
import random

random.seed(123)
precio = 150.00
media_diaria = 0.0005
vol_diaria = 0.015
dias = 252

precios = [precio]

for _ in range(dias):
    retorno = random.gauss(media_diaria, vol_diaria)
    precio *= (1 + retorno)
    precios.append(precio)

rendimiento_total = (precios[-1] - precios[0]) / precios[0] * 100

print(f"Precio inicial: ${precios[0]:.2f}")
print(f"Precio final: ${precios[-1]:.2f}")
print(f"Rendimiento total: {rendimiento_total:.2f}%")
print("(En Jupyter se graficaría con plt.plot(precios))")


# ============================================================
# Ejercicio 2: Estadísticas del Activo
# ============================================================
print("\\n=== Ejercicio 2: Estadísticas del Activo ===")

retornos_diarios_e2 = []
for i in range(1, len(precios)):
    r = (precios[i] - precios[i-1]) / precios[i-1]
    retornos_diarios_e2.append(r)

n = len(retornos_diarios_e2)
promedio_diario = sum(retornos_diarios_e2) / n
varianza = sum((r - promedio_diario) ** 2 for r in retornos_diarios_e2) / (n - 1)
vol_diaria_calc = varianza ** 0.5
vol_anual = vol_diaria_calc * (252 ** 0.5)
retorno_total = (precios[-1] - precios[0]) / precios[0] * 100

print(f"Retorno diario promedio: {promedio_diario:.4%}")
print(f"Volatilidad diaria: {vol_diaria_calc:.4%}")
print(f"Volatilidad anualizada: {vol_anual:.2%}")
print(f"Retorno total acumulado: {retorno_total:.2f}%")


# ============================================================
# Ejercicio 3: Reporte de Portafolio
# ============================================================
print("\\n=== Ejercicio 3: Reporte de Portafolio ===")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

portafolio = [
    ("AAPL", 30.0, 15.2),
    ("MSFT", 25.0, 22.1),
    ("GOOGL", 20.0, 8.5),
    ("AMZN", 15.0, -3.2),
    ("META", 10.0, 12.8),
]

rendimiento_ponderado = 0

print(f"{'Activo':<8} {'Peso':>8} {'Rendimiento':>14}")
for ticker, peso, rend in portafolio:
    print(f"{ticker:<8} {peso:>7.1f}% {rend:>+13.2f}%")
    rendimiento_ponderado += peso * rend / 100

print("-" * 35)
print(f"Portafolio: 100.0% | Rend. ponderado: {rendimiento_ponderado:.2f}%")

# Gráfico de torta
tickers = [p[0] for p in portafolio]
pesos = [p[1] for p in portafolio]
colores = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

plt.figure(figsize=(7, 7))
plt.pie(pesos, labels=tickers, autopct="%1.1f%%", colors=colores, startangle=90)
plt.title("Distribución del Portafolio")
plt.savefig("/tmp/U01_portafolio.png", dpi=100)
print("[Gráfico guardado en /tmp/U01_portafolio.png]")


# ============================================================
# Ejercicio 4: Sharpe Ratio
# ============================================================
print("\\n=== Ejercicio 4: Sharpe Ratio ===")
rendimientos_diarios = [0.0012, -0.0005, 0.0021, -0.0008, 0.0015,
                         0.0003, -0.0012, 0.0028, -0.0004, 0.0009,
                         0.0018, -0.0015, 0.0007, 0.0025, -0.0003,
                         0.0014, -0.0010, 0.0006, 0.0020, -0.0008]
tasa_libre_riesgo = 0.04

n_dias = len(rendimientos_diarios)
promedio_diario = sum(rendimientos_diarios) / n_dias

suma_cuadrados = sum((r - promedio_diario) ** 2 for r in rendimientos_diarios)
vol_diaria = (suma_cuadrados / (n_dias - 1)) ** 0.5

retorno_anual = promedio_diario * 252
vol_anual = vol_diaria * (252 ** 0.5)
sharpe = (retorno_anual - tasa_libre_riesgo) / vol_anual

print(f"Días: {n_dias}")
print(f"Retorno promedio diario: {promedio_diario:.4f}")
print(f"Volatilidad diaria: {vol_diaria:.4f}")
print(f"Retorno anualizado: {retorno_anual:.2%}")
print(f"Volatilidad anualizada: {vol_anual:.2%}")
print(f"Sharpe Ratio: {sharpe:.2f}")
```

---

> [📥 Descargar archivo .py](U01_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 0](index.md)
