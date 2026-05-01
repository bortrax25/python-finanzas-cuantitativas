# ✅ Soluciones: U14 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U14_soluciones)

---

```python
# U14: SOLUCIONES — Manejo de Errores y Logging Profesional

# ============================================================
# Ejercicio 1: Excepciones Personalizadas
# ============================================================
print("=== Ejercicio 1: Excepciones Personalizadas ===")

class TickerInvalidoError(Exception):
    def __init__(self, ticker):
        super().__init__(f"Ticker inválido: {ticker}")
        self.ticker = ticker

class DatosInsuficientesError(Exception):
    def __init__(self, requeridos, disponibles):
        super().__init__(f"Datos insuficientes: se necesitan {requeridos}, solo hay {disponibles}")

def validar_ticker(ticker):
    if not ticker.isalpha() or not (1 <= len(ticker) <= 5):
        raise TickerInvalidoError(ticker)
    return ticker.upper()

def calcular_sma(precios, ventana):
    if len(precios) < ventana:
        raise DatosInsuficientesError(ventana, len(precios))
    return sum(precios[-ventana:]) / ventana

try:
    print(validar_ticker("AAPL"))
    print(validar_ticker("12345"))
except TickerInvalidoError as e:
    print(f"Error: {e}")

try:
    print(calcular_sma([100, 102], 5))
except DatosInsuficientesError as e:
    print(f"Error: {e}")


# ============================================================
# Ejercicio 2: Trading con Logging
# ============================================================
print("\\n=== Ejercicio 2: Trading con Logging ===")
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("trading")

def ejecutar_trade(ticker, tipo, cantidad, precio):
    logger.info(f"Orden recibida: {ticker} {tipo} {cantidad}@${precio:.2f}")

    if cantidad <= 0:
        logger.error(f"Cantidad inválida: {cantidad}")
        raise ValueError("Cantidad debe ser positiva")

    if precio <= 0:
        logger.error(f"Precio inválido: {precio}")
        raise ValueError("Precio debe ser positivo")

    monto_total = cantidad * precio
    logger.info(f"Trade ejecutado: {ticker} {tipo} | Total: ${monto_total:,.2f}")
    return monto_total

try:
    ejecutar_trade("AAPL", "compra", 100, 175.50)
    ejecutar_trade("MSFT", "compra", -5, 310.00)
except ValueError as e:
    print(f"Error capturado: {e}")


# ============================================================
# Ejercicio 3: try/except/else/finally
# ============================================================
print("\\n=== Ejercicio 3: try/except/else/finally ===")

def cargar_datos_mercado(ruta):
    try:
        with open(ruta, "r") as f:
            datos = f.read()
    except FileNotFoundError:
        print(f"Error: Archivo no encontrado: {ruta}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
    else:
        print(f"Carga exitosa: {len(datos)} bytes")
        return datos
    finally:
        print("Operación de carga finalizada")

datos = cargar_datos_mercado("/tmp/archivo_inexistente.csv")
print(f"Datos: {datos}")


# ============================================================
# Ejercicio 4: Tests Financieros
# ============================================================
print("\\n=== Ejercicio 4: Tests Financieros ===")

def test_interes_compuesto():
    VF = 10000 * (1 + 0.08) ** 10
    assert abs(VF - 21589.25) < 0.01, f"VF={VF}, esperado 21589.25"

def test_cagr():
    cagr = ((12000 / 5000) ** (1/8) - 1) * 100
    assert abs(cagr - 11.57) < 0.1, f"CAGR={cagr}, esperado ~11.57%"

def test_sharpe_positivo():
    sharpe = (15 - 4) / 20
    assert sharpe > 0, f"Sharpe={sharpe}, debe ser positivo"

def test_vpn_positivo():
    vpn = -10000 + 3000/1.1 + 4000/1.1**2 + 5000/1.1**3 + 6000/1.1**4
    assert vpn > 0, f"VPN={vpn}, debe ser positivo"

def test_ticker_valido():
    resultado = validar_ticker("aapl")
    assert resultado == "AAPL", f"Resultado={resultado}, esperado AAPL"

test_interes_compuesto()
test_cagr()
test_sharpe_positivo()
test_vpn_positivo()
test_ticker_valido()

print("Todos los tests pasaron!")
```

---

> [📥 Descargar archivo .py](U14_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
