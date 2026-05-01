# U09: Bucles for Anidados

> **Lectura previa:** [U08: Bucle while y control de flujo](./U08-while-control.md)
> **Próxima unidad:** [U10: Listas y tuplas](../fase-4/U10-listas-tuplas.md)

---

## 1. Teoría

### 1.1 ¿Qué es un bucle anidado?

Un bucle **dentro de otro bucle**. El bucle interno se ejecuta **completamente** por cada iteración del bucle externo.

```python
# Bucle externo: filas
for i in range(1, 4):
    # Bucle interno: columnas
    for j in range(1, 4):
        print(f"({i},{j})", end=" ")
    print()   # Nueva línea después de cada fila

# Output:
# (1,1) (1,2) (1,3)
# (2,1) (2,2) (2,3)
# (3,1) (3,2) (3,3)
```

> 💡 **Regla:** por cada iteración del bucle externo, el bucle interno da **todas** sus vueltas.

### 1.2 Matrices (listas de listas)

Las matrices son la aplicación natural de bucles anidados:

```python
# Crear una matriz 3×3
matriz = []
for i in range(3):
    fila = []
    for j in range(3):
        fila.append(i * 3 + j + 1)
    matriz.append(fila)

# Imprimir la matriz
for fila in matriz:
    for valor in fila:
        print(f"{valor:3}", end=" ")
    print()

# Output:
#   1   2   3
#   4   5   6
#   7   8   9
```

### 1.3 Operaciones con matrices

```python
# Suma de matrices
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = [[0, 0], [0, 0]]

for i in range(2):
    for j in range(2):
        C[i][j] = A[i][j] + B[i][j]

# Transposición
filas, cols = 2, 3
original = [[1, 2, 3], [4, 5, 6]]
transpuesta = []
for j in range(cols):
    nueva_fila = []
    for i in range(filas):
        nueva_fila.append(original[i][j])
    transpuesta.append(nueva_fila)
```

### 1.4 Pirámides y patrones

```python
# Pirámide de números
for i in range(1, 6):
    for j in range(i):
        print(i, end=" ")
    print()

# Output:
# 1
# 2 2
# 3 3 3
# 4 4 4 4
# 5 5 5 5 5

# Tabla de multiplicar
for i in range(1, 6):
    for j in range(1, 11):
        print(f"{i}×{j}={i*j:2}", end="  ")
    print()
```

### 1.5 Break y continue en bucles anidados

`break` y `continue` solo afectan al bucle **más interno**:

```python
for i in range(1, 4):
    for j in range(1, 4):
        if j == 2:
            break              # Solo rompe el bucle de j
        print(f"({i},{j})", end=" ")
    print()
# Output:
# (1,1)
# (2,1)
# (3,1)

# break en ambos niveles requiere variable bandera
encontrado = False
for i in range(3):
    for j in range(3):
        if i == 1 and j == 1:
            encontrado = True
            break
    if encontrado:
        break
```

### 1.6 Complejidad: evita anidar innecesariamente

Cada nivel de anidación **multiplica** el número de operaciones:

```python
# O(n²) — 10,000 iteraciones para n=100
for i in range(100):
    for j in range(100):
        pass

# O(n³) — 1,000,000 iteraciones para n=100
for i in range(100):
    for j in range(100):
        for k in range(100):
            pass
```

---

## 2. Práctica

### 2.1 Ejercicio guiado: Calculadora de covarianza

```python
# Datos: rendimientos diarios de 2 acciones
accion_a = [1.2, -0.5, 2.1, -0.8, 0.3]
accion_b = [0.8, -0.3, 1.9, -0.5, 0.1]

n = len(accion_a)
promedio_a = sum(accion_a) / n
promedio_b = sum(accion_b) / n

# Calcular covarianza
suma_productos = 0
for i in range(n):
    diff_a = accion_a[i] - promedio_a
    diff_b = accion_b[i] - promedio_b
    suma_productos += diff_a * diff_b

covarianza = suma_productos / (n - 1)
print(f"Covarianza: {covarianza:.4f}")
```

### 2.2 Ejercicio guiado: Tabla de valor futuro

```python
# ¿Cuánto vale $1,000 a diferentes tasas y plazos?
capital = 1000
tasas = [5, 8, 10, 12]
plazos = range(1, 11)

print(f"Capital inicial: ${capital:,}")
print(f"{'Año':<6}", end="")
for tasa in tasas:
    print(f"{tasa}%".rjust(10), end="")
print()

for anio in plazos:
    print(f"{anio:<6}", end="")
    for tasa in tasas:
        vf = capital * (1 + tasa/100) ** anio
        print(f"${vf:>9,.0f}", end="")
    print()
```

### 2.3 Ejercicio guiado: Búsqueda en matriz de precios

```python
# Matriz: filas = activos, columnas = días
precios = [
    [150, 152, 149, 153, 155],   # AAPL
    [280, 282, 279, 285, 290],   # MSFT
    [900, 895, 910, 905, 920],   # TSLA
]

# Encontrar el precio máximo y su posición
max_precio = 0
activo_max = dia_max = -1

for i, fila in enumerate(precios):
    for j, precio in enumerate(fila):
        if precio > max_precio:
            max_precio = precio
            activo_max = i
            dia_max = j

activos = ["AAPL", "MSFT", "TSLA"]
print(f"Precio máximo: ${max_precio} ({activos[activo_max]}, día {dia_max + 1})")
```

---

## 3. Aplicación en Finanzas 💰

### 3.1 Matriz de correlación

```python
# Rendimientos de 3 activos (filas = activos, columnas = días)
rendimientos = [
    [1.2, -0.5, 2.1, -0.8],    # Activo A
    [0.8, -0.3, 1.9, -0.5],    # Activo B
    [-0.5, 1.2, -1.1, 0.7],    # Activo C
]

n_activos = len(rendimientos)
n_dias = len(rendimientos[0])

# Calcular promedios
promedios = []
for activo in rendimientos:
    promedios.append(sum(activo) / n_dias)

# Matriz de correlación
nombres = ["A", "B", "C"]
print("Matriz de correlación:")
print("     ", end="")
for n in nombres:
    print(f"  {n}  ", end="")
print()

for i in range(n_activos):
    print(f"  {nombres[i]} ", end="")
    for j in range(n_activos):
        suma_xy = 0
        suma_xx = 0
        suma_yy = 0
        for d in range(n_dias):
            dx = rendimientos[i][d] - promedios[i]
            dy = rendimientos[j][d] - promedios[j]
            suma_xy += dx * dy
            suma_xx += dx * dx
            suma_yy += dy * dy
        corr = suma_xy / ((suma_xx * suma_yy) ** 0.5) if suma_xx and suma_yy else 0
        print(f"{corr:5.2f}", end="")
    print()
```

### 3.2 Optimización de portafolio (grilla)

```python
# Buscar la mejor combinación de 2 activos (grilla 0% a 100%)
rendimiento_a = 12   # % anual
rendimiento_b = 8
riesgo_a = 18        # % volatilidad
riesgo_b = 10
correlacion = 0.3

mejor_sharpe = 0
mejor_w = 0
tasa_libre = 4

for w in range(0, 101):
    w_pct = w / 100
    # Rendimiento del portafolio
    rp = w_pct * rendimiento_a + (1 - w_pct) * rendimiento_b
    # Riesgo del portafolio
    varianza = (w_pct * riesgo_a) ** 2 + ((1 - w_pct) * riesgo_b) ** 2
    varianza += 2 * w_pct * (1 - w_pct) * correlacion * riesgo_a * riesgo_b
    riesgo_p = varianza ** 0.5
    sharpe = (rp - tasa_libre) / riesgo_p
    if sharpe > mejor_sharpe:
        mejor_sharpe = sharpe
        mejor_w = w_pct

print(f"Mejor asignación: {mejor_w:.0%} en A, {1-mejor_w:.0%} en B")
print(f"Sharpe ratio: {mejor_sharpe:.2f}")
```

---

## 4. Ejercicios Propuestos

1. **Matriz de rendimientos:** Crea una matriz 3×5 de rendimientos aleatorios. Encuentra el peor rendimiento y su posición.

2. **Tabla de crédito:** Muestra cuánto pagas en total por un préstamo a diferentes tasas (4%-12%) y plazos (1-5 años).

3. **Producto de matrices:** Multiplica una matriz 2×3 por una 3×2.

4. **Optimización de grilla:** Encuentra la combinación de 3 activos (con restricción de suma = 100%) que maximiza el Sharpe. Usa triple for con paso de 10%.

---

## 5. Resumen

| Concepto | Ejemplo |
|---------|---------|
| Bucle anidado | `for i in ...: for j in ...:` |
| Matriz | `lista[i][j]` |
| Búsqueda 2D | Índices i, j con bandera |
| Complejidad | 2 niveles = O(n²) |
| break anidado | Solo rompe nivel interno |

---

## ✅ Autoevaluación

1. ¿Cuántas veces se ejecuta `print("x")` en `for i in range(3): for j in range(4): print("x")`?
2. Si uso `break` dentro del bucle interno, ¿se detiene el bucle externo?
3. ¿Cómo accedes al elemento de la fila 1, columna 2 en una matriz?
4. Escribe un programa que genere un tablero de ajedrez con `#` y espacios.

---

> 📝 **Knowledge Wiki:** Al terminar esta unidad, guarda en `~/.claude/projects/-Users-miguelangelquispetito-Desktop-ZED/memory/`:
> - `reference-U09.md`: Patrones de matrices, búsqueda 2D y banderas de break
> - `project-U09.md`: Optimización de portafolio por grilla y matriz de correlación
