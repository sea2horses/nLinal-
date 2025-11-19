from py.functions.models.matriz import Matriz
from py.functions.models.vector import Vector
from fractions import Fraction

import py.functions.operations.operaciones as op
from py.functions.operations.operaciones import funnel
import py.functions.utils.latex as latex
from py.functions.utils.auxiliar import a_fraccion

# Clases auxiliares simples


class Posicion:
    def __init__(self, fila: int, columna: int):
        self.fila = fila
        self.columna = columna

    def __str__(self):
        return f"({self.fila}, {self.columna})"


# Pasos
__pasos__ = 0


def resetear_pasos():
    global __pasos__
    __pasos__ = 0


def imprimir_paso(texto_paso: str, mat: Matriz | None = None):
    global __pasos__
    __pasos__ += 1
    funnel(latex.text(f"Paso #{__pasos__}: {texto_paso}"))


def paso():
    global __pasos__
    __pasos__ += 1
    funnel(latex.text(f"Paso #{__pasos__}"), latex.newline())


def matriz_escalonada_reducida(mat: Matriz, filas: int, columnas: int):
    fila_pivote = 0
    columna_pivote = 0

    funnel(latex.text(
        "Reduciendo matriz a forma escalonada reducida..."), latex.newline())

    while fila_pivote < filas and columna_pivote < columnas:
        fila_pivote += 1
        columna_pivote += 1

        pivote: Fraction = Fraction(0)

        while pivote == 0 and columna_pivote <= columnas:
            pivote = mat.at(fila_pivote, columna_pivote)

            if pivote != 0:
                break

            encontrado: bool = False
            for i in range(fila_pivote + 1, filas + 1):
                if mat.at(i, columna_pivote) != 0:
                    encontrado = True
                    imprimir_paso(
                        f"Intercambio de filas")
                    op.intercambiar_fila(mat, fila_pivote, i)
                    funnel(latex.newline(), latex.matrix(mat), latex.newline())
                    pivote = mat.at(fila_pivote, columna_pivote)
                    break

            if not encontrado:
                columna_pivote += 1
                if columna_pivote > columnas:
                    return
                pivote = mat.at(fila_pivote, columna_pivote)

        if columna_pivote > columnas:
            return

        if pivote != 1:
            imprimir_paso(
                f"Normalizar fila: ")
            op.escalar_fila(mat, fila_pivote, Fraction(1) / pivote)
            funnel(latex.newline(), latex.matrix(mat), latex.newline())

        for i in range(fila_pivote + 1, filas + 1):
            factor: Fraction = mat.at(i, columna_pivote)
            if factor == 0:
                continue

            imprimir_paso(
                f"Resta compuesta: ")
            op.restar_escalar_fila(mat, Fraction(1), i, factor, fila_pivote)
            funnel(latex.newline(), latex.matrix(mat), latex.newline())

        for i in range(1, fila_pivote):
            factor: Fraction = mat.at(i, columna_pivote)
            if factor == 0:
                continue
            imprimir_paso(
                f"Resta compuesta: ")
            op.restar_escalar_fila(mat, Fraction(1), i, factor, fila_pivote)
            funnel(latex.newline(), latex.matrix(mat), latex.newline())


def obtener_pivotes(mat: Matriz, filas: int, columnas: int):
    pivotes: list[Posicion] = []
    fila_actual = 1

    for c in range(1, columnas + 1):
        pivote: Fraction = mat.at(fila_actual, c)
        if pivote == 0:
            continue
        if pivote != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posición de pivote")
        else:
            pivotes.append(Posicion(fila_actual, c))
        fila_actual += 1
        if fila_actual > filas:
            return pivotes

    return pivotes


def matriz_identidad(mat: Matriz, filas: int, columnas: int):
    fila_actual = 1

    funnel(latex.text("Reduciendo matriz a identidad..."), latex.newline())

    for c in range(1, columnas + 1):
        pivote: Fraction = mat.at(fila_actual, c)
        if pivote == 0:
            continue
        if pivote != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posición de pivote")

        for f in range(1, fila_actual):
            factor: Fraction = mat.at(f, c)
            if factor == 0:
                continue
            imprimir_paso(
                f"Resta compuesta: ")
            op.restar_escalar_fila(mat, Fraction(1), f, factor, fila_actual)
            funnel(latex.newline(), latex.matrix(mat), latex.newline())

        fila_actual += 1
        if fila_actual > filas:
            return


def resolver_sistema(mat: Matriz, ecuaciones: int, incognitas: int):
    """
    Resuelve un sistema de ecuaciones lineales (AX=B o AX=0)
    """
    resetear_pasos()

    if mat.filas != ecuaciones:
        raise Exception(
            "La cantidad de filas no coincide con la cantidad de ecuaciones")
    if mat.columnas != incognitas + 1:
        raise Exception(
            f"La cantidad de columnas esperada era: {incognitas + 1}, pero la dada fue: {mat.columnas}")
    columna_resultados: int = incognitas + 1
    mat.linea = incognitas

    es_homogeneo = True
    for i in range(1, ecuaciones+1):
        if mat.at(i, columna_resultados) != 0:
            es_homogeneo = False
            break
    tipo_sistema = "homogéneo" if es_homogeneo else "no homogéneo"

    mat.linea = incognitas
    
    funnel(latex.text(f"Iniciando resolución del sistema {tipo_sistema}."))

    funnel(latex.newline(), latex.matrix(mat), latex.newline())

    matriz_escalonada_reducida(mat, ecuaciones, incognitas)

    pivotes: list[Posicion] = obtener_pivotes(mat, ecuaciones, incognitas)
    num_pivotes = len(pivotes)
    funnel(latex.text(
        f"El sistema contiene {num_pivotes} pivotes."), latex.newline())

    funnel(latex.text("Matriz en forma Escalonada Reducida:"),
           latex.newline(), latex.matrix(mat), latex.newline(), latex.newline())
    funnel(latex.text(f"El sistema es {tipo_sistema}."), latex.newline())

    inconsistente = False
    for fila in range(1, ecuaciones + 1):
        fila_nula: bool = True
        for columna in range(1, incognitas + 1):
            if mat.at(fila, columna) != 0:
                fila_nula = False
                break
        if fila_nula and mat.at(fila, columna_resultados) != 0:
            inconsistente = True
            funnel(latex.text(
                "El sistema es inconsistente. No tiene solución"), latex.newline())
            return

    matriz_identidad(mat, ecuaciones, incognitas)
    funnel(latex.text("Matriz en forma identidad:"), latex.newline(),
           latex.matrix(mat), latex.newline(), latex.newline())
    funnel(latex.text(f"El sistema es {tipo_sistema}."), latex.newline())

    if num_pivotes == incognitas:
        funnel(latex.text(
            "El sistema es consistente con una solución única."), latex.newline())
        if op.columna_nula(mat, columna_resultados):
            funnel(latex.text(
                "El sistema contiene una única solución trivial. (linealmente independiente)"), latex.newline())
        else:
            funnel(latex.text(
                "El sistema contiene una única solución no trivial. (linealmente dependiente)"), latex.newline())
    elif num_pivotes < incognitas:
        funnel(latex.text(
            "El sistema es consistente con infinitas soluciones."), latex.newline())
        funnel(latex.text(
            "El sistema tiene infinitas soluciones no triviales. (linealmente dependiente)"), latex.newline())
    else:
        funnel(latex.text("El sistema es consistente."), latex.newline())

    variables: list[int | None] = [None] * incognitas
    for pivote in pivotes:
        variables[pivote.columna - 1] = pivote.fila

    funnel(latex.text(
        f"El sistema contiene {num_pivotes} pivotes."), latex.newline())

    columnas_pivote: list[int] = []
    for i in range(0, len(pivotes)):
        funnel(latex.text(f"Pivote #{i + 1}: {pivotes[i]}"), latex.newline())
        if pivotes[i].columna not in columnas_pivote:
            columnas_pivote.append(pivotes[i].columna)
    funnel(latex.text(f"Columnas pivote: {columnas_pivote}"), latex.newline())

    if num_pivotes == incognitas:
        funnel(latex.text("El sistema tiene una única solución:"),
               latex.newline(), latex.newline())
        for i in range(1, incognitas + 1):
            x_val = mat.at(i, columna_resultados)
            funnel("x", latex.subscript(str(i)),
                   " = ", latex.fraction(x_val), latex.newline())
    else:
        funnel(latex.text("El sistema tiene infinitas soluciones (forma paramétrica):"),
               latex.newline(), latex.newline())
        for i in range(0, len(variables)):
            fila_variable = variables[i]
            if fila_variable is None:
                funnel("x", latex.subscript(
                    str(i + 1)),
                    latex.text(" es libre")
                    , latex.newline())
            else:
                resultado = mat.at(fila_variable, columna_resultados)
                eq_parts = []
                eq_parts.append("x" + latex.subscript(str(i + 1)) + " = ")

                primer_termino = True
                if resultado != 0:
                    eq_parts.append(latex.fraction(resultado))
                    primer_termino = False

                for columna in range(1, incognitas + 1):
                    if columna == i + 1:
                        continue
                    coeficiente = mat.at(fila_variable, columna) * -1
                    if coeficiente != 0:
                        if not primer_termino:
                            eq_parts.append(" + " if coeficiente >= 0 else " ")
                        else:
                            primer_termino = False

                        if abs(coeficiente) == 1:
                            coef_str = "" if coeficiente == 1 else "-"
                        else:
                            coef_str = latex.fraction(coeficiente)
                        eq_parts.append(coef_str + "x" +
                                        latex.subscript(str(columna)))

                funnel("".join(eq_parts), latex.newline())

    funnel(latex.text("Clasificación: Consistente."), latex.newline())


def calcular_inversa(mat: Matriz, tamaño: int):
    if mat.filas != tamaño or mat.columnas != tamaño:
        funnel(latex.text("La matriz debe ser cuadrada!"), latex.newline())
        return

    funnel(latex.text("=============================================="),
           latex.newline())
    funnel(latex.text("      MATRIZ INVERSA"), latex.newline())
    funnel(latex.text("=============================================="),
           latex.newline(), latex.newline())

    matriz_completa = Matriz(tamaño, tamaño * 2)
    identidad = op.hacer_matriz_identidad(tamaño)

    for fila in range(1, tamaño + 1):
        for columna in range(1, tamaño + 1):
            matriz_completa.set(fila, columna, mat.at(fila, columna))
            matriz_completa.set(fila, columna + tamaño,
                                identidad.at(fila, columna))

    funnel(latex.text("Matriz aumentada inicial:"), latex.newline(),
           latex.matrix(matriz_completa), latex.newline())

    resetear_pasos()
    matriz_escalonada_reducida(matriz_completa, tamaño, tamaño)

    pivotes: list[Posicion] = obtener_pivotes(matriz_completa, tamaño, tamaño)

    funnel(latex.newline(), latex.text(
        "--- Propiedades teóricas sobre invertibilidad ---"), latex.newline())

    funnel(latex.text(
        f"(c) Pivotes encontrados: {len(pivotes)} de {tamaño}"), latex.newline())
    if len(pivotes) == tamaño:
        funnel(latex.text(
            "Interpretación: A tiene n pivotes, entonces A es invertible."), latex.newline())
    else:
        funnel(latex.text(
            "Interpretación: A no tiene n pivotes, entonces A no es invertible."), latex.newline())

    funnel(latex.text(
        "(d) Resolviendo Ax = 0 para verificar soluciones..."), latex.newline())
    matriz_homogenea = Matriz(tamaño, tamaño + 1)
    for fila in range(1, tamaño + 1):
        for columna in range(1, tamaño + 1):
            matriz_homogenea.set(fila, columna, mat.at(fila, columna))
    funnel(latex.text("Matriz aumentada [A | 0]:"), latex.newline(
    ), latex.matrix(matriz_homogenea), latex.newline())
    funnel(latex.text("Resolviendo a identidad..."), latex.newline())
    matriz_escalonada_reducida(matriz_homogenea, tamaño, tamaño)
    pivotes_homogenea = obtener_pivotes(matriz_homogenea, tamaño, tamaño)
    if len(pivotes_homogenea) == tamaño:
        funnel(latex.text(
            "Interpretación: Ax = 0 solo tiene la solución trivial, entonces A⁻¹ existe."), latex.newline())
    else:
        funnel(latex.text(
            "Interpretación: Ax = 0 tiene soluciones no triviales, entonces A⁻¹ no existe."), latex.newline())

    funnel(latex.text(
        "(e) Verificando independencia lineal de las columnas de A..."), latex.newline())
    if len(pivotes) == tamaño:
        funnel(latex.text(
            "Interpretación: Las columnas de A son linealmente independientes, entonces A es invertible."), latex.newline())
    else:
        funnel(latex.text(
            "Interpretación: Las columnas de A no son linealmente independientes, entonces A no es invertible."), latex.newline())

    parte_izquierda = op.slice_matriz(
        matriz_completa, (1, tamaño), (1, tamaño))

    if parte_izquierda == identidad:
        inversa = op.slice_matriz(
            matriz_completa, (1, tamaño), (tamaño + 1, tamaño * 2))
        funnel(latex.text("La matriz es no singular (determinante diferente de 0) y su inversa es:"),
               latex.newline(), latex.matrix(inversa), latex.newline())

        funnel(latex.newline(), latex.text(
            "Verificación (A · A⁻¹):"), latex.newline())
        verificacion = op.multiplicar_matrices(mat, inversa)
        funnel(latex.matrix(verificacion), latex.newline())
    else:
        funnel(latex.text(
            "La matriz es singular (determinante es 0) y no tiene inversa"), latex.newline())
        funnel(latex.text("Parte izquierda resultante:"), latex.newline(),
               latex.matrix(parte_izquierda), latex.newline())


def combinacion_lineal(dimension: int, vectores: list[Vector], resultado: Vector):
    incognitas = len(vectores)
    ecuaciones = dimension

    matriz: Matriz = Matriz(ecuaciones, incognitas + 1)

    for columna in range(0, incognitas):
        vector = vectores[columna]
        for indice in range(1, dimension + 1):
            matriz.set(indice, columna + 1, vector.at(indice))

    for result in range(1, resultado.dimension + 1):
        matriz.set(result, incognitas + 1, resultado.at(result))

    funnel(latex.text("=============================================="),
           latex.newline())
    funnel(latex.text("      COMBINACIÓN LINEAL DE VECTORES"), latex.newline())
    funnel(latex.text("=============================================="),
           latex.newline(), latex.newline())

    funnel(latex.newline(), latex.text("Matriz del sistema planteado:"),
           latex.newline(), latex.newline(), latex.matrix(matriz), latex.newline())

    funnel(latex.newline(), latex.text("=== Resolución del sistema ==="),
           latex.newline(), latex.newline())
    resolver_sistema(matriz, ecuaciones, incognitas)
    funnel(latex.newline(), latex.text(
        "=============================================="), latex.newline(), latex.newline())

    funnel(latex.text("Planteando el sistema como combinación lineal:"),
           latex.newline(), latex.newline())
    eq_parts = ["  "]
    for i, v in enumerate(vectores):
        coef = "X" + latex.subscript(str(i+1))
        eq_parts.append(coef + latex.cdot() + latex.vector(v))
        if i < len(vectores) - 1:
            eq_parts.append(" + ")
    eq_parts.append(" = " + latex.vector(resultado))
    funnel("".join(eq_parts), latex.newline())


def resolver_ecuacion_matricial(A: Matriz, B: Matriz):
    """
    Resuelve la ecuación matricial AX = B
    """
    if A.filas != A.columnas:
        raise Exception("La matriz A debe ser cuadrada")
    n = A.filas

    if B.filas != n:
        raise Exception("El número de filas de B debe coincidir con las de A")

    m = B.columnas

    aumentada = Matriz(n, n + m)

    for i in range(1, n + 1):
        for j in range(1, n + 1):
            aumentada.set(i, j, A.at(i, j))

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            aumentada.set(i, n + j, B.at(i, j))

    funnel(latex.text("Matriz aumentada [A | B]:"), latex.newline(
    ), latex.matrix(aumentada), latex.newline())

    resetear_pasos()
    funnel(latex.newline(), latex.text(
        "=== Aplicando eliminación de Gauss-Jordan ==="), latex.newline())
    matriz_escalonada_reducida(aumentada, n, n)
    matriz_identidad(aumentada, n, n)

    X = Matriz(n, m)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            valor = aumentada.at(i, n + j)
            X.set(i, j, valor)

    funnel(latex.newline(), latex.text("=== Solución X ==="),
           latex.newline(), latex.matrix(X), latex.newline())

    return X


def dependencia_lineal(dimension: int, vectores: list[Vector]) -> None:
    """
    Determina si un conjunto de vectores es linealmente dependiente o independiente.
    """
    num_vectores = len(vectores)

    if num_vectores > dimension:
        funnel(latex.text(
            f"Paso 1: Más vectores ({num_vectores}) que la dimensión ({dimension}): Dependientes por teorema."), latex.newline())
        funnel(latex.newline(), latex.text(
            "Los vectores ingresados son linealmente dependientes."), latex.newline())
        funnel(latex.newline(), latex.text(
            "=============================================="), latex.newline())
        return

    matriz: Matriz = Matriz(dimension, num_vectores + 1)
    for col in range(1, num_vectores + 1):
        vec = vectores[col - 1]
        for row in range(1, dimension + 1):
            matriz.set(row, col, vec.at(row))
            matriz.set(row, num_vectores + 1, Fraction(0))

    funnel(latex.text("=============================================="),
           latex.newline())
    funnel(latex.text("      DEPENDENCIA LINEAL DE VECTORES"), latex.newline())
    funnel(latex.text("=============================================="),
           latex.newline(), latex.newline())

    funnel(latex.newline(), latex.text("Matriz del sistema homogéneo planteado:"),
           latex.newline(), latex.newline(), latex.matrix(matriz), latex.newline())

    eq_parts = ["Paso 1: Planteo: "]
    for i, vec in enumerate(vectores, 1):
        coef = "c" + latex.subscript(str(i))
        eq_parts.append(coef + latex.cdot() + latex.vector(vec))
        if i < len(vectores):
            eq_parts.append(" + ")
    eq_parts.append(" = 0")
    funnel("".join(eq_parts), latex.newline(), latex.newline())

    funnel(latex.text("=== Resolución del sistema homogéneo ==="),
           latex.newline(), latex.newline())
    resolver_sistema(matriz, dimension, num_vectores)

    pivotes = obtener_pivotes(matriz, dimension, num_vectores)
    if len(pivotes) == num_vectores:
        funnel(latex.text(
            "Solo solución trivial (c₁=0, ..., cₙ=0): Los vectores son linealmente independientes."), latex.newline())
    else:
        funnel(latex.text(
            "Existen soluciones no triviales: Los vectores son linealmente dependientes."), latex.newline())

    funnel(latex.newline(), latex.text(
        "=============================================="), latex.newline())
