# 📝 Ejercicios: U21 — Fase 5

> [← Volver a ejercicios Fase 5](index.md) | [📥 Descargar .py](U21_ejercicios)

---

```python
# U21: EJERCICIOS — Pandas Avanzado: Análisis Técnico

import pandas as pd
import numpy as np

# ============================================================
# Ejercicio 1: SMA, EMA y Golden/Death Cross
# Crea una serie de 252 precios simulados (empieza en 100, seed=42, μ=0.0005, σ=0.015).
# Calcula:
#   - SMA_20 y SMA_50
#   - EMA_12 y EMA_26 (con adjust=False)
#   - Golden Cross: días donde SMA_20 cruza POR ENCIMA de SMA_50
#   - Death Cross: días donde SMA_20 cruza POR DEBAJO de SMA_50
#     (usa shift(1) para comparar con el día anterior)
# Muestra los primeros 3 cruces de cada tipo (fecha y precios).
# ============================================================
print("=== Ejercicio 1: Cruces de medias móviles ===")

# Escribe tu código aquí



# Output esperado:
# Golden Crosses detectados: X
#   2024-XX-XX: SMA_20 cruzó sobre SMA_50 (precio=$1XX.XX)
#   ...
# Death Crosses detectados: X
#   2024-XX-XX: SMA_20 cruzó bajo SMA_50 (precio=$1XX.XX)
#   ...


# ============================================================
# Ejercicio 2: Bollinger Bands con señales de ruptura
# Usando la misma serie de precios:
#   - Calcula Bollinger Bands (20, 2): SMA_20, Banda Superior, Banda Inferior
#   - Calcula %B = (precio - banda_inferior) / (banda_superior - banda_inferior)
#   - Detecta rupturas alcistas: precio > banda_superior (primer día que cruza hacia arriba)
#   - Detecta rupturas bajistas: precio < banda_inferior (primer día que cruza hacia abajo)
#   - Calcula cuántas veces el precio "revierte" después de una ruptura
#     (vuelve dentro de las bandas en los siguientes 5 días)
# Muestra las primeras 3 rupturas de cada tipo.
# ============================================================
print("\\n=== Ejercicio 2: Bollinger Bands ===")

# Escribe tu código aquí



# Output esperado:
# Rupturas alcistas detectadas: X
#   2024-XX-XX: Precio=$1XX.XX | Banda Sup=$1XX.XX | %B=X.XX
# Rupturas bajistas detectadas: X
#   2024-XX-XX: Precio=$1XX.XX | Banda Inf=$1XX.XX | %B=X.XX
# Reversiones post-ruptura alcista: X/Y (XX.X%)
# Reversiones post-ruptura bajista: X/Y (XX.X%)


# ============================================================
# Ejercicio 3: RSI con detección de sobrecompra/sobreventa
# Usando la misma serie de precios:
#   - Calcula RSI(14) usando el método de Wilder (EWM con alpha=1/14)
#   - Detecta zonas de sobrecompra (RSI >= 70) y sobreventa (RSI <= 30)
#   - Para cada día en sobrecompra, indica cuántos días consecutivos lleva
#   - Para cada día en sobreventa, indica cuántos días consecutivos lleva
#   - Muestra:
#       * Cuántos días totales en sobrecompra y sobreventa
#       * La racha más larga de sobrecompra (fecha inicio, duración)
#       * La racha más larga de sobreventa (fecha inicio, duración)
# ============================================================
print("\\n=== Ejercicio 3: RSI y zonas extremas ===")

# Escribe tu código aquí



# Output esperado:
# Días en sobrecompra (RSI>=70): XX (XX.X%)
# Días en sobreventa (RSI<=30): XX (XX.X%)
# Racha más larga sobrecompra: X días desde 2024-XX-XX
# Racha más larga sobreventa: X días desde 2024-XX-XX


# ============================================================
# Ejercicio 4: MACD con estrategia de cruce y P&L simulado
# Usando la misma serie de precios:
#   - Calcula MACD: EMA_12 - EMA_26
#   - Calcula línea de señal: EMA_9 del MACD
#   - Calcula histograma: MACD - señal
#   - Detecta cruces: cuando MACD cruza la línea de señal
#     (cruce_alcista: MACD pasa de debajo a arriba)
#     (cruce_bajista: MACD pasa de arriba a abajo)
#   - Simula estrategia simple:
#       * Comprar en cada cruce alcista
#       * Vender en cada cruce bajista
#       * Capital inicial: $10,000
#       * Siempre invertir todo el capital (compra/vende al precio de cierre del día del cruce)
#   - Calcula: número de trades, P&L final, retorno total %, win rate
# Muestra un resumen de la estrategia.
# ============================================================
print("\\n=== Ejercicio 4: Estrategia MACD ===")

# Escribe tu código aquí



# Output esperado:
# Cruces alcistas del MACD: XX
# Cruces bajistas del MACD: XX
# Estrategia MACD:
#   Trades totales: XX
#   Capital inicial: $10,000.00
#   Capital final: $1X,XXX.XX
#   Retorno total: XX.XX%
#   Win rate: XX.X%
#   Mejor trade: +$XXX.XX
#   Peor trade: -$XXX.XX
```

---

> [📥 Descargar archivo .py](U21_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 5](index.md)
