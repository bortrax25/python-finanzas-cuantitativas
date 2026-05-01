# ✅ Soluciones: U09 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U09_soluciones)

---

```python
# U09: SOLUCIONES — Bucles for Anidados

# ============================================================
# Ejercicio 1: Peor y Mejor Rendimiento
# ============================================================
print("=== Ejercicio 1: Peor y Mejor Rendimiento ===")
rendimientos = [
    [1.5, -0.8, 2.1, -3.2, 0.5],
    [0.3, 1.8, -1.1, 2.5, -0.4],
    [-2.1, 0.9, 1.2, -0.7, 3.1],
]
activos = ["A", "B", "C"]

peor_valor = float("inf")
mejor_valor = float("-inf")

for i, fila in enumerate(rendimientos):
    for j, valor in enumerate(fila):
        if valor < peor_valor:
            peor_valor = valor
            peor_pos = (i, j)
        if valor > mejor_valor:
            mejor_valor = valor
            mejor_pos = (i, j)

print(f"Peor rendimiento: {peor_valor:.2f}% en Activo {activos[peor_pos[0]]}, Día {peor_pos[1]+1}")
print(f"Mejor rendimiento: {mejor_valor:.2f}% en Activo {activos[mejor_pos[0]]}, Día {mejor_pos[1]+1}")


# ============================================================
# Ejercicio 2: Costo de Préstamo
# ============================================================
print("\\n=== Ejercicio 2: Costo de Préstamo ===")
capital = 10000
tasas = range(4, 13, 2)
plazos = range(1, 6)

print(f"{'Años':<6}", end="")
for tasa in tasas:
    print(f"{tasa}%".rjust(8), end="")
print()

for anios in plazos:
    print(f"{anios:<6}", end="")
    for tasa in tasas:
        total = capital * (1 + tasa / 100 * anios)
        print(f"${total:>7,.0f}", end="")
    print()


# ============================================================
# Ejercicio 3: Producto de Matrices
# ============================================================
print("\\n=== Ejercicio 3: Producto de Matrices ===")
A = [[1, 2, 3], [4, 5, 6]]
B = [[7, 8], [9, 10], [11, 12]]

# C = A(2×3) × B(3×2) = C(2×2)
filas_A, cols_A = len(A), len(A[0])
filas_B, cols_B = len(B), len(B[0])
C = [[0] * cols_B for _ in range(filas_A)]

for i in range(filas_A):
    for j in range(cols_B):
        for k in range(cols_A):
            C[i][j] += A[i][k] * B[k][j]

print(f"C[0][0] = {C[0][0]} | C[0][1] = {C[0][1]}")
print(f"C[1][0] = {C[1][0]} | C[1][1] = {C[1][1]}")


# ============================================================
# Ejercicio 4: Optimización de Portafolio (Grilla)
# ============================================================
print("\\n=== Ejercicio 4: Optimización de Portafolio (Grilla) ===")
ret = [12, 8, 6]
vol = [18, 10, 5]
corr = [[1.0, 0.3, 0.1],
        [0.3, 1.0, 0.4],
        [0.1, 0.4, 1.0]]
rf = 4

mejor_sharpe = -float("inf")
mejor_w = None
paso = 20

for w1 in range(0, 101, paso):
    for w2 in range(0, 101 - w1, paso):
        w3 = 100 - w1 - w2
        if w3 < 0 or (w1 + w2 + w3) != 100:
            continue

        wa = w1 / 100
        wb = w2 / 100
        wc = w3 / 100

        rp = wa * ret[0] + wb * ret[1] + wc * ret[2]
        var = (wa * vol[0]) ** 2 + (wb * vol[1]) ** 2 + (wc * vol[2]) ** 2
        var += 2 * wa * wb * corr[0][1] * vol[0] * vol[1]
        var += 2 * wa * wc * corr[0][2] * vol[0] * vol[2]
        var += 2 * wb * wc * corr[1][2] * vol[1] * vol[2]
        riesgo = var ** 0.5
        sharpe = (rp - rf) / riesgo

        if sharpe > mejor_sharpe:
            mejor_sharpe = sharpe
            mejor_w = (w1, w2, w3)
            mejor_rp = rp
            mejor_riesgo = riesgo

print(f"Mejor combinación: A={mejor_w[0]}% B={mejor_w[1]}% C={mejor_w[2]}%")
print(f"Rendimiento: {mejor_rp:.2f}% | Riesgo: {mejor_riesgo:.2f}% | Sharpe: {mejor_sharpe:.2f}")
```

---

> [📥 Descargar archivo .py](U09_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
