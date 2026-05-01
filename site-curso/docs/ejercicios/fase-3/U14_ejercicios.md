# 📝 Ejercicios: U14 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U14_ejercicios)

---

```python
# U14: EJERCICIOS — Manejo de Errores y Logging Profesional

# ============================================================
# Ejercicio 1: Excepciones personalizadas
# Define dos excepciones personalizadas:
# - TickerInvalidoError: se lanza si el ticker no tiene 1-5 letras mayúsculas
# - DatosInsuficientesError: se lanza si hay menos datos de los requeridos
# Luego implementa validar_ticker(ticker) y calcular_sma(precios, ventana)
# que las usen.
# ============================================================
print("=== Ejercicio 1: Excepciones Personalizadas ===")

# Escribe tu código aquí



# Pruebas
try:
    print(validar_ticker("AAPL"))
    print(validar_ticker("12345"))
except TickerInvalidoError as e:
    print(f"Error: {e}")

try:
    print(calcular_sma([100, 102], 5))
except DatosInsuficientesError as e:
    print(f"Error: {e}")

# Output esperado:
# AAPL
# Error: Ticker inválido: 12345
# Error: Datos insuficientes: se necesitan 5, solo hay 2


# ============================================================
# Ejercicio 2: Sistema de trading con logging
# Configura logging con nivel INFO.
# Implementa ejecutar_trade(ticker, tipo, cantidad, precio) que:
# - Loggee en INFO cada orden recibida
# - Si cantidad <= 0 o precio <= 0, loggee ERROR y lance ValueError
# - Si el trade es exitoso, loggee INFO con el monto total
# ============================================================
print("\\n=== Ejercicio 2: Trading con Logging ===")
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s", datefmt="%H:%M:%S")
logger = logging.getLogger("trading")

# Escribe tu código aquí



# Pruebas
try:
    ejecutar_trade("AAPL", "compra", 100, 175.50)
    ejecutar_trade("MSFT", "compra", -5, 310.00)
except ValueError as e:
    print(f"Error capturado: {e}")

# Output esperado:
# HH:MM:SS [INFO] Orden recibida: AAPL compra 100@$175.50
# HH:MM:SS [INFO] Trade ejecutado: AAPL compra | Total: $17,550.00
# HH:MM:SS [ERROR] Cantidad inválida: -5
# Error capturado: Cantidad debe ser positiva


# ============================================================
# Ejercicio 3: try/except/else/finally
# Implementa cargar_datos_mercado(ruta) que:
# - try: abra y lea el archivo
# - except FileNotFoundError: muestre mensaje y retorne None
# - except Exception: capture cualquier otro error
# - else: imprima "Carga exitosa: X bytes" y retorne los datos
# - finally: imprima "Operación de carga finalizada"
# ============================================================
print("\\n=== Ejercicio 3: try/except/else/finally ===")

# Escribe tu código aquí



# Pruebas
datos = cargar_datos_mercado("/tmp/archivo_inexistente.csv")
print(f"Datos: {datos}")

# Output esperado:
# Error: Archivo no encontrado: /tmp/archivo_inexistente.csv
# Operación de carga finalizada
# Datos: None


# ============================================================
# Ejercicio 4: Tests con pytest (simulados)
# Escribe 5 funciones de test (sin pytest, usando assert directamente):
# 1. test_interes_compuesto: VF = C*(1+i)^t con valores conocidos
# 2. test_cagr: CAGR entre $5K y $12K en 8 años ≈ 11.57%
# 3. test_sharpe_positivo: Sharpe > 0 cuando rendimiento > tasa libre
# 4. test_vpn_positivo: VPN > 0 para flujos que superan inversión
# 5. test_ticker_valido: validar_ticker("aapl") == "AAPL"
# ============================================================
print("\\n=== Ejercicio 4: Tests Financieros ===")

# Escribe tus tests aquí



print("Todos los tests pasaron!")

# Output esperado:
# Todos los tests pasaron!
```

---

> [📥 Descargar archivo .py](U14_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
