# Multiplica una matriz (n x m) por un vector (m x 1)
from matriz import Matriz
from vector import Vector
from fractions import Fraction
from auxiliar import a_fraccion, pretty_print_matrix
from ecuacion import Ecuacion, Termino

# Aqui en este archivo van todas las operaciones sobre matrices
# Operaciones basicas en una fila

# Escala una fila por un numero
# a la fila [1][2][3] * 3 -> [3][6][9]
# f -> e*f


def escalar_fila(mat: Matriz, fila: int, escalar):
    # Ciclamos por las columnas en la fila
    for i in range(1, mat.columnas + 1):
        nuevo_valor: Fraction = mat.at(fila, i) * a_fraccion(escalar)
        # En la posicion [fila, i] vamos a cambiar el valor por el mismo pero multiplicado por el escalar
        mat.set(fila, i, nuevo_valor)

# Sumar una fila B a una fila A
# el resultado queda guardado en A
# fa -> fa + fb


def sumar_fila(mat: Matriz, fila_a: int, fila_b: int):
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
    # Ciclamos por la fila A para cambiar los valores
    for i in range(1, mat.columnas + 1):
        # NUEVO VALor
        nuevo_valor: Fraction = escalar_a * \
            mat.at(fila_a, i) + escalar_b * mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# La misma operacion pero en resta


def restar_fila(mat: Matriz, fila_a: int, fila_b: int):
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
    # Ciclamos por la fila A para cambiar los valores
    for i in range(1, mat.columnas + 1):
        # NUEVO VALor
        nuevo_valor: Fraction = a_fraccion(escalar_a) * \
            mat.at(fila_a, i) - a_fraccion(escalar_b) * mat.at(fila_b, i)
        mat.set(fila_a, i, nuevo_valor)

# Intercambio de filas
# fa <-> fb


def intercambiar_fila(mat: Matriz, fila_a: int, fila_b: int):
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

    nueva_matriz: Matriz = Matriz(filas, columnas)

    # Cada cuadrado de la nueva matriz es el resultado de la suma de los numeros
    # en esa posicion en ambas matrices
    for fila in range(1, filas + 1):
        for columna in range(1, columnas + 1):
            nueva_matriz.set(fila, columna, matrizA.at(
                fila, columna) + matrizB.at(fila, columna))

    return nueva_matriz

# Resta dos matrices y devuelve una nueva con el resultado


def resta_matrices(matrizA: Matriz, matrizB: Matriz, calcprint: bool = False) -> Matriz:
    if matrizA.filas != matrizB.filas or matrizA.columnas != matrizB.columnas:
        raise Exception(
            f"No se puede restar una matriz de {matrizA.filas}x{matrizA.columnas} con una matriz de {matrizB.filas}x{matrizB.columnas}")

    # No importa tomar matriz a o matriz b porque ambas son del mismo tamaño
    filas = matrizA.filas
    columnas = matrizA.columnas

    nueva_matriz: Matriz = Matriz(filas, columnas)

    # Cada cuadrado de la nueva matriz es el resultado de la suma de los numeros
    # en esa posicion en ambas matrices
    for fila in range(1, filas + 1):
        for columna in range(1, columnas + 1):
            nueva_matriz.set(fila, columna, matrizA.at(
                fila, columna) - matrizB.at(fila, columna))

    return nueva_matriz


def matriz_por_escalar(matriz: Matriz, escalar: Fraction, calcprint: bool = False) -> Matriz:

    nueva_matriz: Matriz = Matriz(matriz.filas, matriz.columnas)

    for fila in range(1, matriz.filas + 1):
        for columna in range(1, matriz.columnas + 1):
            if calcprint:
                print(
                    f"{matriz.at(fila, columna)} * {escalar} = {matriz.at(fila, columna) * escalar}")
            nueva_matriz.set(fila, columna, matriz.at(fila, columna) * escalar)

    return nueva_matriz


def multiplicar_matrices(matrizA: Matriz, matrizB: Matriz, calcprint: bool = False) -> Matriz:
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
    nueva_matriz = Matriz(matrizA.filas, matrizB.columnas)

    # Paso 3: Recorrer todas las posiciones de la matriz resultado
    for i in range(1, matrizA.filas + 1):          # Recorre filas de A (1..m)
        for j in range(1, matrizB.columnas + 1):   # Recorre columnas de B (1..p)
            if calcprint:
                print(f"Elemento: {i}, {j}:")

            # Acumulador para el producto escalar fila_i(A) · columna_j(B)
            suma = 0

            # Paso 3.1: Calcular el producto escalar
            # k recorre los índices compartidos (1..n)

            # Entonces aca, por ejemplo, en la fila 1, columna 1
            # vas a querer recorrer las posiciones:

            # (1, 1) * (1, 1)
            # (1, 2) * (2, 1)
            # (1, 3) * (3, 1)
            # y sumarlas todas
            # Veanse este video https://www.youtube.com/watch?v=7E_VvhYvJgU
            if calcprint:
                print(
                    f"-- Sumamos los productos de la fila {i} ({list(str(frac) for frac in matrizA.row(i))}) en la matriz 1 y la columna {j} ({list(str(frac) for frac in matrizB.column(j))}) en la matriz 2")

            ecuacion = Ecuacion()
            for k in range(1, matrizA.columnas + 1):
                suma += matrizA.at(i, k) * matrizB.at(k, j)
                if calcprint:
                    print(
                        f"{matrizA.at(i, k)} * {matrizB.at(k, j)} = {matrizA.at(i, k) * matrizB.at(k, j)}")
                ecuacion.agregar_termino(
                    Termino(f"{matrizA.at(i, k) * matrizB.at(k, j)}"))
            ecuacion.agregar_termino(Termino(suma), "derecho")

            if calcprint:
                print(ecuacion)

            # Paso 4: Asignar el valor calculado a la celda (i, j) del resultado
            nueva_matriz.set(i, j, suma)

    # Paso 5: Devolver la matriz resultante
    return nueva_matriz


def transponer_matriz(matriz: Matriz, calcprint: bool = False) -> Matriz:
    nueva_matriz = Matriz(matriz.columnas, matriz.filas)

    for fila in range(1, matriz.filas + 1):
        if calcprint:
            print(
                f"La fila {fila} pasa a ser la columna {fila}: {matriz.row(fila)}")
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
                print(
                    f"Invirtiendo diagonal {fila}, {columna} con {matriz.filas - fila + 1}, {matriz.columnas - columna + 1}")
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

def determinante_por_sarrus(matriz: Matriz, calcprint: bool = False) -> Fraction:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener el determinante de una matriz no cuadrada")

    n = matriz.filas
    if n != 3:
        raise Exception(
            f"El metodo de sarrus solo es válido para matrices 3x3")

    if calcprint:
        print(f"Calculando determinante de la matriz: \n{matriz}")

    # --- Propiedades rápidas que anulan el determinante ---
    # 1) Si alguna fila o columna es nula -> det = 0
    for i in range(1, n + 1):
        if fila_nula(matriz, i):
            if calcprint:
                print(f"Fila {i} es nula -> det = 0")
            return Fraction(0)
        if columna_nula(matriz, i):
            if calcprint:
                print(f"Columna {i} es nula -> det = 0")
            return Fraction(0)

    # 2) Si existe par de filas o columnas proporcionales/iguales -> det = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if filas_proporcionales(matriz, i, j) is not None:
                if calcprint:
                    print(
                        f"Filas {i} y {j} son proporcionales/iguales -> det = 0")
                return Fraction(0)
            if columnas_proporcionales(matriz, i, j) is not None:
                if calcprint:
                    print(
                        f"Columnas {i} y {j} son proporcionales/iguales -> det = 0")
                return Fraction(0)

    # Para sarrus necesitamos agregar (n - 1) filas adicionales a una nueva matriz
    detmatriz = Matriz(n + (n - 1), n)

    for i in range(1, matriz.filas + 1):
        for j in range(1, matriz.columnas + 1):
            detmatriz.set(i, j, matriz.at(i, j))

    # Añadimos las copias de las filas adicionales
    for i in range(1, matriz.filas):
        for j in range(1, matriz.columnas + 1):
            detmatriz.set(n + i, j, matriz.at(i, j))

    if calcprint:
        print(f"Matriz de determinante expandida:\n{detmatriz}")

    # Ahora calculamos las diagonales positivas
    suma_diagonales_positivas = Fraction(0)

    for i in range(0, n):
        diagonal = []
        valor_diagonal = Fraction(1)
        for j in range(1, n + 1):
            diagonal.append(detmatriz.at(j + i, j))
            valor_diagonal *= detmatriz.at(j + i, j)
        if calcprint:
            print(
                f"Diagonal Positiva #{i + 1}: {list(str(x) for x in diagonal)} = {valor_diagonal}")
            suma_diagonales_positivas += valor_diagonal

    # Ahora la de las diagonales negativas
    suma_diagonales_negativas = Fraction(0)

    for i in range(0, n):
        diagonal = []
        valor_diagonal = Fraction(1)
        for j in range(1, n + 1):
            diagonal.append(detmatriz.at(j + i, n - j + 1))
            valor_diagonal *= detmatriz.at(j + i, n - j + 1)
        if calcprint:
            print(
                f"Diagonal Negativa #{i + 1}: {list(str(x) for x in diagonal)} = {valor_diagonal}")
            suma_diagonales_negativas += valor_diagonal

    return suma_diagonales_positivas - suma_diagonales_negativas


def determinante_por_cofactores(matriz: Matriz, calcprint: bool = False, iteration: int = 0) -> Fraction:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener el determinante de una matriz no cuadrada")

    def printmat():
        return pretty_print_matrix(matriz.matriz, additive=f"|{"\t" * iteration}")

    n = matriz.filas
    if calcprint:
        print(
            f"|{"\t" * iteration} Calculando determinante de la matriz: \n{printmat()}")

    # El determinante de una matriz de 1 x 1 es el valor de su unico elemento
    if n == 1:
        if calcprint:
            print(
                f"|{"\t" * iteration} El determinante de una matriz 1 x 1 es su unico elemento: {matriz.at(1, 1)}")
        return matriz.at(1, 1)

    # --- Propiedades rápidas que anulan el determinante ---
    # 1) Si alguna fila o columna es nula -> det = 0
    for i in range(1, n + 1):
        if fila_nula(matriz, i):
            if calcprint:
                print(f"Fila {i} es nula -> det = 0")
            return Fraction(0)
        if columna_nula(matriz, i):
            if calcprint:
                print(f"Columna {i} es nula -> det = 0")
            return Fraction(0)

    # 2) Si existe par de filas o columnas proporcionales/iguales -> det = 0
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            if filas_proporcionales(matriz, i, j) is not None:
                if calcprint:
                    print(
                        f"Filas {i} y {j} son proporcionales/iguales -> det = 0")
                return Fraction(0)
            if columnas_proporcionales(matriz, i, j) is not None:
                if calcprint:
                    print(
                        f"Columnas {i} y {j} son proporcionales/iguales -> det = 0")
                return Fraction(0)

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
        if calcprint:
            print(
                f"|{"\t" * iteration} Calculando cofactor ({1}, {i}):")
        # al calcular recursivamente, no queremos que los menores impriman sus pasos
        det = determinante_por_cofactores(
            mat, calcprint=True, iteration=iteration + 1)

        if calcprint:
            print(
                f"|{"\t" * iteration} Resultado: {valor} * -1^{1 + i} * {det} = {valor * inv * det}")
        suma += valor * inv * det
        componentes.append(valor * inv * det)

    if calcprint:
        print(
            f"|{"\t" * iteration}El determinante de la matriz: \n{printmat()} es: {str.join(" + ", list(str(x) for x in componentes))} = {suma}")
    return suma


def matriz_adjunta(matriz: Matriz, calcprint: bool = False) -> Matriz:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede obtener la adjunta de una matriz no cuadrada")

    n = matriz.filas
    mat = Matriz(n, n)

    if calcprint:
        print(f"Obteniendo matriz adjunta de:\n{matriz}")

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            inv = (-1) ** (i + j)
            co = cofactor(matriz, i, j)
            print(f"Obteniendo determinante del cofactor ({i}, {j})")
            det = determinante_por_cofactores(co, calcprint)

            mat.set(i, j, det * inv)
            print(f"Resultado C{i}{j} = {det} * -1^{i + j}")

    if calcprint:
        print(f"Matriz adjunta: \n{mat}")
    return mat


def inversion_por_adjunta(matriz: Matriz, calcprint: bool = False) -> Matriz:
    if matriz.filas != matriz.columnas:
        raise Exception(
            f"No se puede invertir una matriz no cuadrada")

    if calcprint:
        print(f"Calculando inversa por adjunta de la matriz: \n{matriz}")
    det = determinante_por_cofactores(matriz, calcprint)

    if det == 0:
        raise Exception(f"La matriz no es invertible.")

    # Calculamos la matriz adjunta
    adj = matriz_adjunta(matriz, calcprint)

    if calcprint:
        print(f"Transponiendo matriz adjunta...")
    # La trasponemos
    trasp = transponer_matriz(adj, calcprint)
    if calcprint:
        print(f"Matriz traspuesta:\n{trasp}")
        print(
            f"Ahora se multiplicará la traspuesta por el recíproco del determinante: {1 / det}")

    return matriz_por_escalar(trasp, 1/det, calcprint)


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

    componentes = []
    for i in range(1, vectorA.dimension + 1):
        componentes.append(vectorA.at(i) + vectorB.at(i))

    return Vector(componentes)


def resta_vectores(vectorA: Vector, vectorB: Vector):
    # Ver compatibilidad
    if vectorA.dimension != vectorB.dimension:
        raise Exception(
            f"No se puede sumar un vector de dimension {vectorA.dimension} con un vector de dimension {vectorB.dimension}")

    componentes = []
    for i in range(1, vectorA.dimension + 1):
        componentes.append(vectorA.at(i) - vectorB.at(i))

    return Vector(componentes)


def vector_por_escalar(vector: Vector, escalar):
    componentes = []

    for i in range(1, vector.dimension + 1):
        componentes.append(vector.at(i) * a_fraccion(escalar))

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
    resultado = []
    # Para cada fila de la matriz
    for i in range(1, matriz.filas + 1):
        suma = 0
        elementos: list[Fraction] = []
        # Multiplicamos cada elemento de la fila por el correspondiente del vector
        print(
            f"Multiplicamos la columna {i} de la matriz por cada elemento del vector:")
        for j in range(1, matriz.columnas + 1):
            print(
                f"Elemento ({i}, {j}) de la matriz * Elemento #{j} del vector")
            print(f"{matriz.at(i, j)} * {vector.at(j)}")
            suma += matriz.at(i, j) * vector.at(j)
            elementos.append(matriz.at(i, j) * vector.at(j))

        print(" + ".join(str(elem) for elem in elementos) + f" = {suma}")
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


# Revisa si una fila es proporcional a otra (excepto por 0)
def filas_proporcionales(mat: Matriz, fila_a: int, fila_b: int) -> Fraction | None:
    ra = mat.row(fila_a)
    rb = mat.row(fila_b)

    sv: Fraction = Fraction(0)

    for i in range(0, len(ra)):
        # Si alguna de las dos es cero pero no las dos, no puede ser escalable
        if (ra[i] == 0) != (rb[i] == 0):
            return None

        if sv == 0:
            # Obtener la escala
            sv = rb[i] / ra[i]
        else:
            # Ver si el elemento respeta la escala
            if ra[i] * sv != rb[i]:
                return None

    return sv


# Revisa si una fila es proporcional a otra (excepto por 0)
def columnas_proporcionales(mat: Matriz, columna_a: int, columna_b: int) -> Fraction | None:
    ra = mat.row(columna_a)
    rb = mat.row(columna_b)

    sv: Fraction = Fraction(0)

    for i in range(0, len(ra)):
        # Si alguna de las dos es cero pero no las dos, no puede ser escalable
        if (ra[i] == 0) != (rb[i] == 0):
            return None

        if sv == 0:
            # Obtener la escala
            sv = rb[i] / ra[i]
        else:
            # Ver si el elemento respeta la escala
            if ra[i] * sv != rb[i]:
                return None

    return sv
