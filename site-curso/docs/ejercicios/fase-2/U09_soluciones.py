# U09: SOLUCIONES — Conjuntos y Strings Avanzados para Datos Financieros

# ============================================================
# Ejercicio 1: Parser de Noticias
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

tickers = set(re.findall(r"\(([A-Z]{1,5})\)", noticia))
print(f"Tickers encontrados: {tickers}")

sentimiento = {}
for ticker in tickers:
    puntaje = 0
    for palabra in palabras_positivas:
        puntaje += len(re.findall(rf"{ticker}[^.]*{palabra}|{palabra}[^.]*{ticker}", noticia))
    for palabra in palabras_negativas:
        puntaje -= len(re.findall(rf"{ticker}[^.]*{palabra}|{palabra}[^.]*{ticker}", noticia))
    
    estado = "positivo" if puntaje > 0 else ("negativo" if puntaje < 0 else "neutral")
    sentimiento[ticker] = puntaje
    print(f"{ticker}: {puntaje:+d} ({estado})")


# ============================================================
# Ejercicio 2: Validador de ISIN
# ============================================================
print("\n=== Ejercicio 2: Validador de ISIN ===")

isins = [
    "US0378331005",
    "US5949181045",
    "DE000BAY0017",
    "INVALID1234",
    "US037833100",
    "JP3435000009",
    "U12345",
]

patron_isin = r"^[A-Z]{2}[A-Z0-9]{10}$"

validos = [i for i in isins if re.match(patron_isin, i)]
invalidos = [i for i in isins if not re.match(patron_isin, i)]

print(f"Válidos ({len(validos)}): {validos}")
print(f"Inválidos ({len(invalidos)}): {invalidos}")


# ============================================================
# Ejercicio 3: Screening Multi-Factor
# ============================================================
print("\n=== Ejercicio 3: Screening Multi-Factor ===")
valor = {"XOM", "JPM", "CVX", "PFE", "VZ", "T", "BAC"}
crecimiento = {"AAPL", "JPM", "NVDA", "CVX", "MSFT", "GOOGL"}
calidad = {"AAPL", "MSFT", "JPM", "V", "MA", "NVDA"}
from collections import Counter

cumplen_3 = valor & crecimiento & calidad
print(f"Cumplen los 3 criterios: {cumplen_3}")

todas = list(valor) + list(crecimiento) + list(calidad)
cumplen_2 = [t for t, c in Counter(todas).items() if c >= 2]
print(f"Cumplen al menos 2 criterios: {cumplen_2}")


# ============================================================
# Ejercicio 4: Extracción de Precios
# ============================================================
print("\n=== Ejercicio 4: Extracción de Precios ===")

texto = """
Resumen de cierre: AAPL cerró a $175.50 (+2.1%), MSFT a $310.25 (-0.5%),
TSLA a $820.00 (-3.2%), JPM a $142.80 (+1.8%), AMZN a $178.25 (+0.9%).
El S&P 500 subió 1.3% en la sesión. Los bonos del Tesoro rindieron 4.25%.
El oro cotizó a $2,150.30 la onza. El petróleo WTI bajó -2.5% a $78.50.
"""

precios = re.findall(r"\$(\d+\.\d{2})", texto)
precios_float = [float(p) for p in precios]
promedio = sum(precios_float) / len(precios_float) if precios_float else 0

print(f"Precios: {precios}")
print(f"Promedio de precios: ${promedio:.2f}")

porcentajes = re.findall(r"[-+]?\d+\.?\d*%", texto)
print(f"Porcentajes: {porcentajes}")
