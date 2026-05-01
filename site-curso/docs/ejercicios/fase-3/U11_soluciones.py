# U11: SOLUCIONES — Funciones: Construyendo tu Librería Financiera

# ============================================================
# Ejercicio 1: Payback
# ============================================================
print("=== Ejercicio 1: Payback ===")

def payback(inversion: float, flujos: list[float]) -> int | None:
    """
    Calcula el número de años para recuperar la inversión inicial.

    Parameters
    ----------
    inversion : float
        Monto de la inversión inicial.
    flujos : list[float]
        Lista de flujos de caja anuales.

    Returns
    -------
    int or None
        Años para recuperar la inversión. None si no se recupera.
    """
    acumulado = 0.0
    for i, flujo in enumerate(flujos, start=1):
        acumulado += flujo
        if acumulado >= inversion:
            return i
    return None

print(f"Payback: {payback(50000, [12000, 15000, 18000, 20000, 22000])} años")
print(f"Payback: {payback(10000, [2000, 3000, 4000])} años")


# ============================================================
# Ejercicio 2: VPN
# ============================================================
print("\n=== Ejercicio 2: VPN ===")

def vpn(inversion: float, tasa: float, flujos: list[float]) -> float:
    """
    Calcula el Valor Presente Neto de una serie de flujos.

    Parameters
    ----------
    inversion : float
        Inversión inicial (positiva).
    tasa : float
        Tasa de descuento (decimal, ej. 0.10 = 10%).
    flujos : list[float]
        Flujos de caja futuros.

    Returns
    -------
    float
        Valor Presente Neto.
    """
    valor_presente = sum(flujo / (1 + tasa) ** (t + 1) for t, flujo in enumerate(flujos))
    return valor_presente - inversion

resultado = vpn(10000, 0.10, [3000, 4000, 5000, 6000])
print(f"VPN: ${resultado:,.2f}")


# ============================================================
# Ejercicio 3: Estadísticas con *args
# ============================================================
print("\n=== Ejercicio 3: Estadísticas con *args ===")

def estadisticas(*rendimientos: float) -> tuple[float, float, float]:
    """
    Calcula promedio, máximo y mínimo de una serie de rendimientos.

    Parameters
    ----------
    *rendimientos : float
        Rendimientos porcentuales.

    Returns
    -------
    tuple[float, float, float]
        (promedio, maximo, minimo).
    """
    if not rendimientos:
        return (0.0, 0.0, 0.0)
    return (sum(rendimientos) / len(rendimientos), max(rendimientos), min(rendimientos))

prom, mx, mn = estadisticas(5.2, -2.1, 3.8, -0.5, 4.2, 1.7)
print(f"Promedio: {prom:.2f}% | Max: {mx:.2f}% | Min: {mn:.2f}%")


# ============================================================
# Ejercicio 4: CAGR y Volatilidad
# ============================================================
print("\n=== Ejercicio 4: CAGR y Volatilidad ===")

def cagr(vi: float, vf: float, anios: int) -> float:
    """
    Calcula la Tasa de Crecimiento Anual Compuesta.

    Parameters
    ----------
    vi : float
        Valor inicial de la inversión.
    vf : float
        Valor final de la inversión.
    anios : int
        Número de años del período.

    Returns
    -------
    float
        CAGR en porcentaje.
    """
    return ((vf / vi) ** (1 / anios) - 1) * 100

def volatilidad_anualizada(rendimientos_diarios: list[float]) -> float:
    """
    Calcula la volatilidad anualizada desde rendimientos diarios porcentuales.

    Parameters
    ----------
    rendimientos_diarios : list[float]
        Rendimientos diarios en porcentaje.

    Returns
    -------
    float
        Volatilidad anualizada en porcentaje.
    """
    n = len(rendimientos_diarios)
    media = sum(rendimientos_diarios) / n
    varianza = sum((r - media) ** 2 for r in rendimientos_diarios) / (n - 1)
    vol_diaria = varianza ** 0.5
    return vol_diaria * (252 ** 0.5)

c = cagr(5000, 12000, 8)
print(f"CAGR: {c:.2f}%")

rendimientos = [0.5, -0.2, 1.8, -0.7, 0.3, 1.2, -0.4, 0.8]
vol = volatilidad_anualizada(rendimientos)
print(f"Volatilidad anualizada: {vol:.2f}%")
