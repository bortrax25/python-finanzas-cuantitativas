# U18: Valoración de Bonos (YTM, Duration)

> **Lectura previa:** [U17: Cálculos financieros](./U17-calculos-financieros.md)
> **Próxima unidad:** [U19: Modelos de riesgo](./U19-modelos-riesgo.md)

## 1. Precio de un bono

```python
def precio_bono(valor_nominal, cupon_pct, ytm, anios, frecuencia=1):
    """Calcula el precio de un bono bullet."""
    cupon = valor_nominal * (cupon_pct / 100) / frecuencia
    periodos = anios * frecuencia
    tasa_periodo = (ytm / 100) / frecuencia

    vp_cupones = sum(cupon / (1 + tasa_periodo)**t for t in range(1, periodos + 1))
    vp_nominal = valor_nominal / (1 + tasa_periodo)**periodos
    return vp_cupones + vp_nominal

# Ejemplo: Bono $1,000, cupón 5%, YTM 4%, 10 años
print(f"Precio: ${precio_bono(1000, 5, 4, 10):.2f}")    # ~$1,081.11
```

## 2. Yield to Maturity (YTM)

```python
def ytm(valor_nominal, precio_mercado, cupon_pct, anios, frecuencia=1):
    """Calcula la YTM por iteración (bisección)."""
    cupon = valor_nominal * (cupon_pct / 100) / frecuencia
    periodos = anios * frecuencia

    r_min, r_max = 0.0, 0.50
    while r_max - r_min > 0.00001:
        r = (r_min + r_max) / 2
        vp = sum(cupon / (1 + r/frecuencia)**t for t in range(1, periodos + 1))
        vp += valor_nominal / (1 + r/frecuencia)**periodos
        if vp > precio_mercado:
            r_min = r
        else:
            r_max = r
    return (r_min + r_max) / 2 * 100
```

## 3. Duration y convexidad

```python
def macaulay_duration(valor_nominal, cupon_pct, ytm, anios, frecuencia=1):
    """Duration de Macaulay — tiempo promedio ponderado de flujos."""
    cupon = valor_nominal * (cupon_pct / 100) / frecuencia
    periodos = anios * frecuencia
    tasa = (ytm / 100) / frecuencia

    vp_total = 0
    t_ponderado = 0
    for t in range(1, periodos + 1):
        flujo = cupon + (valor_nominal if t == periodos else 0)
        vp_flujo = flujo / (1 + tasa)**t
        vp_total += vp_flujo
        t_ponderado += t * vp_flujo
    return (t_ponderado / vp_total) / frecuencia

def modified_duration(d_macaulay, ytm, frecuencia=1):
    """Duration modificada — sensibilidad del precio a cambios en tasa."""
    return d_macaulay / (1 + (ytm / 100) / frecuencia)

# Ejemplo
d_mac = macaulay_duration(1000, 5, 4, 10)
d_mod = modified_duration(d_mac, 4)
print(f"Macaulay Duration: {d_mac:.2f} años")
print(f"Modified Duration: {d_mod:.2f}")
print(f"Si YTM sube 1%, precio baja ~{d_mod:.2f}%")
```

## 4. Ejercicios Propuestos

1. Construye una tabla de precios de bonos para diferentes YTM (2% a 10%).
2. Compara la duration de un bono cupón cero vs un bono con cupón del mismo plazo.
3. Calcula el precio sucio (con intereses corridos) de un bono entre fechas de cupón.
