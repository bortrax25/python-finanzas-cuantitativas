# EJERCICIOS DE FOR ANIDADOS

# Ejercicio 1: Imprimir tabla de multiplicar del 1 al 5
print("=== Tabla de multiplicar 1-5 ===")
for i in range(1, 6):
    for j in range(1, 11):
        print(f"{i} x {j} = {i*j}")
    print()

# Ejercicio 2: Crear matriz 3x3
print("=== Matriz 3x3 ===")
matriz = []
for i in range(3):
    fila = []
    for j in range(3):
        fila.append(i * 3 + j + 1)
    matriz.append(fila)

for fila in matriz:
    print(fila)

# Ejercicio 3: Contar vocales en varias palabras
print("=== Contar vocales ===")
palabras = ["hola", "mundo", "python", "programacion"]
vocales = "aeiou"

for palabra in palabras:
    contador = 0
    for letra in palabra.lower():
        if letra in vocales:
            contador += 1
    print(f"{palabra}: {contador} vocales")

# Ejercicio 4: Generar combinaciones de letras
print("=== Combinaciones ===")
letras = ["A", "B", "C"]
for i in range(len(letras)):
    for j in range(len(letras)):
        print(letras[i] + letras[j], end=" ")
    print()

# Ejercicio 5: Sumar matrices
print("=== Suma de matrices ===")
A = [[1, 2], [3, 4]]
B = [[5, 6], [7, 8]]
C = [[0, 0], [0, 0]]

for i in range(2):
    for j in range(2):
        C[i][j] = A[i][j] + B[i][j]

for fila in C:
    print(fila)

# Ejercicio 6: pirámide de números
print("=== Pirámide de números ===")
for i in range(1, 6):
    for j in range(i):
        print(i, end=" ")
    print()

# Ejercicio 7: buscar número en matriz
print("=== Buscar número en matriz ===")
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
buscar = 5
encontrado = False

for i in range(3):
    for j in range(3):
        if matriz[i][j] == buscar:
            print(f"Encontrado {buscar} en полож [{i}][{j}]")
            encontrado = True

if not encontrado:
    print(f"{buscar} no encontrado")