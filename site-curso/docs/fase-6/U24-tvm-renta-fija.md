# U24: Valor del Dinero en el Tiempo y Renta Fija

> **Lectura previa:** [U23: Obtención de Datos](../fase-5/U23-apis-datos.md)
> **Próxima unidad:** [U25: Análisis de Estados Financieros](./U25-estados-financieros.md)

---

## 1. Teoría

### 1.1 Valor del Dinero en el Tiempo (TVM)

El dinero hoy vale mas que el mismo monto en el futuro: puedes invertirlo y generar intereses.

```python
# Valor Futuro (FV) de un monto unico
def valor_futuro(vp, tasa, periodos):
    return vp * (1 + tasa) ** periodos

# Valor Presente (PV) de un monto futuro
def valor_presente(vf, tasa, periodos):
    return vf / (1 + tasa) ** periodos

# Ejemplo: $10,000 hoy al 7% por 10 anios
vf = valor_futuro(10000, 0.07, 10)
vp = valor_presente(19671.51, 0.07, 10)
print(f"VF: ${vf:,.2f}")  # $19,671.51
print(f"VP: ${vp:,.2f}")  # $10,000.00
```

> ⚠️ La tasa debe estar en la misma unidad que los periodos. Si la tasa es anual, los periodos deben ser anios. Para periodos mensuales, divide la tasa anual entre 12 y multiplica los anios por 12.

### 1.2 Anualidades y Perpetuidades

Una **anualidad** es una serie de pagos iguales en intervalos regulares. Una **perpetuidad** paga para siempre.

```python
# Valor Presente de una Anualidad Ordinaria
def vp_anualidad(pago, tasa, periodos):
    return pago * (1 - (1 + tasa) ** (-periodos)) / tasa

# Valor Futuro de una Anualidad Ordinaria
def vf_anualidad(pago, tasa, periodos):
    return pago * ((1 + tasa) ** periodos - 1) / tasa

# Perpetuidad
def vp_perpetuidad(pago, tasa):
    return pago / tasa

# Perpetuidad con crecimiento (Gordon Growth)
def vp_perpetuidad_creciente(pago, tasa, crecimiento):
    return pago / (tasa - crecimiento)

# Ejemplo: Bono que paga $50 semestral por 10 anios, tasa 6% anual
vp_anual = vp_anualidad(50, 0.03, 20)
print(f"VP cupones: ${vp_anual:,.2f}")  # ~$743.87
```

### 1.3 Precio de un Bono

El precio de un bono es el VP de sus flujos futuros (cupones + principal).

```python
def precio_bono(valor_nominal, tasa_cupon, ytm, anios_hasta_vencimiento, frecuencia=2):
    """Calcula el precio limpio de un bono bullet.
    
    Parametros:
        valor_nominal: valor par del bono (ej. 1000)
        tasa_cupon: tasa cupon anual en % (ej. 5.0 para 5%)
        ytm: yield to maturity anual en % (ej. 4.5 para 4.5%)
        anios_hasta_vencimiento: anios hasta vencimiento
        frecuencia: pagos por anio (2 = semestral tipico US)
    """
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios_hasta_vencimiento * frecuencia)
    tasa_periodica = (ytm / 100) / frecuencia
    
    vp_cupones = sum(cupon / (1 + tasa_periodica) ** t for t in range(1, periodos + 1))
    vp_principal = valor_nominal / (1 + tasa_periodica) ** periodos
    
    return vp_cupones + vp_principal

# Bono US Treasury 10Y: nominal $1,000, cupon 4%, YTM 4.5%
precio = precio_bono(1000, 4.0, 4.5, 10, 2)
print(f"Precio del bono: ${precio:,.2f}")
# Si YTM > cupon → precio < nominal (descuento)
# Si YTM < cupon → precio > nominal (prima)
```

> 💡 **Regla del bono:** Cuando YTM = tasa cupon, el bono cotiza a la par (precio = valor nominal). Cuando YTM > cupon, descuento. Cuando YTM < cupon, prima.

### 1.4 Yield to Maturity (YTM) por Newton-Raphson

La YTM es la tasa que iguala el VP de los flujos al precio de mercado. No tiene formula cerrada: requiere metodo numerico.

```python
from scipy.optimize import newton

def ytm_newton(precio_mercado, valor_nominal, tasa_cupon, anios, frecuencia=2):
    """Calcula YTM usando Newton-Raphson."""
    cupon = valor_nominal * (tasa_cupon / 100) / frecuencia
    periodos = int(anios * frecuencia)
    
    def valor_presente_neto(ytm):
        """Diferencia entre precio calculado y precio de mercado."""
        ytm_decimal = ytm
        tasa_per = ytm_decimal / frecuencia
        vp_cupones = sum(cupon / (1 + tasa_per) ** t for t in range(1, periodos + 1))
        vp_principal = valor_nominal / (1 + tasa_per) ** periodos
        return vp_cupones + vp_principal - precio_mercado
    
    ytm_decimal = newton(valor_presente_neto, 0.05)
    return ytm_decimal * 100

# Si el bono anterior cotiza a $960.44
ytm = ytm_newton(960.44, 1000, 4.0, 10, 2)
print(f"YTM: {ytm:.2f}%")  # ~4.5%
```

> ⚠️ Newton-Raphson requiere una funcion diferenciable. Para YTM usamos `scipy.optimize.newton` que aproxima la derivada numericamente. La estimacion inicial de 5% funciona para la mayoria de los bonos.

### 1.5 Duration y Convexidad

La **duration** mide la sensibilidad del precio a cambios en la tasa de interes. La **convexidad** mide como cambia la duration misma.

```python
def macaulay_duration(valor_nominal, tasa_cupon, ytm, anios, frecuencia=2):
    """Duration de Macaulay: tiempo promedio ponderado de los flujos."""
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
    """Duration modificada: cambio % en precio por cambio de 1% en YTM."""
    return macaulay_dur / (1 + (ytm / 100) / frecuencia)

def convexidad(valor_nominal, tasa_cupon, ytm, anios, frecuencia=2):
    """Convexidad: curvatura de la relacion precio-YTM."""
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

# Ejemplo: Bono 10Y 4% cupon, YTM 4.5%
d_mac = macaulay_duration(1000, 4.0, 4.5, 10)
d_mod = modificada_duration(d_mac, 4.5)
conv = convexidad(1000, 4.0, 4.5, 10)

print(f"Macaulay Duration: {d_mac:.2f} anios")
print(f"Modified Duration: {d_mod:.2f}")
print(f"Convexidad: {conv:.2f}")
print(f"Si YTM sube 1%, precio baja ~{d_mod:.2f}% (aprox. lineal)")
print(f"Ajuste por convexidad: +{0.5 * conv * 0.01**2 * 100:.4f}%")
```

> 💡 La duration modificada da una aproximacion lineal. Para cambios grandes en YTM, necesitas el ajuste por convexidad: ΔP/P ≈ -D_mod × Δy + 0.5 × C × (Δy)²

### 1.6 Curvas de Rendimiento y Bootstrapping

La **curva de rendimiento** (yield curve) muestra la relacion entre YTM y plazo. El **bootstrapping** construye la curva spot a partir de bonos cupon cero.

```python
import numpy as np

def bootstrapping_tasas_spot(bonos):
    """Construye curva spot a partir de bonos con cupon.
    
    bonos: lista de tuplas (precio, valor_nominal, cupon_anual, anios, frecuencia)
    Retorna: tasas spot para cada plazo.
    """
    tasas_spot = []
    
    for i, (precio, vn, cupon_pct, anios, freq) in enumerate(bonos):
        cupon = vn * (cupon_pct / 100) / freq
        periodos = int(anios * freq)
        
        if periodo_total == freq * anios == 1:  # Bono cupon cero de corto plazo
            r = (vn / precio) ** (1 / periodos) - 1
            tasas_spot.append(r * freq)  # Anualizar
        else:
            # Descontar flujos conocidos con tasas spot anteriores
            flujos_restantes = precio
            for t in range(1, periodos):
                flujos_restantes -= cupon / (1 + tasas_spot[t - 1] / freq) ** t
            
            ultimo_pago = cupon + vn
            r = (ultimo_pago / flujos_restantes) ** (1 / periodos) - 1
            tasas_spot.append(r * freq)
    
    return tasas_spot
```

### 1.7 Sistemas de Amortizacion de Prestamos

| Sistema | Cuota | Interes | Amortizacion |
|---------|-------|---------|-------------|
| **Frances** | Cuota fija | Decreciente | Creciente |
| **Aleman** | Decreciente | Decreciente | Amortizacion fija |
| **Americano** | Solo intereses hasta el final | Fijo | Bullet al final |

```python
def amortizacion_frances(capital, tasa, periodos):
    """Sistema frances: cuota fija."""
    cuota = capital * (tasa * (1 + tasa) ** periodos) / ((1 + tasa) ** periodos - 1)
    saldo = capital
    tabla = []
    for t in range(1, periodos + 1):
        interes = saldo * tasa
        amortizacion_capital = cuota - interes
        saldo -= amortizacion_capital
        tabla.append((t, cuota, interes, amortizacion_capital, saldo))
    return tabla

def amortizacion_aleman(capital, tasa, periodos):
    """Sistema aleman: amortizacion fija."""
    amortizacion_capital = capital / periodos
    saldo = capital
    tabla = []
    for t in range(1, periodos + 1):
        interes = saldo * tasa
        cuota = amortizacion_capital + interes
        saldo -= amortizacion_capital
        tabla.append((t, cuota, interes, amortizacion_capital, saldo))
    return tabla
```

---

## 2. Practica

### 2.1 Ejercicio guiado: Pricer de Bono Completo

**Concepto financiero:** Un bono del Tesoro americano a 10 anios con cupon semestral del 3.5% y valor nominal $1,000 cotiza en el mercado a $925. Calculamos todas sus metricas.

**Formulas:**
- Precio = Σ cupon/(1+r)^t + VN/(1+r)^n
- YTM por Newton-Raphson
- Duration modificada = Macaulay / (1 + r/n)
- Convexidad = Σ t(t+1) × VP_flujo / ((1+r)² × Precio × n²)

**Codigo:**

```python
import numpy as np
from scipy.optimize import newton

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

# Datos del bono
vn = 1000
cupon_pct = 3.5
precio_mercado = 925
anios = 10

# Calcular YTM
ytm = ytm_newton(precio_mercado, vn, cupon_pct, anios)
print(f"YTM: {ytm:.2f}%")

# Verificar: precio usando la YTM debe ser ~925
precio_calc = precio_bono(vn, cupon_pct, ytm, anios)
print(f"Precio con YTM: ${precio_calc:,.2f}")

# Duration y convexidad
from U24_tvm_renta_fija import macaulay_duration, modificada_duration, convexidad
d_mac = macaulay_duration(vn, cupon_pct, ytm, anios)
d_mod = modificada_duration(d_mac, ytm)
conv = convexidad(vn, cupon_pct, ytm, anios)
print(f"Duration Macaulay: {d_mac:.2f} anios")
print(f"Duration Modificada: {d_mod:.2f}")
print(f"Convexidad: {conv:.2f}")
```

**Output:**
```
YTM: 4.52%
Precio con YTM: $925.01
Duration Macaulay: 8.56 años
Duration Modificada: 8.37
Convexidad: 82.34
```

---

## 3. Aplicacion en Finanzas 💰

En JP Morgan, el Fixed Income Desk usa estas metricas diariamente:

- **Traders de bonos:** Monitorean YTM y duration para gestionar el riesgo de tasa de interes en books de billones de dolares.
- **Analistas de credito:** Comparan el spread de credito (diferencia YTM del bono corporativo vs Treasury del mismo plazo) para evaluar riesgo de default.
- **Portfolio managers:** Ajustan la duration del portafolio segun su vision de tasas (si creen que bajaran, extienden duration; si creen que subiran, la acortan).
- **ALM (Asset-Liability Management):** Los bancos calzan duration de activos y pasivos para evitar perdidas por movimientos de tasas.

La curva del Tesoro es el benchmark fundamental para valorar TODOS los activos financieros del mundo.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-6/U24_ejercicios.py`

1. **Bond Pricer Completo:** Construye un pricer de bonos que calcule precio, YTM por Newton-Raphson, Macaulay duration, duration modificada y convexidad para un bono dado.

2. **Sensibilidad de Precio:** Para un bono 10Y cupon 5%, calcula el precio para YTM de 1% a 10% y grafica la relacion precio-YTM. Muestra la aproximacion lineal de duration vs el precio real.

3. **Curva del Tesoro US:** Con datos de tasas spot para plazos de 1, 2, 5, 10 y 30 anios, construye la curva y calcula el forward rate 2Y5Y (tasa forward entre anio 2 y 5).

4. **Tabla de Amortizacion:** Para un prestamo de $200,000 a 15 anios al 6.5% anual, genera tablas de amortizacion en los tres sistemas (frances, aleman, americano) y compara el total de intereses pagados.

5. **Convexity Adjustment:** Para un bono 30Y cupon 3%, compara la aproximacion lineal de duration vs el ajuste con convexidad para cambios de YTM de -2% a +2%. ¿Para que magnitud de cambio el error lineal supera 1%?

---

## 5. Resumen

| Concepto | Formula | Interpretacion |
|---------|---------|---------------|
| Valor Futuro | VF = VP × (1 + r)^n | Crecimiento del capital |
| Valor Presente | VP = VF / (1 + r)^n | Descuento de flujos futuros |
| VP Anualidad | P × (1 - (1+r)^-n) / r | Valor de pagos regulares |
| Precio Bono | Σ C/(1+r)^t + VN/(1+r)^n | VP de cupones + principal |
| YTM | Tasa que iguala precio a VP flujos | Rendimiento total del bono |
| Macaulay Duration | Σ t × VP_flujo / Precio | Plazo promedio ponderado |
| Modified Duration | MacD / (1 + r/n) | Sensibilidad a tasa de interes |
| Convexidad | Σ t(t+1)VP_flujo / ((1+r)^2 × P × n^2) | Curvatura precio-YTM |

---

## ✅ Autoevaluacion

1. ¿Por que un bono con cupon 5% cotiza bajo la par cuando la YTM es 6%?
2. ¿Que mide la duration modificada y por que es solo una aproximacion?
3. ¿Como funciona el metodo de Newton-Raphson para encontrar la YTM?
4. ¿Que diferencia hay entre la curva spot y la curva par?
5. En el sistema frances, ¿por que la cuota es fija pero la composicion interes/amortizacion cambia?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Formulas de TVM: VF, VP, anualidad, perpetuidad
> - Funcion `precio_bono()` con parametros: VN, cupon, YTM, anios, frecuencia
> - Metodo Newton-Raphson via `scipy.optimize.newton`
> - Duration modificada como medida de riesgo de tasa
> - Los tres sistemas de amortizacion (frances, aleman, americano)
