# U24: EJERCICIOS — Valor del Dinero en el Tiempo y Renta Fija

# ============================================================
# Ejercicio 1: Bond Pricer Completo
# Construye un pricer de bonos que calcule: precio, YTM por
# Newton-Raphson, Macaulay duration, duration modificada y convexidad
# Bono: VN=$1,000, cupon 5% anual, pagos semestrales, 8 anios
# Precio de mercado: $980
# ============================================================
print("=== Ejercicio 1: Bond Pricer Completo ===")
valor_nominal = 1000
tasa_cupon_pct = 5.0
anios_vencimiento = 8
frecuencia_pago = 2
precio_mercado = 980

# Escribe tu codigo aqui: implementa las funciones y calcula todas las metricas



# Output esperado:
# Precio del bono (YTM 5.3%): $980.31
# YTM (Newton-Raphson): 5.30%
# Macaulay Duration: 6.52 anios
# Modified Duration: 6.35
# Convexidad: 50.23


# ============================================================
# Ejercicio 2: Sensibilidad de Precio y Convexity Adjustment
# Para un bono 10Y cupon 5%, grafica la relacion precio-YTM para
# YTM de 1% a 15%. Compara la caida de precio usando solo duration
# modificada vs duration + convexidad para un shock de +2% en YTM.
# ============================================================
print("\n=== Ejercicio 2: Sensibilidad de Precio ===")
vn = 1000
cupon_pct = 5.0
anios = 10
frecuencia = 2
ytm_base = 4.0
shock_ytm = 0.02  # +2%

# Escribe tu codigo aqui: calcula precio base, precio real post-shock,
# precio aprox con duration solamente, precio aprox con duration+convexidad



# Output esperado:
# Precio base (YTM 4%): $1,081.76
# Precio real (YTM 6%): $925.61
# Precio aprox (solo duration): $999.86 -> Error: $74.25
# Precio aprox (duration+convexidad): $932.29 -> Error: $6.68


# ============================================================
# Ejercicio 3: Curva del Tesoro y Bootstrapping
# Construye la curva spot del Tesoro US a partir de los siguientes
# bonos. Calcula la tasa forward 2Y3Y (entre anio 2 y anio 5).
# Bonos:
#   Bono 1: 6M, cupon 0%, precio $98.50, VN=$100
#   Bono 2: 1Y, cupon 2%, precio $99.20, VN=$100, semestral
#   Bono 3: 2Y, cupon 3%, precio $98.80, VN=$100, semestral
#   Bono 4: 5Y, cupon 4%, precio $97.50, VN=$100, semestral
# ============================================================
print("\n=== Ejercicio 3: Curva del Tesoro US ===")
bonos_curva = [
    (98.50, 100, 0.0, 0.5, 2),   # Bono cupon cero 6M
    (99.20, 100, 2.0, 1.0, 2),   # Bono 1Y
    (98.80, 100, 3.0, 2.0, 2),   # Bono 2Y
    (97.50, 100, 4.0, 5.0, 2),   # Bono 5Y
]

# Escribe tu codigo aqui: bootstrapping de tasas spot



# Output esperado:
# Tasa spot 6M: 3.07%
# Tasa spot 1Y: 2.83%
# Tasa spot 2Y: 3.61%
# Tasa spot 5Y: 4.55%
# Forward rate 2Y3Y: 5.18%


# ============================================================
# Ejercicio 4: Tabla de Amortizacion (3 Sistemas)
# Para un prestamo de $200,000 a 15 anios, tasa 6.5% anual,
# pagos mensuales. Genera las tablas de amortizacion para los
# sistemas frances, aleman y americano. Reporta:
#   - Cuota inicial de cada sistema
#   - Total de intereses pagados en cada sistema
#   - ¿Cual sistema conviene mas al deudor?
# ============================================================
print("\n=== Ejercicio 4: Tabla de Amortizacion ===")
capital_prestamo = 200000
tasa_anual = 6.5
anios_plazo = 15
frecuencia_mensual = 12

# Escribe tu codigo aqui



# Output esperado:
# Sistema Frances:
#   Cuota mensual fija: $1,742.21
#   Total intereses: $113,598.32
# Sistema Aleman:
#   Primera cuota: $2,194.44
#   Ultima cuota: $1,117.13
#   Total intereses: $98,041.67
# Sistema Americano:
#   Cuota mensual (solo intereses): $1,083.33
#   Pago final: $200,000.00
#   Total intereses: $195,000.00
# Conclusion: El sistema aleman minimiza intereses totales


# ============================================================
# Ejercicio 5: Convexity Adjustment Precision
# Para un bono 30Y cupon 3%, compara el ajuste por duration
# solamente vs duration+convexidad para shocks de YTM de -3% a +3%
# (en pasos de 0.5%). ¿Para que magnitud de shock el error de la
# aproximacion lineal (solo duration) supera el 1% del precio real?
# ============================================================
print("\n=== Ejercicio 5: Precision del Convexity Adjustment ===")
vn_30 = 1000
cupon_30 = 3.0
anios_30 = 30
freq_30 = 2
ytm_30_base = 3.5

# Escribe tu codigo aqui



# Output esperado:
# Duration modificada: 18.45
# Convexidad: 430.12
# Shock donde error > 1%: ±1.5%
# Para shock +3%: error lineal $138.50, error con convexidad $4.20
