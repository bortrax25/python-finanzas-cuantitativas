# 📝 Ejercicios: U11 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U11_ejercicios)

---

```python
# U11: EJERCICIOS — Funciones: Construyendo tu Librería Financiera

# ============================================================
# Ejercicio 1: Función payback
# Implementa payback(inversion, flujos) que retorne el número de años
# para recuperar la inversión inicial. Si no se recupera, retorna None.
# Incluye type hints y docstring.
# ============================================================
print("=== Ejercicio 1: Payback ===")

# Escribe tu función aquí



print(f"Payback: {payback(50000, [12000, 15000, 18000, 20000, 22000])} años")
print(f"Payback: {payback(10000, [2000, 3000, 4000])} años")

# Output esperado:
# Payback: 4 años
# Payback: None años


# ============================================================
# Ejercicio 2: Función VPN con type hints
# Implementa vpn(inversion, tasa, flujos) con type hints y docstring NumPy.
# VPN = sum(flujo / (1+tasa)^t) - inversion
# ============================================================
print("\\n=== Ejercicio 2: VPN ===")

# Escribe tu función aquí



resultado = vpn(10000, 0.10, [3000, 4000, 5000, 6000])
print(f"VPN: ${resultado:,.2f}")

# Output esperado:
# VPN: $3,597.36


# ============================================================
# Ejercicio 3: Estadísticas con *args
# Implementa estadisticas(*rendimientos) que retorne una tupla (promedio, max, min).
# Si no hay rendimientos, retorna (0.0, 0.0, 0.0).
# ============================================================
print("\\n=== Ejercicio 3: Estadísticas con *args ===")

# Escribe tu función aquí



prom, mx, mn = estadisticas(5.2, -2.1, 3.8, -0.5, 4.2, 1.7)
print(f"Promedio: {prom:.2f}% | Max: {mx:.2f}% | Min: {mn:.2f}%")

# Output esperado:
# Promedio: 2.05% | Max: 5.20% | Min: -2.10%


# ============================================================
# Ejercicio 4: Funciones CAGR y volatilidad
# Implementa dos funciones con type hints y docstrings:
# cagr(vi, vf, anios) → retorna CAGR en %
# volatilidad_anualizada(rendimientos_diarios) → volatilidad anualizada en %
# Volatilidad diaria = std(rendimientos) * sqrt(252)
# ============================================================
print("\\n=== Ejercicio 4: CAGR y Volatilidad ===")

# Escribe tus funciones aquí



c = cagr(5000, 12000, 8)
print(f"CAGR: {c:.2f}%")

rendimientos = [0.5, -0.2, 1.8, -0.7, 0.3, 1.2, -0.4, 0.8]
vol = volatilidad_anualizada(rendimientos)
print(f"Volatilidad anualizada: {vol:.2f}%")

# Output esperado:
# CAGR: 11.57%
# Volatilidad anualizada: 14.52%
```

---

> [📥 Descargar archivo .py](U11_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
