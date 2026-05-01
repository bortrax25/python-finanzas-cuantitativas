# U13: EJERCICIOS — Módulos, Paquetes y Arquitectura de Proyecto

# ============================================================
# Ejercicio 1: Crear submódulo riesgo.py
# Implementa tres funciones en un "módulo simulado":
# - sharpe_ratio(rendimiento, rf, volatilidad) -> float
# - var_historico(rendimientos, confianza=0.95) -> float
# - volatilidad_anualizada(rendimientos_diarios) -> float
# Incluye type hints en todas.
# ============================================================
print("=== Ejercicio 1: Submódulo riesgo.py ===")

# Escribe tus funciones aquí (simulando estar en riesgo.py)



# Probando
print(f"Sharpe: {sharpe_ratio(12, 4, 18):.2f}")
rendimientos = [0.5, -0.2, 1.8, -0.7, 0.3, 1.2, -0.4, 0.8, -1.1, 0.6,
                1.5, -0.9, 0.4, 2.1, -0.5, 0.7, -0.3, 1.0, -0.8, 0.9]
print(f"VaR 95%: {var_historico(rendimientos):.2f}%")
print(f"Volatilidad anualizada: {volatilidad_anualizada(rendimientos):.2f}%")

# Output esperado:
# Sharpe: 0.44
# VaR 95%: X.XX%
# Volatilidad anualizada: X.XX%


# ============================================================
# Ejercicio 2: if __name__ == "__main__"
# Escribe un script que defina dos funciones financieras.
# Cuando se ejecuta directamente (python script.py), debe:
#   - Ejecutar pruebas con valores de ejemplo
#   - Mostrar resultados
# Cuando se importa como módulo, no debe ejecutar nada.
# ============================================================
print("\n=== Ejercicio 2: Entry Point ===")

def valor_futuro(capital: float, tasa: float, anios: int) -> float:
    return capital * (1 + tasa / 100) ** anios

def cuota_prestamo(monto: float, tasa_anual: float, plazo_meses: int) -> float:
    i = (tasa_anual / 100) / 12
    return monto * (i * (1 + i) ** plazo_meses) / ((1 + i) ** plazo_meses - 1)

# Escribe el bloque if __name__ == "__main__" aquí



# Output esperado (al ejecutar directamente):
# === Probando funciones financieras ===
# VF $10,000 al 8% por 10 años = $21,589.25
# Cuota préstamo $200K al 10% a 240 meses = $1,930.07


# ============================================================
# Ejercicio 3: Estructura de paquete quantlib/
# Diseña la estructura de un paquete quantlib/ con los submódulos:
#   pricing/ (__init__.py + bonos.py + acciones.py)
#   riesgo/  (__init__.py + metricas.py)
#   datos/   (__init__.py + io.py)
# Muestra la estructura de carpetas y archivos con print().
# ============================================================
print("\n=== Ejercicio 3: Estructura de Paquete ===")

# Escribe tu código aquí



# Output esperado:
# quantlib/
# ├── __init__.py
# ├── pricing/
# │   ├── __init__.py
# │   ├── bonos.py
# │   └── acciones.py
# ├── riesgo/
# │   ├── __init__.py
# │   └── metricas.py
# └── datos/
#     ├── __init__.py
#     └── io.py


# ============================================================
# Ejercicio 4: Simular uso real del paquete
# Usando las funciones del Ejercicio 1, simula cómo importarías
# y usarías el paquete en un script real.
# Muestra 3 formas diferentes de import.
# ============================================================
print("\n=== Ejercicio 4: Uso del Paquete ===")

# Escribe tu código aquí



# Output esperado:
# Forma 1 (import módulo):
#   import quantlib.riesgo.metricas as riesgo
#   sharpe = riesgo.sharpe_ratio(12, 4, 18)
# Forma 2 (from ... import función):
#   from quantlib.riesgo.metricas import sharpe_ratio
#   sharpe = sharpe_ratio(12, 4, 18)
# Forma 3 (from ... import *):
#   from quantlib import sharpe_ratio
#   sharpe = sharpe_ratio(12, 4, 18)
