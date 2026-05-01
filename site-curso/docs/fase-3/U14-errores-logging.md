# U14: Manejo de Errores y Logging Profesional

> **Lectura previa:** [U13: Módulos, Paquetes y Arquitectura](./U13-modulos-paquetes.md)
> **Próxima unidad:** [U15: Clases y Objetos — Modelando Instrumentos](../fase-4/U15-clases-objetos.md)

---

## 1. Teoría

### 1.1 Jerarquía de excepciones en Python

```
BaseException
 ├── SystemExit
 ├── KeyboardInterrupt
 └── Exception
      ├── ValueError
      ├── TypeError
      ├── KeyError
      ├── IndexError
      ├── ZeroDivisionError
      ├── FileNotFoundError
      └── RuntimeError
```

### 1.2 `try/except/else/finally` completo

```python
def cargar_datos_mercado(ruta):
    """Carga datos con manejo completo de errores."""
    try:
        with open(ruta, "r") as f:
            datos = f.read()
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {ruta}")
        return None
    except PermissionError:
        print(f"Error: Sin permisos para leer {ruta}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    else:
        # Solo se ejecuta si NO hubo excepción
        print(f"Archivo cargado exitosamente: {len(datos)} bytes")
        return datos
    finally:
        # Se ejecuta SIEMPRE (haya o no error)
        print("Intento de carga finalizado")
```

### 1.3 Excepciones personalizadas financieras

```python
class ErrorFinanciero(Exception):
    """Clase base para errores financieros."""
    pass

class TickerInvalidoError(ErrorFinanciero):
    """El ticker no cumple con el formato esperado."""
    def __init__(self, ticker, mensaje="Ticker inválido"):
        self.ticker = ticker
        super().__init__(f"{mensaje}: {ticker}")

class DatosInsuficientesError(ErrorFinanciero):
    """No hay suficientes datos para el cálculo."""
    def __init__(self, requeridos, disponibles):
        super().__init__(
            f"Datos insuficientes: se necesitan {requeridos}, "
            f"solo hay {disponibles}"
        )

class PrecioNegativoError(ErrorFinanciero):
    """Se ingresó un precio negativo."""
    pass

# Uso
def validar_ticker(ticker):
    if not ticker.isalpha() or not (1 <= len(ticker) <= 5):
        raise TickerInvalidoError(ticker)
    return ticker.upper()

def calcular_sma(precios, ventana):
    if len(precios) < ventana:
        raise DatosInsuficientesError(ventana, len(precios))
    return sum(precios[-ventana:]) / ventana
```

### 1.4 `logging` — Registro profesional de eventos

En producción, los prints no alcanzan. `logging` te da niveles, archivos y formato.

```python
import logging

# Configuración básica
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger(__name__)

# Niveles de severidad
logger.debug("Depuración: iteración 5 del solver")       # Solo en desarrollo
logger.info("Pipeline de datos iniciado")                 # Eventos normales
logger.warning("Volatilidad alta en AAPL: 45%")          # Alerta
logger.error("No se pudo conectar a Bloomberg API")      # Error recuperable
logger.critical("Base de datos de precios corrupta")      # Error grave
```

### 1.5 Handlers y formatters avanzados

```python
import logging

# Logger con archivo rotativo
logger = logging.getLogger("quantlib")
logger.setLevel(logging.DEBUG)

# Handler para archivo (con rotación)
from logging.handlers import RotatingFileHandler
fh = RotatingFileHandler("quantlib.log", maxBytes=1_000_000, backupCount=3)
fh.setLevel(logging.DEBUG)

# Handler para consola (solo warnings y errores)
ch = logging.StreamHandler()
ch.setLevel(logging.WARNING)

# Formateador
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)-8s] %(name)s - %(message)s"
)
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

# Uso
logger.info("Cargando precios de 500 tickers...")
logger.warning("Datos faltantes en 12 tickers")
logger.error("Ticker XYZ123 no encontrado en la base")
```

### 1.6 `warnings` — Alertas no bloqueantes

```python
import warnings

def calcular_sharpe_con_pocos_datos(rendimientos):
    if len(rendimientos) < 30:
        warnings.warn(
            f"Sharpe calculado con solo {len(rendimientos)} datos. "
            f"Resultado poco confiable.",
            UserWarning
        )
    media = sum(rendimientos) / len(rendimientos)
    # ... resto del cálculo
    return resultado
```

### 1.7 Intro a `pytest`

Los tests son obligatorios en cualquier desk cuantitativo. Sin tests, un bug en pricing puede costar millones.

```python
# test_pricing.py
import pytest
from quantlib.pricing import valoracion_bono, TickerInvalidoError

def test_valoracion_bono_a_la_par():
    """Un bono con cupón = tasa de mercado debe valer a la par."""
    precio = valoracion_bono(1000, 5, 5, 10)
    assert abs(precio - 1000) < 0.01

def test_valoracion_bono_con_prima():
    """Si cupón > tasa de mercado, el bono vale más que el nominal."""
    precio = valoracion_bono(1000, 8, 5, 10)
    assert precio > 1000

def test_valoracion_bono_con_descuento():
    """Si cupón < tasa de mercado, el bono vale menos que el nominal."""
    precio = valoracion_bono(1000, 3, 5, 10)
    assert precio < 1000

def test_ticker_invalido():
    with pytest.raises(TickerInvalidoError):
        validar_ticker("12345")

def test_ticker_valido():
    assert validar_ticker("aapl") == "AAPL"

def test_sma_datos_insuficientes():
    with pytest.raises(DatosInsuficientesError):
        calcular_sma([100, 102], 5)
```

**Ejecutar tests:**

```bash
# Instalar pytest
pip install pytest

# Ejecutar todos los tests
pytest tests/

# Ejecutar con verbose
pytest -v tests/

# Ejecutar un archivo específico
pytest tests/test_pricing.py -v
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Sistema de validación con excepciones + logging

```python
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("trading")

class OrdenInvalidaError(Exception):
    pass

def validar_orden(ticker, tipo, cantidad, precio):
    """Valida una orden de trading con logging."""
    
    logger.info(f"Validando orden: {ticker} {tipo} {cantidad}@{precio}")
    
    try:
        if not ticker.isalpha() or len(ticker) > 5:
            raise OrdenInvalidaError(f"Ticker inválido: {ticker}")
        
        if tipo not in ("compra", "venta"):
            raise OrdenInvalidaError(f"Tipo inválido: {tipo}")
        
        if cantidad <= 0:
            raise OrdenInvalidaError(f"Cantidad debe ser positiva: {cantidad}")
        
        if precio <= 0:
            raise OrdenInvalidaError(f"Precio debe ser positivo: {precio}")
        
        logger.info(f"Orden válida: {ticker} {tipo} {cantidad}@{precio}")
        return {"ticker": ticker, "tipo": tipo, "cantidad": cantidad, "precio": precio}
    
    except OrdenInvalidaError as e:
        logger.error(f"Orden rechazada: {e}")
        raise

# Probar
try:
    validar_orden("AAPL", "compra", 100, 175.50)    # OK
    validar_orden("", "venta", 50, 200)              # Error
except OrdenInvalidaError:
    pass
```

### 2.2 Ejercicio guiado: Escribir tests con pytest

```python
# tests/test_finanzas.py (simulado en un solo archivo)
import sys

def test_interes_compuesto():
    """VF = C * (1+i)^t"""
    capital = 10000
    tasa = 0.08
    tiempo = 10
    monto = capital * (1 + tasa) ** tiempo
    assert abs(monto - 21589.25) < 0.01

def test_cagr():
    """CAGR de $5K a $12K en 8 años ≈ 11.57%"""
    cagr = ((12000 / 5000) ** (1/8) - 1) * 100
    assert abs(cagr - 11.57) < 0.1

def test_sharpe_positivo():
    """Sharpe debe ser positivo si rendimiento > rf."""
    sharpe = (15 - 4) / 20
    assert sharpe > 0

def test_vpn_inversion_recuperable():
    """VPN debe ser positivo si los flujos superan la inversión."""
    vpn = -10000 + 3000/1.1 + 4000/1.1**2 + 5000/1.1**3 + 6000/1.1**4
    assert vpn > 0

print("Todos los tests pasaron!")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Validación de datos de mercado en producción

```python
import logging
from typing import Optional

logger = logging.getLogger("market_data")

class MarketDataError(Exception):
    pass

def validar_ohlcv(datos: dict) -> bool:
    """Valida datos OHLCV antes de alimentar modelos de pricing."""
    requeridos = ["open", "high", "low", "close", "volume"]
    
    for campo in requeridos:
        if campo not in datos:
            raise MarketDataError(f"Campo faltante: {campo}")
    
    if datos["high"] < datos["low"]:
        raise MarketDataError(f"High ({datos['high']}) < Low ({datos['low']})")
    
    if datos["close"] < datos["low"] or datos["close"] > datos["high"]:
        logger.warning(f"Close fuera de rango High-Low: {datos}")
    
    if datos["volume"] < 0:
        raise MarketDataError(f"Volumen negativo: {datos['volume']}")
    
    return True

def obtener_precio(ticker: str, fuente: str = "bloomberg") -> Optional[float]:
    """Obtiene precio con manejo robusto de errores."""
    logger.info(f"Solicitando precio de {ticker} desde {fuente}")
    
    try:
        # Simulación de llamada a API
        if ticker == "INVALIDO":
            raise MarketDataError("Ticker no encontrado en la base")
        return 175.50
    except MarketDataError as e:
        logger.error(f"Error de datos: {e}")
        return None
    except Exception as e:
        logger.critical(f"Error inesperado en API de {fuente}: {e}")
        raise
```

---

## 4. Ejercicios Propuestos

> Los archivos están en `documentacion/ejercicios/fase-3/U14_ejercicios.py`

1. **Excepciones personalizadas:** Define `TickerInvalidoError` y `DatosInsuficientesError`. Úsalas para validar tickers.

2. **Logging configurado:** Configura logging con niveles INFO y WARNING para un sistema de trading simulado.

3. **try/except/else/finally:** Implementa carga de datos con el patrón completo de manejo de errores.

4. **Tests con pytest:** Escribe 5 tests unitarios para funciones financieras (interés compuesto, CAGR, Sharpe, VPN).

---

## 5. Resumen

| Herramienta | Propósito |
|------------|----------|
| `try/except/else/finally` | Manejo completo de errores |
| `raise MiError()` | Lanzar error personalizado |
| `logging` | Registro profesional con niveles |
| `logging.basicConfig()` | Configuración rápida |
| `RotatingFileHandler` | Log rotativo automático |
| `warnings.warn()` | Alertas no bloqueantes |
| `pytest` | Framework de testing |
| `pytest.raises()` | Verificar que se lanza excepción |

---

## ✅ Autoevaluación

1. ¿Cuándo se ejecuta el bloque `else` de un `try/except`?
2. ¿Qué diferencia hay entre `logger.warning()` y `warnings.warn()`?
3. ¿Para qué sirven las excepciones personalizadas en finanzas?
4. Escribe un test con pytest que verifique que `validar_ticker("123")` lanza `TickerInvalidoError`.

---

> 📝 **Knowledge Wiki:** Guarda en memoria:
> - `reference-U14.md`: Jerarquía de excepciones, logging con handlers, pytest
> - `project-U14.md`: Excepciones personalizadas, validación de órdenes, tests para quantlib
