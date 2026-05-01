# 📝 Ejercicios: U15 — Fase 4

> [← Volver a ejercicios Fase 4](index.md) | [📥 Descargar .py](U15_ejercicios)

---

```python
# U15: EJERCICIOS — Clases y Objetos: Modelando Instrumentos Financieros

# ============================================================
# Ejercicio 1: Clase Accion con P&L
# Crea la clase Accion con:
#   - __init__(self, ticker, precio_compra, cantidad)
#   - actualizar_precio(self, nuevo_precio)
#   - valor_mercado(self) -> float
#   - costo(self) -> float
#   - ganancia_perdida(self) -> float
#   - rendimiento(self) -> float  (porcentaje)
#   - __str__(self) -> str con formato: "TICKER: cant × $precio = $valor | P&L: $pnl (rend%)"
# Prueba con AAPL (precio_compra=150, cant=100) y actualiza precio a 175.
# ============================================================
print("=== Ejercicio 1: Clase Accion ===")

# Escribe tu código aquí



# Output esperado:
# AAPL: 100 × $175.00 = $17,500.00 | P&L: $2,500.00 (16.67%)


# ============================================================
# Ejercicio 2: Clase Bono con cupones y properties
# Crea la clase Bono con:
#   - __init__(self, valor_nominal, tasa_cupon, precio_mercado, vencimiento, frecuencia=2)
#   - cupon_por_periodo(self) -> float
#   - total_cupones(self) -> float
#   - rendimiento_actual (property) -> float: (cupon_anual / precio_mercado) * 100
#   - prima_descuento (property) -> str: "Sobre par", "Bajo par", "A la par"
#   - __repr__(self) -> str: Bono(VN=..., cupon=...%, venc=..., precio=...)
# Prueba: Bono con VN=1000, cupon=6%, precio=950, vencimiento=10 años.
# ============================================================
print("\\n=== Ejercicio 2: Clase Bono ===")

# Escribe tu código aquí



# Output esperado:
# Bono(VN=1000, cupon=6.0%, venc=10, precio=950)
# Cupón por periodo: $30.00
# Total cupones: $600.00
# Rendimiento actual: 6.32%
# Clasificación: Bajo par (descuento)


# ============================================================
# Ejercicio 3: Clase Portafolio con estadísticas avanzadas
# Crea la clase Portafolio con:
#   - __init__(self, nombre)
#   - agregar(self, accion: Accion)
#   - eliminar(self, ticker: str)
#   - valor_total(self) -> float
#   - pnl_total(self) -> float
#   - rendimiento_ponderado(self) -> float: (PnL_total / costo_total) * 100
#   - concentracion_maxima(self) -> tuple[str, float]: (ticker, peso_porcentual)
#   - resumen(self) -> str: tabla formateada con todos los activos
# Crea un portafolio con 3 acciones, actualiza precios y muestra resumen.
# ============================================================
print("\\n=== Ejercicio 3: Clase Portafolio ===")
# Reutiliza la clase Accion del Ejercicio 1

# Escribe tu código aquí



# Output esperado:
# Portafolio: Mi Fondo
# Ticker    Cant      Precio        Valor        P&L     Peso
# ----------------------------------------------------------------
# AAPL        150 $   180.00 $   27,000.00 $   4,500.00   40.91%
# MSFT         80 $   340.00 $   27,200.00 $   4,800.00   41.21%
# TSLA         40 $   295.00 $   11,800.00 $   -200.00   17.88%
# ----------------------------------------------------------------
# Valor Total: $66,000.00 | P&L: $9,100.00 | Rend: 15.99%
# Concentración máxima: MSFT (41.21%)


# ============================================================
# Ejercicio 4: Clase Prestamo con tabla de amortización
# Crea la clase Prestamo con sistema de amortización francés:
#   - __init__(self, capital, tasa_anual, plazo_años)
#   - tasa_mensual (property) -> float: tasa_anual / 12
#   - numero_cuotas (property) -> int: plazo_años * 12
#   - cuota_mensual(self) -> float: fórmula francesa
#     cuota = capital * (tasa_mensual * (1 + tasa_mensual)^n) / ((1 + tasa_mensual)^n - 1)
#   - tabla_amortizacion(self, mostrar: int = 5) -> list[dict]:
#     Retorna lista con {"periodo", "cuota", "interes", "amortizacion", "saldo"}
#     Muestra solo las primeras `mostrar` cuotas y la última.
# Prueba: Préstamo de $200,000 al 8% anual a 20 años.
# ============================================================
print("\\n=== Ejercicio 4: Clase Prestamo ===")

# Escribe tu código aquí



# Output esperado:
# Préstamo: $200,000.00 | Tasa: 8.00% | Plazo: 20 años
# Cuota mensual: $1,672.88
# Periodo    Cuota      Interés    Amortización    Saldo
# ------------------------------------------------------------
# 1          $1,672.88  $1,333.33  $339.55         $199,660.45
# 2          $1,672.88  $1,331.07  $341.81         $199,318.64
# 3          $1,672.88  $1,328.79  $344.09         $198,974.55
# ...
# 240        $1,672.88  $11.09     $1,661.79       $0.00
```

---

> [📥 Descargar archivo .py](U15_ejercicios) &nbsp;|&nbsp; [← Volver a ejercicios Fase 4](index.md)
