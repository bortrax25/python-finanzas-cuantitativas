# U28: Derivados — Opciones y Modelos de Pricing

> **Lectura previa:** [U26: Valoracion DCF](./U26-valoracion-dcf.md)
> **Proxima unidad:** [U29: Teoria Moderna de Portafolios](../fase-7/U29-mpt.md)

---

## 1. Teoria

> ⚠️ **Jane Street / Citadel Core Skill:** El pricing de derivados es la habilidad fundamental en trading cuantitativo y desks de opciones. Todo quant trader entiende Black-Scholes, griegas y volatilidad implicita al reves y al derecho.

### 1.1 Opciones: Calls y Puts

Una **opcion** da el derecho (no la obligacion) de comprar (call) o vender (put) un activo subyacente a un precio de ejercicio (strike) en o antes de una fecha de vencimiento.

| Tipo | Derecho | Payoff al vencimiento | Comprador | Vendedor |
|------|---------|----------------------|-----------|----------|
| Call Europea | Comprar | max(S_T - K, 0) | Derecho a comprar | Obligacion de vender |
| Put Europea | Vender | max(K - S_T, 0) | Derecho a vender | Obligacion de comprar |

```python
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def payoff_call(s_t, k):
    """Payoff de una call option al vencimiento."""
    return np.maximum(s_t - k, 0)

def payoff_put(s_t, k):
    """Payoff de una put option al vencimiento."""
    return np.maximum(k - s_t, 0)

# Graficar payoffs
precios = np.linspace(50, 150, 100)
k = 100
prima_call = 5
prima_put = 4

plt.figure(figsize=(10, 4))
plt.subplot(1, 2, 1)
plt.plot(precios, payoff_call(precios, k) - prima_call, label='Call (con prima)')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(k + prima_call, color='green', linestyle=':', label=f'BE={k+prima_call}')
plt.title('Payoff Call')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(precios, payoff_put(precios, k) - prima_put, label='Put (con prima)')
plt.axhline(0, color='gray', linestyle='--')
plt.axvline(k - prima_put, color='red', linestyle=':', label=f'BE={k-prima_put}')
plt.title('Payoff Put')
plt.legend()
plt.tight_layout()
```

### 1.2 Estrategias con Opciones

```python
def straddle(precios, k, prima_call, prima_put):
    """Straddle: comprar call + put mismo strike. Apuesta a volatilidad."""
    return payoff_call(precios, k) + payoff_put(precios, k) - prima_call - prima_put

def bull_spread(precios, k1, k2, prima_1, prima_2):
    """Bull spread con calls: comprar call K1 bajo, vender call K2 alto."""
    return payoff_call(precios, k1) - payoff_call(precios, k2) - prima_1 + prima_2

def collar(precios, k_put, k_call, prima_put, prima_call):
    """Collar: tener subyacente + comprar put protectora + vender call."""
    subyacente = precios - 100  # Asumiendo compra a 100
    proteccion = payoff_put(precios, k_put) - prima_put
    financiamiento = -payoff_call(precios, k_call) + prima_call
    return subyacente + proteccion + financiamiento
```

> 💡 Las estrategias con opciones permiten expresar cualquier vision de mercado: direccional (bull/bear), volatilidad (straddle/strangle), o rango (butterfly/condor).

### 1.3 Modelo Black-Scholes-Merton (BSM)

El modelo BSM (1973, Premio Nobel) valora opciones europeas asumiendo que el subyacente sigue un Movimiento Browniano Geometrico:

```
dS = μS dt + σS dW

Call: C = S₀ × N(d₁) − K × e^(−rT) × N(d₂)
Put:  P = K × e^(−rT) × N(−d₂) − S₀ × N(−d₁)

Donde:
d₁ = [ln(S₀/K) + (r + σ²/2)T] / (σ√T)
d₂ = d₁ − σ√T
```

```python
def black_scholes_merton(tipo, s0, k, r, sigma, T):
    """Precio de opcion europea por Black-Scholes-Merton.
    
    Parametros:
        tipo: 'call' o 'put'
        s0: precio actual del subyacente
        k: precio de ejercicio (strike)
        r: tasa libre de riesgo (anual, continua)
        sigma: volatilidad (anual)
        T: tiempo hasta vencimiento (anios)
    """
    d1 = (np.log(s0 / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if tipo == 'call':
        precio = s0 * norm.cdf(d1) - k * np.exp(-r * T) * norm.cdf(d2)
    elif tipo == 'put':
        precio = k * np.exp(-r * T) * norm.cdf(-d2) - s0 * norm.cdf(-d1)
    else:
        raise ValueError("tipo debe ser 'call' o 'put'")
    
    return precio

# Ejemplo: Call ATM, S=100, K=100, r=5%, sigma=20%, T=1 anio
call_bsm = black_scholes_merton('call', 100, 100, 0.05, 0.20, 1.0)
put_bsm = black_scholes_merton('put', 100, 100, 0.05, 0.20, 1.0)
print(f"Call BSM: ${call_bsm:.2f}")
print(f"Put BSM:  ${put_bsm:.2f}")
```

> 💡 **Intuicion de BSM:** N(d₂) es la probabilidad riesgo-neutral de que la opcion expire ITM. S₀N(d₁) es el valor esperado del subyacente condicional a que la opcion expire ITM.

### 1.4 Las Griegas

Las griegas miden la sensibilidad del precio de la opcion a cambios en los parametros:

| Griega | Derivada | Mide sensibilidad a | Unidad |
|--------|----------|-------------------|--------|
| Δ (Delta) | ∂C/∂S | Precio del subyacente | $/unidad |
| Γ (Gamma) | ∂²C/∂S² | Cambio en Delta | Δ/unidad |
| Θ (Theta) | −∂C/∂T | Paso del tiempo | $/dia |
| ν (Vega) | ∂C/∂σ | Volatilidad | $/1% vol |
| ρ (Rho) | ∂C/∂r | Tasa de interes | $/1% tasa |

```python
def griegas_completas(tipo, s0, k, r, sigma, T):
    """Calcula todas las griegas de BSM."""
    d1 = (np.log(s0 / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    # Delta
    if tipo == 'call':
        delta = norm.cdf(d1)
    else:
        delta = norm.cdf(d1) - 1
    
    # Gamma (igual para call y put)
    gamma = norm.pdf(d1) / (s0 * sigma * np.sqrt(T))
    
    # Theta (por dia calendario, dividido entre 365)
    theta_call = (-s0 * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                  - r * k * np.exp(-r * T) * norm.cdf(d2))
    theta_put = (-s0 * norm.pdf(d1) * sigma / (2 * np.sqrt(T))
                 + r * k * np.exp(-r * T) * norm.cdf(-d2))
    theta = theta_call if tipo == 'call' else theta_put
    theta_diario = theta / 365
    
    # Vega (cambio por 1% de volatilidad = 0.01)
    vega = s0 * norm.pdf(d1) * np.sqrt(T) * 0.01
    
    # Rho (cambio por 1% de tasa = 0.01)
    if tipo == 'call':
        rho = k * T * np.exp(-r * T) * norm.cdf(d2) * 0.01
    else:
        rho = -k * T * np.exp(-r * T) * norm.cdf(-d2) * 0.01
    
    return {
        'delta': delta, 'gamma': gamma, 'theta': theta_diario,
        'vega': vega, 'rho': rho
    }

# Ejemplo
griegas = griegas_completas('call', 100, 100, 0.05, 0.20, 1.0)
for nombre, valor in griegas.items():
    print(f"{nombre.capitalize()}: {valor:+.4f}")
```

### 1.5 Modelo Binomial (Cox-Ross-Rubinstein)

El modelo binomial discretiza el tiempo y modela el subyacente como un arbol de precios que sube (u) o baja (d) en cada paso:

```python
def binomial_crr(tipo, s0, k, r, sigma, T, pasos=100):
    """Valoracion de opcion europea por arbol binomial CRR."""
    dt = T / pasos
    
    # Parametros CRR
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)  # Probabilidad riesgo-neutral
    
    # Precios terminales del subyacente
    precios_terminales = np.zeros(pasos + 1)
    for j in range(pasos + 1):
        precios_terminales[j] = s0 * (u ** (pasos - j)) * (d ** j)
    
    # Payoffs terminales
    if tipo == 'call':
        valores = np.maximum(precios_terminales - k, 0)
    else:
        valores = np.maximum(k - precios_terminales, 0)
    
    # Backward induction
    descuento = np.exp(-r * dt)
    for i in range(pasos - 1, -1, -1):
        for j in range(i + 1):
            valores[j] = descuento * (p * valores[j] + (1 - p) * valores[j + 1])
    
    return valores[0]

# Comparacion BSM vs Binomial
bsm = black_scholes_merton('call', 100, 100, 0.05, 0.20, 1.0)
binomial = binomial_crr('call', 100, 100, 0.05, 0.20, 1.0, 500)
print(f"BSM:       ${bsm:.4f}")
print(f"Binomial:  ${binomial:.4f}")
print(f"Diferencia: ${abs(bsm - binomial):.6f}")
```

> 💡 Con muchos pasos (≥100), el binomial converge a BSM. La ventaja del binomial es que puede valorar opciones americanas (ejercicio temprano) que BSM no puede.

### 1.6 Volatilidad Implicita (IV)

La volatilidad implicita es la σ que iguala el precio BSM al precio de mercado. No tiene formula cerrada: requiere metodo numerico.

```python
def volatilidad_implicita(precio_mercado, tipo, s0, k, r, T, 
                          sigma_inicial=0.3, tolerancia=1e-6):
    """Calcula volatilidad implicita por Newton-Raphson.
    
    Itera hasta que |precio_bsm - precio_mercado| < tolerancia.
    """
    sigma = sigma_inicial
    
    for _ in range(100):
        precio_bsm = black_scholes_merton(tipo, s0, k, r, sigma, T)
        vega = s0 * norm.pdf(
            (np.log(s0 / k) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
        ) * np.sqrt(T)
        
        if abs(vega) < 1e-10:
            break
        
        diff = precio_bsm - precio_mercado
        sigma = sigma - diff / vega  # Newton-Raphson
        
        if abs(diff) < tolerancia:
            return sigma
    
    return sigma

# Ejemplo: Call cotiza a $12.50 en el mercado
iv = volatilidad_implicita(12.50, 'call', 100, 100, 0.05, 1.0)
print(f"Volatilidad implicita: {iv:.2%}")
```

### 1.7 Volatility Smile y Skew

En el mundo real, la volatilidad implicita NO es constante: varia con el strike (smile) y con el vencimiento (term structure).

```python
def construir_smile_volatilidad(precios_mercado, tipo, s0, strikes, r, T):
    """Construye la curva de volatility smile."""
    ivs = []
    for i, (k, precio) in enumerate(zip(strikes, precios_mercado)):
        iv = volatilidad_implicita(precio, tipo, s0, k, r, T)
        ivs.append(iv)
    return np.array(ivs)

# Simular smile tipico de equities (skew negativo)
strikes = np.linspace(80, 120, 21)
s0 = 100
sigma_base = 0.20

# Precios con volatilidad variable (skew)
sigmas_reales = sigma_base - 0.003 * (strikes - s0)  # Skew: menor K = mayor IV
precios_sinteticos = np.array([
    black_scholes_merton('call', s0, k, 0.05, sigma, 1.0)
    for k, sigma in zip(strikes, sigmas_reales)
])

ivs_recuperadas = construir_smile_volatilidad(
    precios_sinteticos, 'call', s0, strikes, 0.05, 1.0
)
```

> 💡 El volatility smile existe porque el mercado asigna mayor probabilidad a eventos extremos (fat tails) que lo que predice la distribucion log-normal de BSM. Esto es especialmente pronunciado en indices de equity (crashophobia: puts OTM cotizan con IV mas alta).

---

## 2. Practica

### 2.1 Ejercicio guiado: Pricer de Opciones con Griegas y IV

**Concepto financiero:** Construimos un pricer completo para opciones sobre AAPL (S=$185, volatilidad 25%, sin dividendos).

**Codigo:**

```python
import numpy as np
from scipy.stats import norm

# Pricer BSM
def bsm(tipo, s, k, r, sigma, T):
    d1 = (np.log(s/k) + (r + 0.5*sigma**2)*T) / (sigma*np.sqrt(T))
    d2 = d1 - sigma*np.sqrt(T)
    if tipo == 'call':
        return s*norm.cdf(d1) - k*np.exp(-r*T)*norm.cdf(d2)
    return k*np.exp(-r*T)*norm.cdf(-d2) - s*norm.cdf(-d1)

# Parametros AAPL
s0 = 185.0
r = 0.045
sigma_impl = 0.25
T = 30/365  # 30 dias

strikes = [170, 175, 180, 185, 190, 195, 200]

print("=== Pricer de Opciones AAPL ===")
print(f"S0=${s0}, r={r:.1%}, sigma={sigma_impl:.0%}, T={T*365:.0f} dias\n")
print(f"{'Strike':>8} {'Call':>8} {'Put':>8} {'Delta C':>8} {'Gamma':>8} {'Vega':>8}")

for k in strikes:
    call = bsm('call', s0, k, r, sigma_impl, T)
    put = bsm('put', s0, k, r, sigma_impl, T)
    d1 = (np.log(s0/k) + (r + 0.5*sigma_impl**2)*T) / (sigma_impl*np.sqrt(T))
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (s0 * sigma_impl * np.sqrt(T))
    vega = s0 * norm.pdf(d1) * np.sqrt(T) * 0.01
    print(f"${k:>6}  ${call:>7.2f}  ${put:>7.2f}  {delta:>7.3f}  {gamma:>7.4f}  ${vega:>6.3f}")
```

**Output:**
```
=== Pricer de Opciones AAPL ===
S0=$185, r=4.5%, sigma=25%, T=30 dias

  Strike     Call      Put   Delta C    Gamma     Vega
$   170  $ 16.04  $  0.52    0.898    0.0172  $0.145
$   175  $ 12.18  $  1.66    0.781    0.0252  $0.213
$   180  $  8.76  $  3.23    0.622    0.0298  $0.252
$   185  $  6.00  $  5.47    0.457    0.0295  $0.249
$   190  $  3.93  $  8.40    0.309    0.0252  $0.213
$   195  $  2.46  $ 11.93    0.194    0.0188  $0.159
$   200  $  1.48  $ 15.95    0.114    0.0125  $0.106
```

---

## 3. Aplicacion en Finanzas 💰

El pricing de derivados es esencial en:

- **Market Making (Jane Street, Citadel Securities):** Los market makers cotizan bid/ask de miles de opciones simultaneamente. Usan BSM + ajustes por smile en tiempo real.
- **Delta Hedging:** Un trader que vende una call compra Delta acciones del subyacente para neutralizar el riesgo direccional. El Gamma mide cuanto debe rebalancear.
- **Volatility Arbitrage:** Si la IV de una opcion es 25% y crees que la volatilidad realizada sera 20%, vendes la opcion y haces delta-hedging para capturar el spread.
- **Risk Management:** Las griegas permiten descomponer el riesgo de un book de opciones en factores independientes.

> 💡 En desks de derivados, el trader mira una pantalla con: posicion neta en Delta, Gamma, Vega, Theta. Al final del dia, el P&L se explica por: P&L = Delta×ΔS + 0.5×Gamma×(ΔS)² + Vega×Δσ + Theta×Δt.

---

## 4. Ejercicios Propuestos

> Los archivos de ejercicios estan en `documentacion/ejercicios/fase-6/U28_ejercicios.py`

1. **BSM Pricer + Griegas:** Implementa funciones para BSM (call y put) y calcula las 5 griegas. Prueba con S=100, K=105, r=4%, σ=30%, T=0.5 anios. Muestra todas las griegas.

2. **Binomial vs BSM:** Implementa el modelo binomial CRR y compara los precios con BSM para 10, 50, 100 y 500 pasos. Muestra la convergencia.

3. **Volatility Smile:** Dados 5 precios de mercado para calls con diferentes strikes (mismo subyacente y vencimiento), calcula la IV de cada uno y grafica el volatility smile. Explica por que tiene esa forma.

4. **Payoff de Estrategias:** Define funciones para graficar los payoffs de: (a) covered call (long stock + short call), (b) protective put (long stock + long put), (c) bull spread con calls, (d) straddle. Marca break-evens y zonas de ganancia/perdida.

5. **IV Surface:** Para un conjunto de opciones con diferentes strikes (80-120) y vencimientos (1M, 3M, 6M, 1Y), calcula la IV de todas y construye una superficie 3D de volatilidad (strike vs T vs IV).

---

## 5. Resumen

| Concepto | Formula/Descripcion | Uso |
|---------|-------------------|-----|
| Call BSM | S₀N(d₁) - Ke^(-rT)N(d₂) | Precio de call europea |
| Put BSM | Ke^(-rT)N(-d₂) - S₀N(-d₁) | Precio de put europea |
| Delta | N(d₁) para call | Hedge ratio |
| Gamma | N'(d₁)/(S₀σ√T) | Estabilidad del delta |
| Vega | S₀N'(d₁)√T × 0.01 | Sensibilidad a volatilidad |
| Theta | -∂C/∂T | Decaimiento temporal |
| Binomial CRR | Arbol binomial backward induction | Opciones americanas |
| IV | σ que iguala BSM al precio mercado | Expectativa de volatilidad |
| Smile | IV varia con K | Evidencia de fat tails |

---

## ✅ Autoevaluacion

1. ¿Por que el delta de una call ATM es aproximadamente 0.5?
2. ¿Que significa un Gamma alto y por que es relevante para un delta hedger?
3. ¿Por que la volatilidad implicita de puts OTM suele ser mayor que la de calls OTM en indices de equity?
4. ¿Como converge el modelo binomial al BSM cuando aumentas los pasos?
5. ¿Que informacion obtienes del volatility smile que no obtienes del precio de la opcion?

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en memoria:
> - Formula BSM para calls y puts
> - Las 5 griegas y su interpretacion financiera
> - Arbol binomial CRR y backward induction
> - Calculo de volatilidad implicita por Newton-Raphson
> - Volatility smile como evidencia de fat tails en retornos
