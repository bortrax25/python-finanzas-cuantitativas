# ✅ Soluciones: U24 — Fase 6

> [← Volver a ejercicios Fase 6](index.md) | [📥 Descargar .py](U24_soluciones)

---

```python
# U24: SOLUCIONES — Valor del Dinero en el Tiempo y Renta Fija

import numpy as np
from scipy.optimize import newton

# ============================================================
# Funciones auxiliares (reutilizables en todos los ejercicios)
# ============================================================

def precio_bono(valor_nominal, tasa_cupon, ytm, anios, frecuencia=2):
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios * frecuencia)
    tasa_per = (ytm / 100) / frecuencia
    vp_cupones = sum(cupon / (1 + tasa_per) ** t for t in range(1, periodos + 1))
    vp_principal = valor_nominal / (1 + tasa_per) ** periodos
    return vp_cupones + vp_principal

def ytm_newton(precio_mercado, valor_nominal, tasa_cupon, anios, frecuencia=2):
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios * frecuencia)
    def vpn(ytm_dec):
        tp = ytm_dec / frecuencia
        vp = sum(cupon / (1 + tp) ** t for t in range(1, periodos + 1))
        vp += valor_nominal / (1 + tp) ** periodos
        return vp - precio_mercado
    return newton(vpn, 0.05) * 100

def macaulay_duration(valor_nominal, tasa_cupon, ytm, anios, frecuencia=2):
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios * frecuencia)
    tasa_per = (ytm / 100) / frecuencia
    vp_total = 0.0
    t_ponderado = 0.0
    for t in range(1, periodos + 1):
        flujo = cupon + (valor_nominal if t == periodos else 0)
        vp_flujo = flujo / (1 + tasa_per) ** t
        vp_total += vp_flujo
        t_ponderado += t * vp_flujo
    return (t_ponderado / vp_total) / frecuencia

def modificada_duration(macaulay_dur, ytm, frecuencia=2):
    return macaulay_dur / (1 + (ytm / 100) / frecuencia)

def convexidad(valor_nominal, tasa_cupon, ytm, anios, frecuencia=2):
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios * frecuencia)
    tasa_per = (ytm / 100) / frecuencia
    precio = precio_bono(valor_nominal, tasa_cupon, ytm, anios, frecuencia)
    convexidad_total = 0.0
    for t in range(1, periodos + 1):
        flujo = cupon + (valor_nominal if t == periodos else 0)
        vp_flujo = flujo / (1 + tasa_per) ** t
        convexidad_total += t * (t + 1) * vp_flujo
    convexidad_total = convexidad_total / ((1 + tasa_per) ** 2 * precio)
    return convexidad_total / (frecuencia ** 2)


# ============================================================
# Ejercicio 1: Bond Pricer Completo
# ============================================================
print("=== Ejercicio 1: Bond Pricer Completo ===")
valor_nominal = 1000
tasa_cupon_pct = 5.0
anios_vencimiento = 8
frecuencia_pago = 2
precio_mercado = 980

ytm = ytm_newton(precio_mercado, valor_nominal, tasa_cupon_pct, anios_vencimiento, frecuencia_pago)
precio = precio_bono(valor_nominal, tasa_cupon_pct, ytm, anios_vencimiento, frecuencia_pago)
d_mac = macaulay_duration(valor_nominal, tasa_cupon_pct, ytm, anios_vencimiento, frecuencia_pago)
d_mod = modificada_duration(d_mac, ytm, frecuencia_pago)
conv = convexidad(valor_nominal, tasa_cupon_pct, ytm, anios_vencimiento, frecuencia_pago)

print(f"Precio del bono (YTM {ytm:.2f}%): ${precio:,.2f}")
print(f"YTM (Newton-Raphson): {ytm:.2f}%")
print(f"Macaulay Duration: {d_mac:.2f} anios")
print(f"Modified Duration: {d_mod:.2f}")
print(f"Convexidad: {conv:.2f}")


# ============================================================
# Ejercicio 2: Sensibilidad de Precio y Convexity Adjustment
# ============================================================
print("\\n=== Ejercicio 2: Sensibilidad de Precio ===")
vn = 1000
cupon_pct = 5.0
anios = 10
frecuencia = 2
ytm_base = 4.0
shock_ytm = 0.02

precio_base = precio_bono(vn, cupon_pct, ytm_base, anios, frecuencia)
precio_shock = precio_bono(vn, cupon_pct, ytm_base + shock_ytm * 100, anios, frecuencia)

d_mac_base = macaulay_duration(vn, cupon_pct, ytm_base, anios, frecuencia)
d_mod_base = modificada_duration(d_mac_base, ytm_base, frecuencia)
conv_base = convexidad(vn, cupon_pct, ytm_base, anios, frecuencia)

delta_ytm = shock_ytm
precio_aprox_dur = precio_base * (1 - d_mod_base * delta_ytm)
precio_aprox_dur_conv = precio_base * (1 - d_mod_base * delta_ytm + 0.5 * conv_base * delta_ytm ** 2)

error_dur = abs(precio_shock - precio_aprox_dur)
error_dur_conv = abs(precio_shock - precio_aprox_dur_conv)

print(f"Precio base (YTM {ytm_base}%): ${precio_base:,.2f}")
print(f"Precio real (YTM {ytm_base + shock_ytm * 100}%): ${precio_shock:,.2f}")
print(f"Precio aprox (solo duration): ${precio_aprox_dur:,.2f} -> Error: ${error_dur:,.2f}")
print(f"Precio aprox (duration+convexidad): ${precio_aprox_dur_conv:,.2f} -> Error: ${error_dur_conv:,.2f}")


# ============================================================
# Ejercicio 3: Curva del Tesoro y Bootstrapping
# ============================================================
print("\\n=== Ejercicio 3: Curva del Tesoro US ===")
bonos_curva = [
    (98.50, 100, 0.0, 0.5, 2),
    (99.20, 100, 2.0, 1.0, 2),
    (98.80, 100, 3.0, 2.0, 2),
    (97.50, 100, 4.0, 5.0, 2),
]

tasas_spot = []

for i, (precio, vn, cupon_pct, anios_bono, freq) in enumerate(bonos_curva):
    cupon = vn * (cupon_pct / 100) / freq
    periodos = int(anios_bono * freq)
    
    if periodos == 1:
        # Bono cupon cero
        r_per = (vn / precio) - 1
        r_anual = (1 + r_per) ** freq - 1
        tasas_spot.append(r_anual)
    else:
        # Descontar flujos conocidos con tasas spot ya calculadas
        flujo_restante = precio
        for t in range(1, periodos):
            tasa_descuento = tasas_spot[t - 1] if t - 1 < len(tasas_spot) else 0.03
            flujo_restante -= cupon / (1 + tasa_descuento) ** (t / freq)
        
        # El ultimo flujo incluye el principal
        ultimo_pago = cupon + vn
        r_per = (ultimo_pago / flujo_restante) ** (1 / periodos) - 1
        r_anual = (1 + r_per) ** freq - 1
        tasas_spot.append(r_anual)

for j, (_, _, _, plazo, _) in enumerate(bonos_curva):
    print(f"Tasa spot {plazo}Y: {tasas_spot[j]:.2%}")

# Forward rate 2Y3Y (entre anio 2 y 5)
# (1 + s5)^5 = (1 + s2)^2 * (1 + f_2_5)^3
idx_2y = 2  # 2Y spot
idx_5y = 3  # 5Y spot
forward_2y3y = ((1 + tasas_spot[idx_5y]) ** 5 / (1 + tasas_spot[idx_2y]) ** 2) ** (1 / 3) - 1
print(f"Forward rate 2Y3Y: {forward_2y3y:.2%}")


# ============================================================
# Ejercicio 4: Tabla de Amortizacion (3 Sistemas)
# ============================================================
print("\\n=== Ejercicio 4: Tabla de Amortizacion ===")
capital_prestamo = 200000
tasa_anual = 6.5
anios_plazo = 15
frecuencia_mensual = 12

tasa_mensual = (tasa_anual / 100) / frecuencia_mensual
periodos = anios_plazo * frecuencia_mensual

# Sistema Frances: cuota fija
cuota_frances = capital_prestamo * (tasa_mensual * (1 + tasa_mensual) ** periodos) / ((1 + tasa_mensual) ** periodos - 1)
saldo = capital_prestamo
intereses_frances = 0.0
for t in range(1, periodos + 1):
    interes = saldo * tasa_mensual
    amortizacion = cuota_frances - interes
    saldo -= amortizacion
    intereses_frances += interes

# Sistema Aleman: amortizacion fija
amortizacion_aleman = capital_prestamo / periodos
saldo = capital_prestamo
intereses_aleman = 0.0
primera_cuota_aleman = 0.0
ultima_cuota_aleman = 0.0
for t in range(1, periodos + 1):
    interes = saldo * tasa_mensual
    cuota = amortizacion_aleman + interes
    if t == 1:
        primera_cuota_aleman = cuota
    if t == periodos:
        ultima_cuota_aleman = cuota
    saldo -= amortizacion_aleman
    intereses_aleman += interes

# Sistema Americano: solo intereses hasta el final
cuota_americana = capital_prestamo * tasa_mensual
intereses_americano = cuota_americana * periodos
pago_final_americano = capital_prestamo

print("Sistema Frances:")
print(f"  Cuota mensual fija: ${cuota_frances:,.2f}")
print(f"  Total intereses: ${intereses_frances:,.2f}")
print("Sistema Aleman:")
print(f"  Primera cuota: ${primera_cuota_aleman:,.2f}")
print(f"  Ultima cuota: ${ultima_cuota_aleman:,.2f}")
print(f"  Total intereses: ${intereses_aleman:,.2f}")
print("Sistema Americano:")
print(f"  Cuota mensual (solo intereses): ${cuota_americana:,.2f}")
print(f"  Pago final: ${pago_final_americano:,.2f}")
print(f"  Total intereses: ${intereses_americano:,.2f}")

print("Conclusion: El sistema aleman minimiza intereses totales")


# ============================================================
# Ejercicio 5: Convexity Adjustment Precision
# ============================================================
print("\\n=== Ejercicio 5: Precision del Convexity Adjustment ===")
vn_30 = 1000
cupon_30 = 3.0
anios_30 = 30
freq_30 = 2
ytm_30_base = 3.5

d_mac_30 = macaulay_duration(vn_30, cupon_30, ytm_30_base, anios_30, freq_30)
d_mod_30 = modificada_duration(d_mac_30, ytm_30_base, freq_30)
conv_30 = convexidad(vn_30, cupon_30, ytm_30_base, anios_30, freq_30)
precio_base_30 = precio_bono(vn_30, cupon_30, ytm_30_base, anios_30, freq_30)

print(f"Duration modificada: {d_mod_30:.2f}")
print(f"Convexidad: {conv_30:.2f}")

# Probar shocks de -3% a +3% en pasos de 0.5%
shocks = np.arange(-0.03, 0.035, 0.005)
umbral_superado = None

for shock in shocks:
    precio_real = precio_bono(vn_30, cupon_30, ytm_30_base + shock * 100, anios_30, freq_30)
    precio_aprox_lin = precio_base_30 * (1 - d_mod_30 * shock)
    precio_aprox_con = precio_base_30 * (1 - d_mod_30 * shock + 0.5 * conv_30 * shock ** 2)
    error_lin_pct = abs(precio_real - precio_aprox_lin) / precio_real * 100
    
    if error_lin_pct > 1.0 and umbral_superado is None:
        umbral_superado = abs(shock)
    
    if abs(shock) == 0.015:
        error_lin_15 = abs(precio_real - precio_aprox_lin)
        error_con_15 = abs(precio_real - precio_aprox_con)
    if abs(shock - 0.03) < 0.001 or abs(shock + 0.03) < 0.001:
        error_lin_30 = abs(precio_real - precio_aprox_lin)
        error_con_30 = abs(precio_real - precio_aprox_con)

print(f"Shock donde error > 1%: {umbral_superado:.1%}")
print(f"Para shock +3%: error lineal ${error_lin_30:,.2f}, error con convexidad ${error_con_30:,.2f}")
```

---

> [📥 Descargar archivo .py](U24_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 6](index.md)
