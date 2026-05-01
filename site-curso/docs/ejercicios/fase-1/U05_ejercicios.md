# 📝 Ejercicios: U05 — Fase 1

> [← Volver a ejercicios Fase 1](index.md) | [📥 Descargar .py](U05_ejercicios)

---

```python
# U05: EJERCICIOS — Condicionales: Reglas de Negocio y Señales de Trading

# ============================================================
# Ejercicio 1: Calculadora de impuesto a la renta
# Tramos progresivos:
# Hasta $10,000 → 10%
# De $10,001 a $50,000 → 15%
# De $50,001 a $100,000 → 20%
# Más de $100,000 → 25%
# Muestra el impuesto y la tasa efectiva.
# ============================================================
print("=== Ejercicio 1: Impuesto a la Renta ===")
ingreso_anual = 75000

# Escribe tu código aquí



# Output esperado:
# Ingreso anual: $75,000.00
# Impuesto a pagar: $11,250.00
# Tasa efectiva: 15.00%


# ============================================================
# Ejercicio 2: Clasificador de score crediticio
# Clasifica según score:
#   750+ → "Excelente (AAA)"
#   650-749 → "Bueno (BBB)"
#   550-649 → "Regular (CCC)"
#   < 550 → "Malo (D)"
# Usa match/case con guardas donde aplique.
# ============================================================
print("\\n=== Ejercicio 2: Score Crediticio ===")
score = 720

# Escribe tu código aquí



# Output esperado:
# Score: 720 → Clasificación: Bueno (BBB)


# ============================================================
# Ejercicio 3: Señal de medias móviles (Golden Cross / Death Cross)
# Dados precio_actual, media_corta (MA20) y media_larga (MA50):
#   MA20 > MA50 → "COMPRA (Golden Cross)"
#   MA20 < MA50 → "VENTA (Death Cross)"
#   igual → "INDEFINIDO"
# Clasifica tendencia:
#   precio > MA20 y MA50 → "ALCISTA"
#   precio < MA20 y MA50 → "BAJISTA"
#   otro → "LATERAL"
# ============================================================
print("\\n=== Ejercicio 3: Señal de Trading ===")
precio_actual = 155.00
media_corta = 152.00
media_larga = 148.00

# Escribe tu código aquí



# Output esperado:
# Precio: $155.00 | MA20: $152.00 | MA50: $148.00
# Señal: COMPRA (Golden Cross)
# Tendencia: ALCISTA


# ============================================================
# Ejercicio 4: Sistema de alertas de portafolio
# Dada una lista de (ticker, peso%, cambio%):
#   Si cae más de 5% Y peso > 20% → "ALERTA ROJA"
#   Si solo cae más de 5% → "ALERTA AMARILLA"
#   Otro → "NORMAL"
# Usa condicionales anidados con and/or.
# ============================================================
print("\\n=== Ejercicio 4: Alertas de Portafolio ===")
acciones = [
    ("AAPL", 30, -6.5),
    ("MSFT", 25, -3.2),
    ("TSLA", 15, -8.0),
    ("JPM", 20, 1.5),
    ("VIX", 10, 15.0),
]

# Escribe tu código aquí



# Output esperado:
# AAPL: -6.5% (peso 30%) → ALERTA ROJA
# MSFT: -3.2% (peso 25%) → NORMAL
# TSLA: -8.0% (peso 15%) → ALERTA AMARILLA
# JPM: 1.5% (peso 20%) → NORMAL
# VIX: 15.0% (peso 10%) → NORMAL
```

---

> [📥 Descargar archivo .py](U05_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 1](index.md)
