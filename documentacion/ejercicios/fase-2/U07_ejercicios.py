# U07: EJERCICIOS — Listas y Tuplas: Series de Precios y Registros Financieros

# ============================================================
# Ejercicio 1: Rastreador de portafolio
# Dada una lista de (ticker, cantidad, precio_compra) y un dict de
# precios_actuales, calcula el P&L de cada posición y el total.
# ============================================================
print("=== Ejercicio 1: Rastreador de Portafolio ===")
portafolio = [
    ("AAPL", 10, 150.00),
    ("MSFT", 5, 280.00),
    ("TSLA", 3, 900.00),
    ("JPM", 20, 135.00),
]
precios_actuales = {"AAPL": 175.00, "MSFT": 310.00, "TSLA": 820.00, "JPM": 142.00}

# Escribe tu código aquí



# Output esperado:
# AAPL: 10 × $150.00 → Actual: $175.00 | P&L: +$250.00 (+16.67%)
# MSFT: 5 × $280.00 → Actual: $310.00 | P&L: +$150.00 (+10.71%)
# TSLA: 3 × $900.00 → Actual: $820.00 | P&L: -$240.00 (-8.89%)
# JPM: 20 × $135.00 → Actual: $142.00 | P&L: +$140.00 (+5.19%)
# P&L Total: +$300.00


# ============================================================
# Ejercicio 2: Filtro de oportunidades (list comprehension)
# Dada una lista de (ticker, PER, crecimiento %), filtra las que:
#   - PER < 15
#   - Crecimiento > 10%
# Usa list comprehension.
# ============================================================
print("\n=== Ejercicio 2: Filtro de Oportunidades ===")
acciones = [
    ("AAPL", 28, 8),
    ("XOM", 10, 15),
    ("JPM", 9, 12),
    ("TSLA", 65, 25),
    ("CVX", 11, 18),
    ("PFE", 14, 5),
]

# Escribe tu código aquí



# Output esperado:
# Oportunidades (PER<15, Crec>10%): [('XOM', 10, 15), ('JPM', 9, 12), ('CVX', 11, 18)]


# ============================================================
# Ejercicio 3: Media móvil con slicing
# Calcula la SMA de 5 días para la siguiente serie de precios.
# Usa slicing (lista[i:i+5]) para obtener cada ventana.
# ============================================================
print("\n=== Ejercicio 3: SMA 5 con Slicing ===")
precios = [100, 102, 101, 105, 103, 108, 110, 107, 112, 115, 113, 118]

# Escribe tu código aquí



# Output esperado:
# SMA(5) día 5: 102.20
# SMA(5) día 6: 103.80
# SMA(5) día 7: 105.40
# SMA(5) día 8: 106.60
# SMA(5) día 9: 108.00
# SMA(5) día 10: 110.40
# SMA(5) día 11: 111.40
# SMA(5) día 12: 113.00


# ============================================================
# Ejercicio 4: Estadísticas financieras (sin librerías externas)
# Usa SOLO listas y operaciones básicas para calcular:
# - Media de retornos
# - Varianza (poblacional: divide entre n-1)
# - Desviación estándar (sqrt de varianza)
# - Max drawdown (máxima caída desde un pico)
# Datos: serie de precios de cierre diarios
# ============================================================
print("\n=== Ejercicio 4: Estadísticas Financieras ===")
precios_cierre = [100, 102, 105, 98, 103, 108, 95, 102, 110, 105, 99, 106]

# Escribe tu código aquí



# Output esperado:
# Retornos diarios calculados
# Media de retornos: X.XX%
# Volatilidad diaria: X.XX%
# Volatilidad anualizada (×√252): XX.XX%
# Max Drawdown: XX.XX%
