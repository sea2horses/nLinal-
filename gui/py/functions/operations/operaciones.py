# Multiplica una matriz (n x m) por un vector (m x 1)
from py.functions.models.matriz import Matriz
from py.functions.models.vector import Vector
from fractions import Fraction
from py.functions.utils.auxiliar import a_fraccion

import py.functions.utils.latex as latex

SILENT_MODE = False


def funnel(*_latex: str):
    if not SILENT_MODE:
        for part in _latex:
            latex.LATEX_STDOUT.writelatex(part)

# Latex helpers


def latex_fila(numero: int, coeficiente: Fraction = Fraction(1), force_sign: bool = False) -> str:
    if coeficiente != 1:
        return latex.fraction(coeficiente, force_sign) + "f" + latex.subscript(str(numero))
    else:
        return "f" + latex.subscript(str(numero))

# Aqui en este archivo van todas las operaciones sobre matrices
# Operaciones basicas en una fila

# Escala una fila por un numero
# a la fila [1][2][3] * 3 -> [3][6][9]
# f -> e*f


def escalar_fila(mat: Matriz, fila: int, escalar: Fraction):
    funnel(
        latex.indexedvar("f", fila),
        latex.rarrow(),
        latex.term(latex.indexedvar("f", fila), a_fraccion(escalar))
    )

    # Ciclamos por las columnas en la fila
    for i in range(1, mat.columnas + 1):
        nuevo_valor: Fraction = mat.at(fila, i) * a_fraccion(escalar)
        # En la posicion [fila, i] vamos a cambiar el valor por el mismo pero multiplicado por el escalar
        mat.set(fila, i, nuevo_valor)

# Sumar una fila B a una fila A
# el resultado queda guardado en A
# fa -> fa + fb


def sumar_fila(mat: Matriz, fila_a: int, fila_b: int):
    funnel(latex.indexedvar("f", fila_a),
           latex.rarrow(),
           latex.indexedvar("f", fila_a),
           " + ",
           latex.indexedvar("f", fila_b)
           )
    # Ciclamos de nuevo por las columnas
    for i in range(1, mat.columnas + 1):
        # En la fila A, ponemos el resultado de A + B
        nuevo_valor: Fraction = mat.at(fila_a, i) + mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# Sumar filas escaladas
# fa -> c*fa + d*fb

# [1][5][4]
# [2][1][5]

# f2 -> 1 * f2 + (-2) * f1
# [1][5][4]
# [0][-9][-3]


def sumar_escalar_fila(mat: Matriz, escalar_a: Fraction, fila_a: int, escalar_b: Fraction, fila_b: int):
    funnel(
        latex.indexedvar("f", fila_a),
        latex.rarrow(),
        latex.term(latex.indexedvar("f", fila_a), escalar_a),
        latex.term(latex.indexedvar("f", fila_b), escalar_b, forcesign=True),
    )
    # Ciclamos por la fila A para cambiar los valores
    for i in range(1, mat.columnas + 1):
        # NUEVO VALor
        nuevo_valor: Fraction = escalar_a * \
            mat.at(fila_a, i) + escalar_b * mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# La misma operacion pero en resta


def restar_fila(mat: Matriz, fila_a: int, fila_b: int):
    funnel(latex.indexedvar("f", fila_a),
           latex.rarrow(),
           latex.indexedvar("f", fila_a),
           " - ",
           latex.indexedvar("f", fila_b)
           )
    # Ciclamos de nuevo por las columnas
    for i in range(1, mat.columnas + 1):
        # En la fila A, ponemos el resultado de A - B
        nuevo_valor: Fraction = mat.at(fila_a, i) - mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# Restar filas escaladas
# fa -> c*fa - d*fb


# Sumar filas escaladas
# fa -> c*fa + d*fb

# [1][5][4]
# [2][1][5]

# f2 -> 1 * f2 - 2 * f1
# [1][5][4]
# [0][-9][-3]

def restar_escalar_fila(mat: Matriz, escalar_a, fila_a: int, escalar_b, fila_b: int):
    funnel(
        latex.indexedvar("f", fila_a),
        latex.rarrow(),
        latex.term(latex.indexedvar("f", fila_a), escalar_a),
        latex.term(latex.indexedvar("f", fila_b),
                   escalar_b * -1, forcesign=True),
    )
    # Ciclamos por la fila A para cambiar los valores
    for i in range(1, mat.columnas + 1):
        # NUEVO VALor
        nuevo_valor: Fraction = a_fraccion(escalar_a) * \
            mat.at(fila_a, i) - a_fraccion(escalar_b) * mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# Intercambio de filas
# fa <-> fb


def intercambiar_fila(mat: Matriz, fila_a: int, fila_b: int):
    funnel(
        latex.indexedvar("f", fila_a),
        latex.barrow(),
        latex.indexedvar("f", fila_b)
    )
    # Ciclamos de nuevo por las columnas
    for i in range(1, mat.columnas + 1):
        # Intercambiamos los valores
        temp: Fraction = mat.at(fila_a, i)
        mat.set(fila_a, i, mat.at(fila_b, i))
        mat.set(fila_b, i, temp)

# Detectar si una fila es nula


def fila_nula(mat: Matriz, fila: int) -> bool:
    # Ciclamos de nuevo por las columnas
    for i in range(1, mat.columnas + 1):
        # Intercambiamos los valores
        if mat.at(fila, i) != 0:
            return False
    return True

# Operaciones basicas en una columna (por ahora solo una)
# Detectar si una columna es nula (0)


def columna_nula(mat: Matriz, columna: int) -> bool:
    # Ciclamos por todas las filas
    for i in range(1, mat.filas + 1):
        # Si encontramos un valor que no es 0, retornamos False
        if mat.at(i, columna) != 0:
            return False
    # Si no encontramos ningun valor que no es 0, retornamos True
    return True


# OPERACIONES ENTRE MATRICES

# Suma dos matrices y devuelve una nueva con el resultado
def suma_matrices(matrizA: Matriz, matrizB: Matriz):
    if matrizA.filas != matrizB.filas or matrizA.columnas != matrizB.columnas:
        raise Exception(
            f"No se puede sumar una matriz de {matrizA.filas}x{matrizA.columnas} con una matriz de {matrizB.filas}x{matrizB.columnas}")

    # No importa tomar matriz a o matriz b porque ambas son del mismo tamaño
    filas = matrizA.filas
    columnas = matrizA.columnas

    funnel(latex.text("Sumando matrices"), latex.newline(),
           latex.matrix(matrizA), " + ", latex.matrix(matrizB), latex.newline())

    nueva_matriz: Matriz = Matriz(filas, columnas)

    # Cada cuadrado de la nueva matriz es el resultado de la suma de los numeros
    # en esa posicion en ambas matrices
    for fila in range(1, filas + 1):
        for columna in range(1, columnas + 1):
            a = matrizA.at(fila, columna)
            b = matrizB.at(fila, columna)
            res = a + b
            funnel(
                latex.fraction(
                    a), " + ", latex.fraction(b), " = ", latex.fraction(res), latex.newline()
            )
            nueva_matriz.set(fila, columna, res)

    return nueva_matriz

# Resta dos matrices y devuelve una nueva con el resultado


def resta_matrices(matrizA: Matriz, matrizB: Matriz) -> Matriz:
    if matrizA.filas != matrizB.filas or matrizA.columnas != matrizB.columnas:
        raise Exception(
            f"No se puede restar una matriz de {matrizA.filas}x{matrizA.columnas} con una matriz de {matrizB.filas}x{matrizB.columnas}")

    # No importa tomar matriz a o matriz b porque ambas son del mismo tamaño
    filas = matrizA.filas
    columnas = matrizA.columnas

    funnel(latex.text("Restando matrices"), latex.newline(),
           latex.matrix(matrizA), " - ", latex.matrix(matrizB), latex.newline())

    nueva_matriz: Matriz = Matriz(filas, columnas)

    # Cada cuadrado de la nueva matriz es el resultado de la suma de los numeros
    # en esa posicion en ambas matrices
    for fila in range(1, filas + 1):
        for columna in range(1, columnas + 1):
            a = matrizA.at(fila, columna)
            b = matrizB.at(fila, columna)
            res = a - b
            funnel(
                latex.fraction(
                    a), " - ", latex.fraction(b), " = ", latex.fraction(res), latex.newline()
            )
            nueva_matriz.set(fila, columna, res)

    return nueva_matriz


def matriz_por_escalar(matriz: Matriz, escalar: Fraction) -> Matriz:
    funnel(latex.text("Escalando matriz por "), latex.fraction(a_fraccion(escalar)), latex.newline(),
           latex.matrix(matriz), latex.newline())

    nueva_matriz: Matriz = Matriz(matriz.filas, matriz.columnas)

    for fila in range(1, matriz.filas + 1):
        for columna in range(1, matriz.columnas + 1):
            val = matriz.at(fila, columna)
            res = val * a_fraccion(escalar)
            funnel(latex.fraction(val), latex.cdot(), latex.fraction(
                a_fraccion(escalar)), " = ", latex.fraction(res), latex.newline())
            nueva_matriz.set(fila, columna, res)

    return nueva_matriz


def multiplicar_matrices(matrizA: Matriz, matrizB: Matriz) -> Matriz:
    """
    Multiplica dos matrices y devuelve la matriz resultado.

    Esta función implementa la operación estándar de multiplicación matricial:
        C = A * B

    donde:
        - `matrizA` es de tamaño (m x n)
        - `matrizB` es de tamaño (n x p)
        - El resultado `C` será una nueva matriz de tamaño (m x p)

    Requisitos:
        - El número de columnas de `matrizA` debe coincidir con el número de filas de `matrizB`.
          En caso contrario, se lanza una excepción.

    Parámetros:
        matrizA (Matriz): La primera matriz, de tamaño m x n.
        matrizB (Matriz): La segunda matriz, de tamaño n x p.

    Retorna:
        Matriz: Una nueva matriz de tamaño m x p, que representa el producto matricial A * B.

    Excepciones:
        Exception: Si las dimensiones no son compatibles para la multiplicación.

    Procedimiento paso a paso:
        1. Verificar que las matrices sean multiplicables (número de columnas de A = número de filas de B).
        2. Crear una nueva matriz vacía `nueva_matriz` con m filas y p columnas.
        3. Para cada posición (i, j) en `nueva_matriz`, calcular:
               suma = Σ (A[i, k] * B[k, j])   para k = 1..n
        4. Guardar el valor calculado en la celda correspondiente.
        5. Devolver la nueva matriz.

    Ejemplo:
        Si A = [ [1, 2, 3],
                 [4, 5, 6] ]    (2 x 3)

        y B = [ [7,  8],
                 [9, 10],
                 [11,12] ]      (3 x 2)

        entonces C = A * B será:

        C = [ [ 58,  64],
              [139, 154] ]      (2 x 2)
    """

    # Paso 1: Verificar compatibilidad de dimensiones
    # La multiplicación de matrices A (m x n) y B (n x p) solo es posible si n = filas(B).
    if matrizA.columnas != matrizB.filas:
        raise Exception(
            f"No se puede multiplicar una matriz de {matrizA.filas}x{matrizA.columnas} "
            f"con una matriz de {matrizB.filas}x{matrizB.columnas}"
        )

    # Paso 2: Crear matriz resultado con el tamaño correcto (m x p)
    funnel(latex.text("Multiplicando matrices"), latex.newline(),
           latex.matrix(matrizA), latex.cdot(), latex.matrix(matrizB), latex.newline())

    nueva_matriz = Matriz(matrizA.filas, matrizB.columnas)

    # Paso 3: Recorrer todas las posiciones de la matriz resultado
    for i in range(1, matrizA.filas + 1):          # Recorre filas de A (1..m)
        for j in range(1, matrizB.columnas + 1):   # Recorre columnas de B (1..p)
            # Acumulador para el producto escalar fila_i(A) · columna_j(B)
            suma = Fraction(0)

            # Paso 3.1: Calcular el producto escalar
            # k recorre los índices compartidos (1..n)

            # Entonces aca, por ejemplo, en la fila 1, columna 1
            # vas a querer recorrer las posiciones:

            # (1, 1) * (1, 1)
            # (1, 2) * (2, 1)
            # (1, 3) * (3, 1)
            # y sumarlas todas
            # Veanse este video https://www.youtube.com/watch?v=7E_VvhYvJgU
            funnel(latex.text(f"Elemento ({i},{j})"), latex.newline())
            terms = []
            for k in range(1, matrizA.columnas + 1):
                prod = matrizA.at(i, k) * matrizB.at(k, j)
                terms.append(prod)
                funnel(latex.fraction(matrizA.at(i, k)), latex.cdot(), latex.fraction(
                    matrizB.at(k, j)), " = ", latex.fraction(prod), latex.newline())
                suma += prod
            # Mostrar suma total
            funnel(" + ".join(latex.fraction(t) for t in terms),
                   " = ", latex.fraction(suma), latex.newline())

            # Paso 4: Asignar el valor calculado a la celda (i, j) del resultado
            nueva_matriz.set(i, j, suma)

    # Paso 5: Devolver la matriz resultante
    return nueva_matriz


def transponer_matriz(matriz: Matriz) -> Matriz:
    funnel(latex.text("Transponiendo matriz"), latex.newline(),
           latex.matrix(matriz), latex.newline())
    nueva_matriz = Matriz(matriz.columnas, matriz.filas)

    for fila in range(1, matriz.filas + 1):
        funnel(latex.text(
            f"La fila {fila} pasa a columna {fila}"), latex.newline())
        for columna in range(1, matriz.columnas + 1):
            nueva_matriz.set(columna, fila, matriz.at(fila, columna))

    return nueva_matriz


def matriz_inversa(matriz: Matriz) -> Matriz:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede invertir una matriz no cuadrada")

    nueva_matriz = Matriz(matriz.filas, matriz.columnas)

    determinante = determinante_por_cofactores(matriz)

    for fila in range(1, matriz.filas + 1):
        for columna in range(1, matriz.columnas + 1):
            valor: Fraction

            # Diagonal
            if fila == columna:
                funnel(latex.text(
                    f"Invirtiendo diagonal {fila},{columna} con {matriz.filas - fila + 1},{matriz.columnas - columna + 1}"), latex.newline())
                valor = matriz.at(
                    matriz.filas - fila + 1, matriz.columnas - columna + 1)
            else:
                valor = matriz.at(fila, columna) * -1

            valor /= determinante
            nueva_matriz.set(fila, columna, valor)

    return nueva_matriz


def remover_columna(matriz: Matriz, columna: int) -> Matriz:
    if columna < 1 or columna > matriz.columnas:
        raise Exception("La columna dada a remover es inválida")

    nueva_matriz = Matriz(matriz.filas, matriz.columnas - 1)
    for f in range(1, matriz.filas + 1):
        col: int = 1
        for c in range(1, matriz.columnas + 1):
            if c == columna:
                continue
            nueva_matriz.set(f, col, matriz.at(f, c))
            col += 1

    return nueva_matriz


def remover_fila(matriz: Matriz, fila: int) -> Matriz:
    if fila < 1 or fila > matriz.filas:
        raise Exception("La fila dada a remover es inválida")

    nueva_matriz = Matriz(matriz.filas - 1, matriz.columnas)

    fil: int = 1
    for f in range(1, matriz.filas + 1):
        if f == fila:
            continue
        for c in range(1, matriz.columnas + 1):
            nueva_matriz.set(fil, c, matriz.at(f, c))
        fil += 1

    return nueva_matriz


def cofactor(matriz: Matriz, i: int, j: int) -> Matriz:
    return remover_fila(remover_columna(matriz, j), i)


# def calcular_determinante(matriz: Matriz) -> Fraction:
#     if matriz.filas != matriz.columnas:
#         raise Exception(
#             f"No se puede obtener el determinante de una matriz no cuadrada")

#     n = matriz.filas

#     if n == 2:
#         # Diagonal principal
#         diagonal_principal: Fraction = Fraction(1)
#         diagonal_secundaria: Fraction = Fraction(1)

#         for i in range(1, n + 1):
#             print(
#                 f"Diagonal principal: {i}, {i}, Diagonal Secundaria: {i}, {matriz.columnas - i + 1}")
#             diagonal_principal *= matriz.at(i, i)
#             diagonal_secundaria *= matriz.at(i, matriz.columnas - i + 1)

#         return diagonal_principal - diagonal_secundaria
#     else:
#         raise Exception(
#             f"No se ha implementado la obtención del determinante en matrices {n}x{n}")

def determinante_por_sarrus(matriz: Matriz) -> Fraction:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener el determinante de una matriz no cuadrada")

    n = matriz.filas
    if n != 3:
        raise Exception(
            f"El metodo de sarrus solo es válido para matrices 3x3")

    funnel(latex.text("Determinante por Sarrus"),
           latex.newline(), latex.matrix(matriz), latex.newline())
    # Para sarrus necesitamos agregar (n - 1) filas adicionales a una nueva matriz
    detmatriz = Matriz(n + (n - 1), n)

    for i in range(1, matriz.filas + 1):
        for j in range(1, matriz.columnas + 1):
            detmatriz.set(i, j, matriz.at(i, j))

    # Añadimos las copias de las filas adicionales
    for i in range(1, matriz.filas):
        for j in range(1, matriz.columnas + 1):
            detmatriz.set(n + i, j, matriz.at(i, j))

    funnel(latex.text("Matriz expandida para Sarrus"),
           latex.newline(), latex.matrix(detmatriz), latex.newline())

    # Ahora calculamos las diagonales positivas
    suma_diagonales_positivas = Fraction(0)

    for i in range(0, n):
        diagonal = []
        valor_diagonal = Fraction(1)
        for j in range(1, n + 1):
            diagonal.append(detmatriz.at(j + i, j))
            valor_diagonal *= detmatriz.at(j + i, j)
        funnel(latex.text(f"Diagonal positiva #{i+1}: "), " ",
               " ".join(latex.fraction(x) for x in diagonal),
               " = ", latex.fraction(valor_diagonal), latex.newline())
        suma_diagonales_positivas += valor_diagonal

    # Ahora la de las diagonales negativas
    suma_diagonales_negativas = Fraction(0)

    for i in range(0, n):
        diagonal = []
        valor_diagonal = Fraction(1)
        for j in range(1, n + 1):
            diagonal.append(detmatriz.at(j + i, n - j + 1))
            valor_diagonal *= detmatriz.at(j + i, n - j + 1)
        funnel(latex.text(f"Diagonal negativa #{i+1}: "), " ",
               " ".join(latex.fraction(x) for x in diagonal),
               " = ", latex.fraction(valor_diagonal), latex.newline())
        suma_diagonales_negativas += valor_diagonal

    return suma_diagonales_positivas - suma_diagonales_negativas


def determinante_por_cofactores(matriz: Matriz, iteration: int = 0) -> Fraction:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener el determinante de una matriz no cuadrada")

    def printmat():
        return latex.matrix(matriz)

    n = matriz.filas
    funnel(latex.text(("|" * iteration) + " Calculando determinante (cofactores) de:"),
           latex.newline(), printmat(), latex.newline())

    # El determinante de una matriz de 1 x 1 es el valor de su unico elemento
    if n == 1:
        funnel(latex.text(("|" * iteration) + " Matriz 1x1: det = "),
               latex.fraction(matriz.at(1, 1)), latex.newline())
        return matriz.at(1, 1)

    suma: Fraction = Fraction(0)
    componentes: list[Fraction] = []

    for i in range(1, matriz.columnas + 1):
        valor = matriz.at(1, i)
        # signo del cofactor: (-1)^(1+i)
        inv = Fraction((-1) ** (1 + i))

        # si el elemento es 0, no aporta al determinante (evitamos trabajo extra)
        if valor == 0:
            continue

        # construimos el menor (removiendo columna i y la fila 1)
        mat = remover_fila(remover_columna(matriz, i), 1)
        funnel(latex.text(("|" * iteration) +
               f" Cofactor (1,{i})"), latex.newline(), latex.matrix(mat), latex.newline())
        det = determinante_por_cofactores(mat, iteration=iteration + 1)
        funnel(latex.text(("|" * iteration) + " Termino:"), " ",
               latex.fraction(valor), latex.cdot(), latex.text(
                   f"(-1)^{{{1 + i}}}"), latex.cdot(), latex.fraction(det),
               " = ", latex.fraction(valor * inv * det), latex.newline())
        suma += valor * inv * det
        componentes.append(valor * inv * det)

    funnel(latex.text(("|" * iteration) + " Resultado det:"),
           " ",
           " + ".join(latex.fraction(x) for x in componentes),
           " = ", latex.fraction(suma), latex.newline())
    return suma


def matriz_adjunta(matriz: Matriz) -> Matriz:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener la adjunta de una matriz no cuadrada")

    n = matriz.filas
    mat = Matriz(n, n)

    funnel(latex.text("Calculando matriz adjunta de:"),
           latex.newline(), latex.matrix(matriz), latex.newline())

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            inv = (-1) ** (i + j)
            co = cofactor(matriz, i, j)
            funnel(latex.text(f"Cofactor ({i},{j})"), latex.newline(
            ), latex.matrix(co), latex.newline())
            det = determinante_por_cofactores(co)
            mat.set(i, j, det * inv)
            funnel(latex.text(f"C{i}{j} = det(cof) * (-1)^{{{i + j}}} = "),
                   latex.fraction(det * inv), latex.newline())

    funnel(latex.text("Matriz adjunta obtenida:"),
           latex.newline(), latex.matrix(mat), latex.newline())
    return mat


def inversion_por_adjunta(matriz: Matriz) -> Matriz:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede invertir una matriz no cuadrada")

    funnel(latex.text("Inversa por adjunta"), latex.newline(),
           latex.matrix(matriz), latex.newline())
    det = determinante_por_cofactores(matriz)

    if det == 0:
        raise Exception(f"La matriz no es invertible.")

    # Calculamos la matriz adjunta
    adj = matriz_adjunta(matriz)

    funnel(latex.text("Transponiendo adjunta"), latex.newline())
    # La trasponemos
    trasp = transponer_matriz(adj)
    funnel(latex.text("Matriz traspuesta:"), latex.newline(), latex.matrix(trasp), latex.newline(),
           latex.text("Multiplicando por 1/det"), " = ", latex.fraction(Fraction(1, 1) / det), latex.newline())

    return matriz_por_escalar(trasp, 1/det)


def hacer_matriz_identidad(tamaño: int) -> Matriz:
    nueva_matriz = Matriz(tamaño, tamaño)

    for fila in range(1, tamaño + 1):
        for columna in range(1, tamaño + 1):
            if fila == columna:
                nueva_matriz.set(fila, columna, Fraction(1))
            else:
                nueva_matriz.set(fila, columna, Fraction(0))

    return nueva_matriz


def slice_matriz(mat: Matriz, rango_filas: tuple[int, int], rango_columnas: tuple[int, int]) -> Matriz:
    nueva_matriz = Matriz(
        rango_filas[1] - rango_filas[0] + 1, rango_columnas[1] - rango_columnas[0] + 1)

    for fila in range(rango_filas[0], rango_filas[1] + 1):
        for columna in range(rango_columnas[0], rango_columnas[1] + 1):
            nueva_matriz.set(
                fila - rango_filas[0] + 1, columna - rango_columnas[0] + 1, mat.at(fila, columna))

    return nueva_matriz

# OPERACIONES DE VECTORES


def suma_vectores(vectorA: Vector, vectorB: Vector):
    # Ver compatibilidad
    if vectorA.dimension != vectorB.dimension:
        raise Exception(
            f"No se puede sumar un vector de dimension {vectorA.dimension} con un vector de dimension {vectorB.dimension}")

    funnel(latex.text("Sumando vectores"), latex.newline(), latex.vector(
        vectorA), " + ", latex.vector(vectorB), latex.newline())
    componentes = []
    for i in range(1, vectorA.dimension + 1):
        a = vectorA.at(i)
        b = vectorB.at(i)
        r = a + b
        funnel(latex.fraction(a), " + ", latex.fraction(b),
               " = ", latex.fraction(r), latex.newline())
        componentes.append(r)

    return Vector(componentes)


def resta_vectores(vectorA: Vector, vectorB: Vector):
    # Ver compatibilidad
    if vectorA.dimension != vectorB.dimension:
        raise Exception(
            f"No se puede sumar un vector de dimension {vectorA.dimension} con un vector de dimension {vectorB.dimension}")

    funnel(latex.text("Restando vectores"), latex.newline(), latex.vector(
        vectorA), " - ", latex.vector(vectorB), latex.newline())
    componentes = []
    for i in range(1, vectorA.dimension + 1):
        a = vectorA.at(i)
        b = vectorB.at(i)
        r = a - b
        funnel(latex.fraction(a), " - ", latex.fraction(b),
               " = ", latex.fraction(r), latex.newline())
        componentes.append(r)

    return Vector(componentes)


def vector_por_escalar(vector: Vector, escalar):
    funnel(latex.text("Escalando vector por "), latex.fraction(a_fraccion(
        escalar)), latex.newline(), latex.vector(vector), latex.newline())
    componentes = []

    for i in range(1, vector.dimension + 1):
        v = vector.at(i)
        r = v * a_fraccion(escalar)
        funnel(latex.fraction(v), latex.cdot(), latex.fraction(
            a_fraccion(escalar)), " = ", latex.fraction(r), latex.newline())
        componentes.append(r)

    return Vector(componentes)


def matriz_por_vector(matriz, vector):
    """
    Multiplica una matriz por un vector.
    matriz: instancia de Matriz (n x m)
    vector: instancia de Vector (m x 1)
    Retorna un nuevo Vector con el resultado (n x 1).

    El resultado es un vector donde cada componente es el producto escalar de la fila correspondiente de la matriz por el vector.
    Ejemplo:
    Si matriz = [[a, b], [c, d]] y vector = [x, y],
    entonces matriz_por_vector(matriz, vector) = [a*x + b*y, c*x + d*y]
    """
    # Verificar compatibilidad de dimensiones
    if matriz.columnas != vector.dimension:
        raise Exception(
            "Las dimensiones no son compatibles para la multiplicación.")
    funnel(latex.text("Multiplicando matriz por vector"), latex.newline(),
           latex.matrix(matriz), latex.cdot(), latex.vector(vector), latex.newline())
    resultado = []
    # Para cada fila de la matriz
    for i in range(1, matriz.filas + 1):
        suma = Fraction(0)
        elementos: list[Fraction] = []
        # Multiplicamos cada elemento de la fila por el correspondiente del vector
        funnel(latex.text(f"Fila {i} · vector"), latex.newline())
        for j in range(1, matriz.columnas + 1):
            prod = matriz.at(i, j) * vector.at(j)
            funnel(latex.fraction(matriz.at(i, j)), latex.cdot(), latex.fraction(
                vector.at(j)), " = ", latex.fraction(prod), latex.newline())
            suma += prod
            elementos.append(prod)

        funnel(" + ".join(latex.fraction(elem) for elem in elementos),
               " = ", latex.fraction(suma), latex.newline())
        resultado.append(suma)
    # Retornamos el vector resultado
    return Vector(resultado)

# Crear matrices


def crear_matriz_identidad(tamaño: int):
    # Creamos la matriz del tamaño pedido
    # Nueva matriz
    nueva_matriz: Matriz = Matriz(tamaño, tamaño)

    # La matriz se inicializa en 0s, asi que vamos a ir poniendo 1s en la diagonal
    for i in range(1, tamaño + 1):
        # En la posicion i, i durante la diagonal vamos poniendo 1s
        nueva_matriz.set(i, i, 1)

    return nueva_matriz
