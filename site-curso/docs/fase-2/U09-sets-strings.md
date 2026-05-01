# U09: Conjuntos y Strings Avanzados para Datos Financieros

> **Lectura previa:** [U08: Diccionarios — Portafolios](./U08-diccionarios.md)
> **Próxima unidad:** [U10: Archivos y Datos — CSV, JSON y Datos de Mercado](./U10-archivos.md)

---

## 1. Teoría

### 1.1 Conjuntos (`set`) — Colecciones sin duplicados

```python
sectores = {"Tecnología", "Finanzas", "Energía"}
numeros = set([1, 2, 2, 3, 3, 4])   # {1, 2, 3, 4} sin duplicados

# Agregar y eliminar
sectores.add("Salud")
sectores.remove("Finanzas")

# Verificar membresía (O(1), muy rápido)
"Tecnología" in sectores    # True
```

### 1.2 Operaciones de conjuntos

```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b     # Unión: {1, 2, 3, 4, 5, 6}
a & b     # Intersección: {3, 4}
a - b     # Diferencia: {1, 2}
a ^ b     # Diferencia simétrica: {1, 2, 5, 6}
```

### 1.3 Usos financieros de conjuntos

```python
# Encontrar activos comunes entre dos carteras
cartera_a = {"AAPL", "MSFT", "TSLA", "AMZN"}
cartera_b = {"AAPL", "GOOGL", "TSLA", "META"}

comunes = cartera_a & cartera_b       # {"AAPL", "TSLA"}
solo_a = cartera_a - cartera_b        # {"MSFT", "AMZN"}
todos = cartera_a | cartera_b         # Unión de ambas carteras

# Eliminar duplicados de una lista de tickers
lista_bruta = ["AAPL", "MSFT", "AAPL", "TSLA", "MSFT", "MSFT"]
unicos = list(set(lista_bruta))       # ["AAPL", "MSFT", "TSLA"]
```

### 1.4 Strings avanzados para finanzas

```python
# Métodos útiles para tickers
ticker = "  aapl  "
ticker = ticker.strip().upper()       # "AAPL"

# Verificar formato
"AAPL".isalpha()      # True
"AAPL123".isalnum()   # True
"123".isdigit()       # True

# Búsqueda
"AAPL: precio $175.50".find("$")      # 14
"compra_aapl_msft".startswith("compra")  # True

# Split y join
tickers_str = "AAPL,MSFT,TSLA,JPM"
tickers_lista = tickers_str.split(",") # ["AAPL", "MSFT", "TSLA", "JPM"]
", ".join(tickers_lista)              # "AAPL, MSFT, TSLA, JPM"
```

### 1.5 Expresiones regulares básicas para finanzas

Los ISIN, CUSIP y tickers tienen formatos específicos. Regex permite validarlos y extraerlos.

```python
import re

# Validar ticker (1-5 letras mayúsculas)
patron_ticker = r"^[A-Z]{1,5}$"
re.match(patron_ticker, "AAPL")   # Match
re.match(patron_ticker, "AAPL123")  # None

# Validar ISIN (2 letras + 10 alfanuméricos)
# Ej: US0378331005 (Apple Inc.)
patron_isin = r"^[A-Z]{2}[A-Z0-9]{10}$"
re.match(patron_isin, "US0378331005")  # Match

# Extraer tickers de un texto (ej: noticia financiera)
noticia = "Apple (AAPL) subió mientras Microsoft (MSFT) y Tesla (TSLA) cayeron."
tickers = re.findall(r"\(([A-Z]{1,5})\)", noticia)
print(tickers)  # ['AAPL', 'MSFT', 'TSLA']

# Buscar menciones de precios ($XXX.XX)
texto = "AAPL cerró a $175.50 tras abrir a $173.20"
precios = re.findall(r"\$\d+\.\d{2}", texto)
print(precios)  # ['$175.50', '$173.20']

# Split con múltiples delimitadores
datos = "AAPL|175.50;Tecnología,100"
campos = re.split(r"[|;,]", datos)
print(campos)  # ['AAPL', '175.50', 'Tecnología', '100']
```

### 1.6 Filtrado de universos de inversión con sets

```python
# Universo completo vs lista restringida (compliance)
universo = {"AAPL", "MSFT", "TSLA", "AMZN", "META", "GOOGL", "NVDA"}
restringidos = {"TSLA", "META"}                # Compliance bloquea
permitidos_esg = {"AAPL", "MSFT", "GOOGL"}     # Solo ESG

# Calcular universo invertible
invertible = (universo - restringidos) & permitidos_esg
print(f"Universo invertible: {invertible}")

# Verificar que todos los activos del portafolio son invertibles
portafolio = {"AAPL", "MSFT"}
es_valido = portafolio.issubset(invertible)    # True
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Parser de tickers en noticias

```python
import re

noticia = """
Las acciones de Apple Inc. (AAPL) subieron un 2.3% tras el reporte trimestral.
Microsoft (MSFT) también avanzó 1.8%. Sin embargo, Tesla (TSLA) cayó 4.2%
tras los comentarios de Elon Musk. JP Morgan (JPM) reiteró su recomendación
de compra para AAPL con precio objetivo de $200.00.
Goldman Sachs (GS) elevó su precio objetivo para MSFT a $400.00.
"""

# Extraer tickers únicos
tickers = set(re.findall(r"\(([A-Z]{1,5})\)", noticia))
print(f"Tickers mencionados: {tickers}")

# Extraer precios objetivo
precios_objetivo = re.findall(r"\$(\d+\.\d{2})", noticia)
print(f"Precios objetivo: {precios_objetivo}")

# Clasificar sentimiento por palabras clave
positivas = ["subió", "subieron", "avanzó", "compra", "elevó"]
negativas = ["cayó", "cayeron", "venta", "redujo"]

sentimiento = {}
for ticker in tickers:
    puntaje = 0
    for palabra in positivas:
        if re.search(rf"{ticker}.*{palabra}|{palabra}.*{ticker}", noticia):
            puntaje += 1
    for palabra in negativas:
        if re.search(rf"{ticker}.*{palabra}|{palabra}.*{ticker}", noticia):
            puntaje -= 1
    sentimiento[ticker] = "positivo" if puntaje > 0 else ("negativo" if puntaje < 0 else "neutral")

for ticker, sent in sentimiento.items():
    print(f"{ticker}: sentimiento {sent}")
```

### 2.2 Ejercicio guiado: Validación de ISIN/CUSIP

```python
import re

def validar_isin(isin):
    """ISIN: 2 letras de país + 9 alfanuméricos + 1 check digit"""
    patron = r"^[A-Z]{2}[A-Z0-9]{9}[0-9]$"
    return bool(re.match(patron, isin))

def validar_cusip(cusip):
    """CUSIP: 9 caracteres (letras mayúsculas o dígitos)"""
    patron = r"^[A-Z0-9]{9}$"
    return bool(re.match(patron, cusip))

# Ejemplos reales
print(validar_isin("US0378331005"))   # AAPL: True
print(validar_isin("US5949181045"))   # MSFT: True
print(validar_isin("INVALID1234"))    # False

print(validar_cusip("037833100"))     # AAPL: True
print(validar_cusip("594918104"))     # MSFT: True
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Intersección de universos (multi-factor screening)

```python
# Screening multi-factor
bajo_per = {"XOM", "JPM", "CVX", "PFE", "VZ"}
crecimiento_alto = {"AAPL", "JPM", "NVDA", "CVX"}
dividendos = {"XOM", "CVX", "JPM", "VZ", "T"}

# Acciones que cumplen los 3 criterios
top_picks = bajo_per & crecimiento_alto & dividendos

# Acciones que cumplen al menos 2 criterios
from collections import Counter
todas = list(bajo_per) + list(crecimiento_alto) + list(dividendos)
cumplen_2 = [t for t, c in Counter(todas).items() if c >= 2]

print(f"Top picks (3/3): {top_picks}")
print(f"Cumplen ≥2 criterios: {cumplen_2}")
```

### 3.2 Extracción de tickers desde un email de trading

```python
import re

email = """
FROM: trader@desk.com
TO: execution@broker.com
SUBJECT: Orders for today

BUY 1000 AAPL @ MARKET
SELL 500 TSLA LIMIT 250.00
BUY 200 MSFT @ MARKET
BUY 5000 AAPL LIMIT 175.50
"""

# Extraer órdenes de compra
compras = re.findall(r"BUY\s+(\d+)\s+([A-Z]{1,5})", email)
for cantidad, ticker in compras:
    print(f"Comprar {cantidad} {ticker}")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-2/U09_ejercicios.py`

1. **Parser de noticias:** Extrae tickers de un texto y clasifica sentimiento con palabras clave.

2. **Validador de ISIN:** Valida una lista de ISINs con regex. Separa válidos de inválidos.

3. **Intersección de universos:** Encuentra tickers que están en al menos 2 de 3 screenings.

4. **Extracción de precios:** De un texto financiero, extrae todos los montos en formato `$XXX.XX`.

---

## 5. Resumen

| Herramienta | Uso financiero |
|------------|---------------|
| `set` | Universos de inversión, sin duplicados |
| `&`, `\|`, `-` | Intersección, unión, diferencia |
| `strip().upper()` | Normalizar tickers |
| `re.search()` | Buscar patrón |
| `re.findall()` | Extraer todas las coincidencias |
| `re.split()` | Split con múltiples delimitadores |

---

## ✅ Autoevaluación

1. ¿Cómo encuentras los tickers comunes entre dos carteras?
2. ¿Qué hace `re.findall(r"\(([A-Z]{1,5})\)", texto)`?
3. ¿Cómo validas un ISIN con regex?
4. Extrae todos los precios en formato `$XXX.XX` del string `"AAPL $175.50, MSFT $310.00, TSLA $820.50"`.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U09.md`: Operaciones de sets, regex básico, patrones ISIN/CUSIP
> - `project-U09.md`: Parser de noticias, validador ISIN, screening multi-factor
