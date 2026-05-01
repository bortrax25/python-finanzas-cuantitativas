# ✅ Soluciones: U13 — Fase 5

> [← Volver a ejercicios Fase 5](index.md) | [📥 Descargar .py](U13_U15_soluciones)

---

```python
# U13-U15: SOLUCIONES

# ============================================================
# U13 - Ejercicio 1: Payback
# ============================================================
print("=== U13: Payback ===")

def payback(inversion, flujos):
    acumulado = 0
    for i, flujo in enumerate(flujos):
        acumulado += flujo
        if acumulado >= inversion:
            return i + 1
    return None

print(payback(50000, [12000, 15000, 18000, 20000, 22000]))


# ============================================================
# U13 - Ejercicio 2: VPN
# ============================================================
print("\\n=== U13: VPN ===")

def vpn(inversion, tasa, flujos):
    valor_presente = 0
    for t, flujo in enumerate(flujos, start=1):
        valor_presente += flujo / (1 + tasa) ** t
    return valor_presente - inversion

print(f"${vpn(10000, 0.10, [3000, 4000, 5000, 6000]):,.2f}")


# ============================================================
# U14 - Ejercicio 1: Estadísticas con *args
# ============================================================
print("\\n=== U14: Estadísticas con *args ===")

def estadisticas(*rendimientos):
    if not rendimientos:
        return (0, 0, 0)
    return (sum(rendimientos) / len(rendimientos), max(rendimientos), min(rendimientos))

print(estadisticas(5.2, -2.1, 3.8, -0.5, 4.2))


# ============================================================
# U14 - Ejercicio 2: Ordenar con lambda
# ============================================================
print("\\n=== U14: Ordenar con lambda ===")
acciones = [("AAPL", 28, 8), ("XOM", 10, 15), ("JPM", 9, 12), ("TSLA", 65, 25)]

por_per = sorted(acciones, key=lambda x: x[1])
por_crec = sorted(acciones, key=lambda x: x[2], reverse=True)

print(f"Por PER: {por_per}")
print(f"Por Crecimiento: {por_crec}")


# ============================================================
# U15 - Ejercicio: Edad de inversión
# ============================================================
print("\\n=== U15: Edad de inversión ===")
from datetime import date

def edad_inversion(anio, mes, dia):
    inicio = date(anio, mes, dia)
    hoy = date.today()
    return (hoy - inicio).days // 365

print(f"Años transcurridos: {edad_inversion(2020, 1, 15)}")
```

---

> [📥 Descargar archivo .py](U13_U15_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 5](index.md)
