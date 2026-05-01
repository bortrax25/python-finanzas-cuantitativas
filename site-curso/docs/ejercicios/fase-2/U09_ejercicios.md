# 📝 Ejercicios: U09 — Fase 2

> [← Volver a ejercicios Fase 2](index.md) | [📥 Descargar .py](U09_ejercicios)

---

```python
# U09: EJERCICIOS — Conjuntos y Strings Avanzados para Datos Financieros

# ============================================================
# Ejercicio 1: Parser de noticias financieras
# Extrae todos los tickers mencionados (entre paréntesis, 1-5 mayúsculas).
# Clasifica sentimiento con palabras clave:
#   Positivas: subió, subieron, ganancia, compra, repunte
#   Negativas: cayó, cayeron, pérdida, venta, desplome
# Cuenta menciones positivas y negativas por ticker.
# ============================================================
print("=== Ejercicio 1: Parser de Noticias ===")
import re

noticia = """
El mercado cerró mixto. Apple (AAPL) subió 2.1% tras buenos resultados.
Microsoft (MSFT) también registró ganancia de 1.5%. Tesla (TSLA) cayó
3.2% por preocupaciones de demanda. JP Morgan (JPM) reportó compra
institucional. Amazon (AMZN) tuvo un leve repunte de 0.8%.
Por otro lado, Meta (META) se desplomó 5.1% y Tesla (TSLA) sumó
otra pérdida de 1.3% en after-hours.
"""

palabras_positivas = ["subió", "subieron", "ganancia", "compra", "repunte"]
palabras_negativas = ["cayó", "cayeron", "pérdida", "venta", "desplome", "desplomó"]

# Escribe tu código aquí



# Output esperado:
# Tickers encontrados: {'AAPL', 'MSFT', 'TSLA', 'JPM', 'AMZN', 'META'}
# AAPL: +1 (positivo)
# MSFT: +1 (positivo)
# TSLA: -2 (negativo)
# JPM: +1 (positivo)
# AMZN: +1 (positivo)
# META: -1 (negativo)


# ============================================================
# Ejercicio 2: Validador de ISIN con regex
# Valida una lista de ISINs. Un ISIN válido tiene el formato:
# 2 letras de país + 10 caracteres alfanuméricos (total 12)
# Separa en listas de válidos e inválidos.
# ============================================================
print("\\n=== Ejercicio 2: Validador de ISIN ===")

isins = [
    "US0378331005",    # Apple — válido
    "US5949181045",    # Microsoft — válido
    "DE000BAY0017",    # Bayer — válido
    "INVALID1234",     # empieza con número
    "US037833100",     # muy corto
    "JP3435000009",    # Sony — válido
    "U12345",           # muy corto
]

# Escribe tu código aquí



# Output esperado:
# Válidos (4): ['US0378331005', 'US5949181045', 'DE000BAY0017', 'JP3435000009']
# Inválidos (3): ['INVALID1234', 'US037833100', 'U12345']


# ============================================================
# Ejercicio 3: Intersección de universos (screening multi-factor)
# Dados 3 screenings:
#   - valor: tickers con PER bajo (< 15)
#   - crecimiento: tickers con crecimiento > 10%
#   - calidad: tickers con ROE > 20%
# Encuentra:
#   a) Acciones que cumplen los 3 criterios
#   b) Acciones que cumplen al menos 2 de 3 criterios
# ============================================================
print("\\n=== Ejercicio 3: Screening Multi-Factor ===")
valor = {"XOM", "JPM", "CVX", "PFE", "VZ", "T", "BAC"}
crecimiento = {"AAPL", "JPM", "NVDA", "CVX", "MSFT", "GOOGL"}
calidad = {"AAPL", "MSFT", "JPM", "V", "MA", "NVDA"}
from collections import Counter

# Escribe tu código aquí



# Output esperado:
# Cumplen los 3 criterios: {'JPM'}
# Cumplen al menos 2 criterios: ['JPM', 'AAPL', 'NVDA', 'CVX', 'MSFT', 'VZ']


# ============================================================
# Ejercicio 4: Extracción de precios de un texto financiero
# De un análisis de mercado, extrae:
# - Todos los precios en formato $XXX.XX
# - Calcula el promedio de esos precios
# - Todos los porcentajes en formato XX.X% o -XX.X%
# ============================================================
print("\\n=== Ejercicio 4: Extracción de Precios ===")

texto = """
Resumen de cierre: AAPL cerró a $175.50 (+2.1%), MSFT a $310.25 (-0.5%),
TSLA a $820.00 (-3.2%), JPM a $142.80 (+1.8%), AMZN a $178.25 (+0.9%).
El S&P 500 subió 1.3% en la sesión. Los bonos del Tesoro rindieron 4.25%.
El oro cotizó a $2,150.30 la onza. El petróleo WTI bajó -2.5% a $78.50.
"""

# Escribe tu código aquí



# Output esperado:
# Precios: ['175.50', '310.25', '820.00', '142.80', '178.25', ...]
# Promedio de precios: $XXX.XX
# Porcentajes: ['2.1%', '-0.5%', '-3.2%', '1.8%', '0.9%', '1.3%', '4.25%', '-2.5%']
```

---

> [📥 Descargar archivo .py](U09_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 2](index.md)
