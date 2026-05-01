# 📝 Ejercicios: U03 — Fase 1

> [← Volver a ejercicios Fase 1](index.md) | [📥 Descargar .py](U03_ejercicios)

---

```python
# U03: EJERCICIOS — Operadores: La Aritmética de Wall Street

# ============================================================
# Ejercicio 1: Precio promedio ponderado
# Tienes 3 compras de una acción a diferentes precios y cantidades.
# Calcula el precio promedio ponderado.
# PAPP = (P1*C1 + P2*C2 + P3*C3) / (C1 + C2 + C3)
# ============================================================
print("=== Ejercicio 1: Precio Promedio Ponderado ===")
cantidad1, precio1 = 100, 152.50
cantidad2, precio2 = 50, 148.00
cantidad3, precio3 = 75, 155.00

# Escribe tu código aquí



# Output esperado:
# Total invertido: $37,340.00
# Total acciones: 225
# Precio promedio: $165.96


# ============================================================
# Ejercicio 2: Verificador de stop-loss
# Dado un precio de entrada y un porcentaje de stop-loss,
# verifica si el precio actual activó el stop-loss.
# Regla: stop_loss activado si precio_actual <= precio_entrada * (1 - stop_loss/100)
# ============================================================
print("\\n=== Ejercicio 2: Stop-Loss ===")
precio_entrada = 200.00
stop_loss_pct = 7
precio_actual = 184.00

# Escribe tu código aquí



# Output esperado:
# Precio de entrada: $200.00
# Stop-loss: $186.00 (7.0%)
# Precio actual: $184.00
# ¿Stop-loss activado? True


# ============================================================
# Ejercicio 3: CAGR (Tasa de Crecimiento Anual Compuesta)
# CAGR = (VF / VI) ** (1/n) - 1
# ============================================================
print("\\n=== Ejercicio 3: CAGR ===")
valor_inicial = 5000
valor_final = 12000
anios = 8

# Escribe tu código aquí



# Output esperado:
# Valor inicial: $5,000.00
# Valor final: $12,000.00
# Período: 8 años
# CAGR: 11.57%


# ============================================================
# Ejercicio 4: Cuota de hipoteca (sistema francés)
# Cuota fija = M * (i * (1+i)^n) / ((1+i)^n - 1)
# donde M = monto, i = tasa mensual, n = número de cuotas
# ============================================================
print("\\n=== Ejercicio 4: Cuota de Hipoteca ===")
monto = 200000
tasa_anual = 10
plazo_anios = 20

# Escribe tu código aquí



# Output esperado:
# Monto: $200,000.00
# Tasa anual: 10%
# Plazo: 20 años (240 meses)
# Cuota mensual: $1,930.07
# Total a pagar: $463,217.60
# Interés total: $263,217.60
```

---

> [📥 Descargar archivo .py](U03_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 1](index.md)
