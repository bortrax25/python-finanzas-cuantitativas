# U11: Diccionarios y Conjuntos

> **Lectura previa:** [U10: Listas y tuplas](./U10-listas-tuplas.md)
> **Próxima unidad:** [U12: Manejo de archivos CSV](./U12-archivos-csv.md)

---

## 1. Teoría

### 1.1 Diccionarios — Pares clave-valor

Un **diccionario** (`dict`) almacena pares **clave: valor**. Las claves deben ser únicas e inmutables (strings, números, tuplas).

```python
# Creación
accion = {
    "ticker": "AAPL",
    "precio": 175.50,
    "cantidad": 10,
    "sector": "Tecnología"
}

# Acceso
print(accion["ticker"])        # AAPL
print(accion.get("dividendo", 0))  # 0 (valor default si no existe)

# Modificación
accion["precio"] = 180.00      # Actualizar
accion["mercado"] = "NASDAQ"   # Agregar nueva clave
del accion["sector"]           # Eliminar
```

### 1.2 Métodos de diccionarios

| Método | Descripción |
|--------|------------|
| `.keys()` | Lista de claves |
| `.values()` | Lista de valores |
| `.items()` | Lista de tuplas (clave, valor) |
| `.get(clave, default)` | Obtener con valor por defecto |
| `.update(dict2)` | Fusionar diccionarios |
| `.pop(clave)` | Eliminar y retornar |

```python
portafolio = {"AAPL": 175.50, "MSFT": 310.00, "TSLA": 250.00}

for ticker, precio in portafolio.items():
    print(f"{ticker}: ${precio}")

# Dict comprehension
precios_dobles = {t: p * 2 for t, p in portafolio.items()}
# {"AAPL": 351.00, "MSFT": 620.00, "TSLA": 500.00}
```

### 1.3 Diccionarios anidados (JSON-like)

```python
portafolio = {
    "AAPL": {"cantidad": 10, "precio_compra": 150, "sector": "Tecnología"},
    "MSFT": {"cantidad": 5, "precio_compra": 280, "sector": "Tecnología"},
    "XOM": {"cantidad": 20, "precio_compra": 85, "sector": "Energía"},
}

# Valor total del portafolio
total = sum(d["cantidad"] * d["precio_compra"] for d in portafolio.values())

# Agrupar por sector
from collections import defaultdict
por_sector = defaultdict(float)
for ticker, datos in portafolio.items():
    por_sector[datos["sector"]] += datos["cantidad"] * datos["precio_compra"]

for sector, valor in por_sector.items():
    print(f"{sector}: ${valor:,.2f}")
```

### 1.4 Conjuntos (set) — Colecciones sin duplicados

Un **conjunto** (`set`) es una colección no ordenada de elementos únicos.

```python
# Creación
sectores = {"Tecnología", "Finanzas", "Energía"}
numeros = set([1, 2, 2, 3, 3, 4])   # {1, 2, 3, 4}

# Operaciones de conjuntos
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

a | b     # Unión: {1, 2, 3, 4, 5, 6}
a & b     # Intersección: {3, 4}
a - b     # Diferencia: {1, 2}
a ^ b     # Diferencia simétrica: {1, 2, 5, 6}
```

### 1.5 Usos financieros de conjuntos

```python
# Encontrar activos comunes entre dos carteras
cartera_a = {"AAPL", "MSFT", "TSLA", "AMZN"}
cartera_b = {"AAPL", "GOOGL", "TSLA", "META"}

comunes = cartera_a & cartera_b
print(f"Activos en ambas: {comunes}")

# Activos únicos de cada cartera
solo_a = cartera_a - cartera_b
solo_b = cartera_b - cartera_a

# Verificar si un ticker existe
if "AAPL" in cartera_a:
    print("AAPL está en la cartera A")
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Libro de órdenes (order book)

```python
ordenes = {}

# Agregar órdenes
ordenes["ORD001"] = {"ticker": "AAPL", "tipo": "compra", "precio": 150.00, "cantidad": 100}
ordenes["ORD002"] = {"ticker": "TSLA", "tipo": "venta", "precio": 900.00, "cantidad": 50}

for oid, datos in ordenes.items():
    print(f"{oid}: {datos['tipo'].upper()} {datos['cantidad']} {datos['ticker']} @ ${datos['precio']}")

# Cancelar una orden
ordenes.pop("ORD001", None)
```

### 2.2 Ejercicio guiado: Contador de frecuencia

```python
movimientos = ["compra", "venta", "compra", "compra", "venta", "compra", "venta", "venta"]

frecuencia = {}
for mov in movimientos:
    frecuencia[mov] = frecuencia.get(mov, 0) + 1

print(frecuencia)  # {"compra": 4, "venta": 4}

# Con dict comprehension
conteo = {tipo: movimientos.count(tipo) for tipo in set(movimientos)}
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Datos de mercado como diccionario

```python
mercado = {
    "AAPL": {"precio": 175.50, "cambio": 1.2, "volumen": 50000000},
    "MSFT": {"precio": 310.00, "cambio": -0.5, "volumen": 25000000},
    "TSLA": {"precio": 250.00, "cambio": 2.8, "volumen": 80000000},
}

# Top 3 por volumen
ranking = sorted(mercado.items(), key=lambda x: x[1]["volumen"], reverse=True)[:3]
for ticker, datos in ranking:
    print(f"{ticker}: Vol {datos['volumen']:,}")
```

### 3.2 Cartera con pesos relativos

```python
cartera = {"AAPL": 3500, "MSFT": 6200, "TSLA": 5300}
total = sum(cartera.values())

print("Pesos del portafolio:")
for ticker, valor in cartera.items():
    peso = valor / total * 100
    print(f"{ticker}: {peso:.1f}%")
```

---

## 4. Ejercicios Propuestos

1. **Analizador de transacciones:** Procesa una lista de transacciones (dicts) y calcula P&L por ticker.

2. **Índice de concentración (HHI):** Calcula el Herfindahl-Hirschman Index para medir concentración del portafolio.

3. **Detección de duplicados:** Usa sets para encontrar tickers repetidos en una lista de entradas.

4. **Cotizaciones en tiempo "simulado":** Mantén un dict de precios que se actualiza periódicamente y calcula cambios.

---

## 5. Resumen

| Estructura | Sintaxis | Mutabilidad | Duplicados | Orden |
|-----------|---------|------------|-----------|-------|
| Lista | `[1, 2]` | Mutable | Sí | Sí |
| Tupla | `(1, 2)` | Inmutable | Sí | Sí |
| Dict | `{a:1, b:2}` | Mutable | Claves: no | Python 3.7+: sí |
| Set | `{1, 2}` | Mutable | No | No |

---

## ✅ Autoevaluación

1. ¿Cómo agregas una clave nueva a un diccionario existente?
2. ¿Qué pasa si intentas crear un set con elementos duplicados: `set([1,1,2,2,3])`?
3. ¿Cuál es la diferencia entre `diccionario["clave"]` y `diccionario.get("clave")`?
4. Crea un dict comprehension que asocie números del 1 al 5 con su cubo.

---

> 📝 **Knowledge Wiki:** Guarda `reference-U11.md` (métodos de dicts y sets) y `project-U11.md` (libro de órdenes y analizador de cartera).
