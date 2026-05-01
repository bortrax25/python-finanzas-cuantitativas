# ✅ Soluciones: U13 — Fase 3

> [← Volver a ejercicios Fase 3](index.md) | [📥 Descargar .py](U13_soluciones)

---

```python
# U13: SOLUCIONES — Módulos, Paquetes y Arquitectura de Proyecto

# ============================================================
# Ejercicio 1: Submódulo riesgo.py
# ============================================================
print("=== Ejercicio 1: Submódulo riesgo.py ===")

def sharpe_ratio(rendimiento: float, rf: float, volatilidad: float) -> float:
    return (rendimiento - rf) / volatilidad

def var_historico(rendimientos: list[float], confianza: float = 0.95) -> float:
    ordenados = sorted(rendimientos)
    indice = int(len(ordenados) * (1 - confianza))
    return -ordenados[indice]

def volatilidad_anualizada(rendimientos_diarios: list[float]) -> float:
    n = len(rendimientos_diarios)
    media = sum(rendimientos_diarios) / n
    varianza = sum((r - media) ** 2 for r in rendimientos_diarios) / (n - 1)
    vol_diaria = varianza ** 0.5
    return vol_diaria * (252 ** 0.5)

print(f"Sharpe: {sharpe_ratio(12, 4, 18):.2f}")
rendimientos = [0.5, -0.2, 1.8, -0.7, 0.3, 1.2, -0.4, 0.8, -1.1, 0.6,
                1.5, -0.9, 0.4, 2.1, -0.5, 0.7, -0.3, 1.0, -0.8, 0.9]
print(f"VaR 95%: {var_historico(rendimientos):.2f}%")
print(f"Volatilidad anualizada: {volatilidad_anualizada(rendimientos):.2f}%")


# ============================================================
# Ejercicio 2: if __name__ == "__main__"
# ============================================================
print("\\n=== Ejercicio 2: Entry Point ===")

def valor_futuro(capital: float, tasa: float, anios: int) -> float:
    return capital * (1 + tasa / 100) ** anios

def cuota_prestamo(monto: float, tasa_anual: float, plazo_meses: int) -> float:
    i = (tasa_anual / 100) / 12
    return monto * (i * (1 + i) ** plazo_meses) / ((1 + i) ** plazo_meses - 1)

if __name__ == "__main__":
    print("=== Probando funciones financieras ===")
    vf = valor_futuro(10000, 8, 10)
    print(f"VF $10,000 al 8% por 10 años = ${vf:,.2f}")
    cuota = cuota_prestamo(200000, 10, 240)
    print(f"Cuota préstamo $200K al 10% a 240 meses = ${cuota:,.2f}")


# ============================================================
# Ejercicio 3: Estructura de Paquete
# ============================================================
print("\\n=== Ejercicio 3: Estructura de Paquete ===")

estructura = r"""quantlib/
├── __init__.py
├── pricing/
│   ├── __init__.py
│   ├── bonos.py
│   └── acciones.py
├── riesgo/
│   ├── __init__.py
│   └── metricas.py
└── datos/
    ├── __init__.py
    └── io.py"""
print(estructura)


# ============================================================
# Ejercicio 4: Uso del Paquete
# ============================================================
print("\\n=== Ejercicio 4: Uso del Paquete ===")

print("Forma 1 (import módulo):")
print("  import quantlib.riesgo.metricas as riesgo")
print("  sharpe = riesgo.sharpe_ratio(12, 4, 18)")

print("Forma 2 (from ... import función):")
print("  from quantlib.riesgo.metricas import sharpe_ratio")
print("  sharpe = sharpe_ratio(12, 4, 18)")

print("Forma 3 (from ... import *):")
print("  from quantlib import sharpe_ratio")
print("  sharpe = sharpe_ratio(12, 4, 18)")

print(f"\\nUsando la función real: Sharpe = {sharpe_ratio(12, 4, 18):.2f}")
```

---

> [📥 Descargar archivo .py](U13_soluciones) &nbsp;|&nbsp; [← Volver a ejercicios Fase 3](index.md)
