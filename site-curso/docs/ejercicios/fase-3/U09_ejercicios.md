# 📝 Ejercicios: U09 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U09_ejercicios)

---

```python
# U09: EJERCICIOS — Bucles for Anidados

# ============================================================
# Ejercicio 1: Matriz de rendimientos
# Crea una matriz 3x5 de rendimientos. Encuentra el peor y mejor rendimiento
# y si posición (activo, día). Usa enumerate para obtener índices.
# ============================================================
print("=== Ejercicio 1: Peor y Mejor Rendimiento ===")
rendimientos = [
    [1.5, -0.8, 2.1, -3.2, 0.5],
    [0.3, 1.8, -1.1, 2.5, -0.4],
    [-2.1, 0.9, 1.2, -0.7, 3.1],
]
activos = ["A", "B", "C"]

# Escribe tu código aquí



# Output esperado:
# Peor rendimiento: -3.20% en Activo A, Día 4
# Mejor rendimiento: 3.10% en Activo C, Día 5


# ============================================================
# Ejercicio 2: Tabla de costo de préstamo
# Muestra el costo total (capital + interés) para un préstamo de $10,000
# a diferentes tasas (4% a 12% en pasos de 2) y plazos (1 a 5 años)
# Fórmula: interés simple → total = capital * (1 + tasa/100 * anios)
# ============================================================
print("\\n=== Ejercicio 2: Costo de Préstamo ===")
capital = 10000
tasas = range(4, 13, 2)
plazos = range(1, 6)

# Escribe tu código aquí



# Output esperado (primeras líneas):
# Años      4%      6%      8%     10%     12%
# 1    10,400  10,600  10,800  11,000  11,200
# 2    10,800  11,200  11,600  12,000  12,400
# ...


# ============================================================
# Ejercicio 3: Producto de matrices
# Multiplica una matriz A (2×3) por B (3×2)
# A = [[1, 2, 3], [4, 5, 6]]
# B = [[7, 8], [9, 10], [11, 12]]
# C debe ser 2×2
# ============================================================
print("\\n=== Ejercicio 3: Producto de Matrices ===")
A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]

# Escribe tu código aquí



# Output esperado:
# C[0][0] = 58 | C[0][1] = 64
# C[1][0] = 139 | C[1][1] = 154


# ============================================================
# Ejercicio 4: Optimización de grilla (3 activos)
# 3 activos: A (ret=12%, vol=18%), B (ret=8%, vol=10%), C (ret=6%, vol=5%)
# Correlación: AB=0.3, AC=0.1, BC=0.4 | Tasa libre: 4%
# Encuentra la combinación que maximiza Sharpe con pasos de 20%
# (wA + wB + wC = 100%)
# ============================================================
print("\\n=== Ejercicio 4: Optimización de Portafolio (Grilla) ===")
ret = [12, 8, 6]
vol = [18, 10, 5]
corr = [[1.0, 0.3, 0.1],
        [0.3, 1.0, 0.4],
        [0.1, 0.4, 1.0]]
rf = 4

# Escribe tu código aquí



# Output esperado:
# Mejor combinación: A=60% B=0% C=40%
# Rendimiento: 9.60% | Riesgo: 11.47% | Sharpe: 0.49
```

---

> [📥 Descargar archivo .py](U09_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
