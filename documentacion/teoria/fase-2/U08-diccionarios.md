# U08: Diccionarios — Portafolios y Datos Estructurados

> **Lectura previa:** [U07: Listas y Tuplas](./U07-listas-tuplas.md)
> **Próxima unidad:** [U09: Sets y Strings Avanzados para Datos Financieros](./U09-sets-strings.md)

---

## 1. Teoría

### 1.1 Diccionarios — Pares clave-valor

```python
accion = {
    "ticker": "AAPL",
    "precio": 175.50,
    "cantidad": 10,
    "sector": "Tecnología"
}

print(accion["ticker"])              # AAPL
print(accion.get("dividendo", 0))    # 0 (valor por defecto)

# Modificación
accion["precio"] = 180.00
accion["mercado"] = "NASDAQ"
del accion["sector"]
```

### 1.2 Portafolios como diccionarios

```python
# Portafolio simple: ticker → valor
portafolio = {"AAPL": 3500, "MSFT": 6200, "TSLA": 5300, "JPM": 4100, "XOM": 2800}

total = sum(portafolio.values())
print("Pesos del portafolio:")
for ticker, valor in portafolio.items():
    peso = valor / total * 100
    print(f"{ticker}: ${valor:,.2f} ({peso:.1f}%)")
```

### 1.3 Métodos de diccionarios

| Método | Descripción |
|--------|------------|
| `.keys()` | Vista de claves |
| `.values()` | Vista de valores |
| `.items()` | Vista de tuplas (clave, valor) |
| `.get(clave, default)` | Obtener con valor por defecto |
| `.update(dict2)` | Fusionar diccionarios |
| `.pop(clave)` | Eliminar y retornar |

```python
portafolio = {"AAPL": 175.50, "MSFT": 310.00}
for ticker, precio in portafolio.items():
    print(f"{ticker}: ${precio}")

# Dict comprehension
precios_dobles = {t: p * 2 for t, p in portafolio.items()}
```

### 1.4 Diccionarios anidados — Estados financieros

```python
# Balance sheet como dict anidado
balance = {
    "AAPL": {
        "activos_corrientes": 143_566_000_000,
        "activos_totales": 352_755_000_000,
        "pasivos_corrientes": 145_308_000_000,
        "pasivos_totales": 302_083_000_000,
        "patrimonio": 50_672_000_000,
    },
    "MSFT": {
        "activos_corrientes": 169_684_000_000,
        "activos_totales": 364_840_000_000,
        "pasivos_corrientes": 95_082_000_000,
        "pasivos_totales": 198_298_000_000,
        "patrimonio": 166_542_000_000,
    },
}

for ticker, datos in balance.items():
    ratio_liquidez = datos["activos_corrientes"] / datos["pasivos_corrientes"]
    ratio_endeudamiento = datos["pasivos_totales"] / datos["activos_totales"]
    roe = datos["patrimonio"] / datos["activos_totales"]  # simplificado
    print(f"{ticker}: Liquidez={ratio_liquidez:.2f}, Deuda={ratio_endeudamiento:.1%}, ROE aprox={roe:.1%}")
```

### 1.5 `defaultdict` — Diccionarios con valor por defecto

```python
from collections import defaultdict

# Agrupar transacciones por ticker sin verificar si la clave existe
transacciones = [
    ("AAPL", "compra", 1500),
    ("MSFT", "compra", 2800),
    ("AAPL", "venta", 2000),
    ("TSLA", "compra", 3500),
]

por_ticker = defaultdict(float)
for ticker, tipo, monto in transacciones:
    if tipo == "compra":
        por_ticker[ticker] -= monto
    else:
        por_ticker[ticker] += monto

for ticker, pl in por_ticker.items():
    print(f"{ticker}: P&L ${pl:+,.2f}")
```

### 1.6 `Counter` — Conteo de frecuencias

```python
from collections import Counter

# Frecuencia de tipos de orden
ordenes = ["compra", "venta", "compra", "compra", "venta", "venta", "compra"]
conteo = Counter(ordenes)
print(conteo)  # Counter({'compra': 4, 'venta': 3})

# Top N más comunes
print(conteo.most_common(1))  # [('compra', 4)]

# Total de órdenes
print(f"Total: {sum(conteo.values())}")
```

### 1.7 Agrupar portafolio por sector

```python
portafolio = {
    "AAPL": {"cantidad": 10, "precio": 175, "sector": "Tecnología"},
    "MSFT": {"cantidad": 5, "precio": 310, "sector": "Tecnología"},
    "XOM": {"cantidad": 20, "precio": 85, "sector": "Energía"},
    "JPM": {"cantidad": 15, "precio": 140, "sector": "Finanzas"},
    "CVX": {"cantidad": 10, "precio": 150, "sector": "Energía"},
}

from collections import defaultdict
por_sector = defaultdict(float)
for ticker, datos in portafolio.items():
    valor = datos["cantidad"] * datos["precio"]
    por_sector[datos["sector"]] += valor

for sector, valor in sorted(por_sector.items()):
    print(f"{sector}: ${valor:,.2f}")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Performance de portafolio

```python
# Precios al inicio y fin del período
precios_inicio = {"AAPL": 150, "MSFT": 280, "TSLA": 900, "JPM": 135}
precios_fin = {"AAPL": 175, "MSFT": 310, "TSLA": 820, "JPM": 142}
cantidades = {"AAPL": 10, "MSFT": 5, "TSLA": 3, "JPM": 20}

# Calcular rendimiento ponderado
valor_inicio = sum(cantidades[t] * precios_inicio[t] for t in cantidades)
valor_fin = sum(cantidades[t] * precios_fin[t] for t in cantidades)
rendimiento = (valor_fin - valor_inicio) / valor_inicio * 100

# Rendimiento por activo
for ticker in cantidades:
    ri = (precios_fin[ticker] - precios_inicio[ticker]) / precios_inicio[ticker] * 100
    peso = cantidades[ticker] * precios_inicio[ticker] / valor_inicio * 100
    print(f"{ticker}: {ri:+.2f}% (peso: {peso:.1f}%)")

print(f"\nRendimiento total: {rendimiento:+.2f}%")
```

### 2.2 Ejercicio guiado: Rebalanceo de portafolio

```python
# Pesos objetivo vs pesos actuales
pesos_objetivo = {"AAPL": 0.30, "MSFT": 0.25, "TSLA": 0.15, "JPM": 0.30}
capital = 100000
precios_actuales = {"AAPL": 175, "MSFT": 310, "TSLA": 820, "JPM": 142}

posiciones_objetivo = {}
for ticker, peso in pesos_objetivo.items():
    monto = capital * peso
    cantidad = monto / precios_actuales[ticker]
    posiciones_objetivo[ticker] = cantidad

print("Rebalanceo:")
for ticker, cantidad in posiciones_objetivo.items():
    monto = cantidad * precios_actuales[ticker]
    print(f"{ticker}: {cantidad:.4f} acciones → ${monto:,.2f} ({pesos_objetivo[ticker]:.0%})")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Estado de resultados como dict anidado

```python
estado_resultados = {
    "AAPL": {
        "ingresos": 383_285_000_000,
        "costo_ventas": 214_137_000_000,
        "gastos_operativos": 54_847_000_000,
        "impuestos": 16_741_000_000,
    }
}

for ticker, datos in estado_resultados.items():
    utilidad_bruta = datos["ingresos"] - datos["costo_ventas"]
    utilidad_operativa = utilidad_bruta - datos["gastos_operativos"]
    utilidad_neta = utilidad_operativa - datos["impuestos"]
    margen_bruto = utilidad_bruta / datos["ingresos"] * 100
    margen_neto = utilidad_neta / datos["ingresos"] * 100
    
    print(f"--- {ticker} ---")
    print(f"Ingresos: ${datos['ingresos']:,}")
    print(f"Margen bruto: {margen_bruto:.1f}%")
    print(f"Margen neto: {margen_neto:.1f}%")
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-2/U08_ejercicios.py`

1. **Portafolio de 5 activos:** Calcula valor total, pesos, rendimiento ponderado.

2. **Agrupador por sector:** Usa defaultdict para agrupar el valor del portafolio por sector.

3. **Frecuencia de órdenes:** Usa Counter para contar tipos de órdenes de trading.

4. **Estados financieros:** Con dicts anidados, calcula ratios de liquidez y endeudamiento.

---

## 5. Resumen

| Herramienta | Uso financiero |
|------------|---------------|
| `dict` | Portafolios, precios, datos estructurados |
| `.get()` | Acceder con valor por defecto |
| Dict comprehension | `{t: p*2 for t, p in d.items()}` |
| `defaultdict` | Agrupar sin verificar claves |
| `Counter` | Conteo de frecuencias |
| Dicts anidados | Estados financieros, balances |

---

## ✅ Autoevaluación

1. ¿Cómo accedes a un valor de un diccionario sin riesgo de KeyError?
2. ¿Qué ventaja tiene `defaultdict` sobre `dict`?
3. ¿Cómo agrupas items de un portafolio por sector?
4. Crea un dict comprehension con tickers y su market cap en millones.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U08.md`: Métodos de dict, defaultdict, Counter, dict comprehension
> - `project-U08.md`: Portafolio como dict, agrupación por sector, estados financieros
