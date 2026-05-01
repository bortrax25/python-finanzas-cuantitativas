# 📝 Ejercicios: U07 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U07_ejercicios)

---

```python
# U07: EJERCICIOS — Bucle for y range()

# ============================================================
# Ejercicio 1: Promedio móvil simple (SMA)
# Calcula el promedio móvil de 3 días para precios dados
# SMA[2] = (p[0] + p[1] + p[2]) / 3
# ============================================================
print("=== Ejercicio 1: Media Móvil (SMA 3) ===")
precios = [100, 102, 101, 105, 103, 108, 110, 107]

# Escribe tu código aquí



# Output esperado:
# Día 3: 101.00 | Día 4: 102.67 | Día 5: 103.00
# Día 6: 105.33 | Día 7: 107.00 | Día 8: 108.33


# ============================================================
# Ejercicio 2: Máximo drawdown
# Encuentra la máxima caída desde un pico
# drawdown = (pico - precio_actual) / pico * 100
# ============================================================
print("\\n=== Ejercicio 2: Máximo Drawdown ===")
precios = [100, 105, 95, 90, 98, 92, 88, 96]

# Escribe tu código aquí



# Output esperado:
# Máximo drawdown: 16.19%


# ============================================================
# Ejercicio 3: Tabla de tasas
# Muestra cuánto crece $1 a diferentes tasas (5%, 10%, 15%) en 1-10 años
# ============================================================
print("\\n=== Ejercicio 3: Crecimiento de $1 ===")
tasas = [5, 10, 15]
anios = range(1, 11)

# Escribe tu código aquí



# Output esperado (primeras líneas):
# Año    5%    10%    15%
# 1    1.05   1.10   1.15
# 2    1.10   1.21   1.32


# ============================================================
# Ejercicio 4: Clasificador de velas
# Dado pares (apertura, cierre), clasifica cada día:
#   cierre > apertura → "VELA VERDE  "
#   cierre < apertura → "VELA ROJA   "
#   igual           → "DOJI        "
# Cuenta cuántas de cada tipo
# ============================================================
print("\\n=== Ejercicio 4: Clasificador de Velas ===")
datos = [
    (100, 105),
    (105, 102),
    (102, 108),
    (108, 106),
    (106, 110),
    (110, 110),
    (110, 107),
    (107, 103),
]

# Escribe tu código aquí



# Output esperado:
# Día 1: Abre $100 | Cierra $105 → VELA VERDE
# ...
# Verdes: 3 | Rojas: 4 | Doji: 1
```

---

> [📥 Descargar archivo .py](U07_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
