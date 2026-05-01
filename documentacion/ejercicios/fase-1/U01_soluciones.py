# U01: SOLUCIONES — Variables y Tipos de Datos

# ============================================================
# Ejercicio 1: Interés compuesto
# ============================================================
print("=== Ejercicio 1: Interés Compuesto ===")
capital_e1 = 5000
tasa_anual_e1 = 8
tiempo_e1 = 5

tasa_decimal = tasa_anual_e1 / 100
monto_final = capital_e1 * (1 + tasa_decimal) ** tiempo_e1

print(f"Capital inicial: ${capital_e1:,.2f}")
print(f"Tasa anual: {tasa_anual_e1}%")
print(f"Tiempo: {tiempo_e1} años")
print(f"Monto final: ${monto_final:,.2f}")


# ============================================================
# Ejercicio 2: Conversor de monedas
# ============================================================
print("\n=== Ejercicio 2: Conversor de Monedas ===")
cantidad_usd = 1000
tipo_cambio_pen = 3.75
tipo_cambio_mxn = 17.20
tipo_cambio_cop = 3900.00

monto_pen = cantidad_usd * tipo_cambio_pen
monto_mxn = cantidad_usd * tipo_cambio_mxn
monto_cop = cantidad_usd * tipo_cambio_cop

print(f"${cantidad_usd:,.2f} USD equivale a:")
print(f"S/ {monto_pen:,.2f} PEN")
print(f"$ {monto_mxn:,.2f} MXN")
print(f"$ {monto_cop:,.2f} COP")


# ============================================================
# Ejercicio 3: Perfil del inversionista
# ============================================================
print("\n=== Ejercicio 3: Perfil del Inversionista ===")
nombre = "Carlos Martínez"
edad = 28
capital = 10000.00
meta_rendimiento = 12.5
activo = True

print("=== Perfil del Inversionista ===")
print(f"Nombre: {nombre}")
print(f"Edad: {edad}")
print(f"Capital inicial: ${capital:,.2f}")
print(f"Meta de rendimiento: {meta_rendimiento}%")
print(f"Activo: {activo}")


# ============================================================
# Ejercicio 4: Comisión del broker
# ============================================================
print("\n=== Ejercicio 4: Comisión del Broker ===")
monto_transaccion = 25000
comision_pct = 0.5

comision = monto_transaccion * (comision_pct / 100)
monto_neto = monto_transaccion - comision

print(f"Monto de transacción: ${monto_transaccion:,.2f}")
print(f"Comisión ({comision_pct}%): ${comision:,.2f}")
print(f"Monto neto: ${monto_neto:,.2f}")
