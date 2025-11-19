from matriz import Matriz
from vector import Vector
from posicion import Posicion
from ecuacion import Ecuacion, Termino
from operaciones import *
from auxiliar import to_subscript

# Funcion para el output de los pasos
__pasos__ = 0


def resetear_pasos():
    global __pasos__
    __pasos__ = 0


def imprimir_paso(texto_paso: str, mat: Matriz | None = None):
    # Esta instructiva es para decirle a python
    # que la variable pasos no es de la funcion, si no
    # una global
    global __pasos__
    __pasos__ += 1
    matriz_string: str = ""
    if mat is not None:
        matriz_string += mat.__str__()
    print(f"Paso #{__pasos__}: {texto_paso} \n{matriz_string}\n")

# Esta funcion convierte cualquier matriz a su forma escalonada reducida, esta se puede usar
# como fase primera en el algoritmo gauss_jordan

# La cantidad de filas y columnas son la submatriz que se desea reducir a forma escalonada
# (por ejemplo, en un sistema de ecuaciones, queremos reducir toda la matriz excepto la ultima columna)


def matriz_escalonada_reducida(mat: Matriz, filas: int, columnas: int):
    # Vamos a ciclar por todas las columnas de la matriz
    fila_pivote = 0
    columna_pivote = 0

    print("Reduciendo matriz a forma escalonada reducida...")
    # Mientras estemos en los limites de la matriz
    while fila_pivote < filas and columna_pivote < columnas:
        # Nos movemos en la diagonal
        fila_pivote += 1
        columna_pivote += 1

        pivote: Fraction = Fraction(0)
        # Busquemos nuestro pivote
        while pivote == 0 and columna_pivote <= columnas:
            # Obtenemos el numero en la posicion pivote
            pivote = mat.at(fila_pivote, columna_pivote)
            # Si no esta vacia la posicion del pivote, todo bien, ese es nuestro pivote
            if pivote != 0:
                break
            # Si no, tenemos que buscar otro en la misma columna
            encontrado: bool = False
            for i in range(fila_pivote + 1, filas + 1):
                # Si encontramos un buen candidato
                if mat.at(i, columna_pivote) != 0:
                    encontrado = True
                    # Intercambiamos las filas
                    intercambiar_fila(mat, i, fila_pivote)
                    # Ahora el nuevo numero esta en la posicion pivote
                    pivote = mat.at(fila_pivote, columna_pivote)
                    # Imprimimos el paso
                    imprimir_paso(
                        f"Intercambio de filas, f{fila_pivote} <-> f{i}", mat)
                    break

            # Si no encontramos el pivote, revisemos la siguiente columna
            if not encontrado:
                columna_pivote += 1
                # Si ya nos pasamos de las columnas de la matriz
                # sin encontrar un nuevo pivote, nuestro trabajo esta hecho
                if columna_pivote > columnas:
                    return
                # Actualizamos el pivote para la nueva columna
                pivote = mat.at(fila_pivote, columna_pivote)

        # Si salimos del while porque nos quedamos sin columnas, terminamos
        if columna_pivote > columnas:
            return

        # Ahora normalizamos la fila
        if pivote != 1:
            escalar_fila(mat, fila_pivote, 1 / pivote)
            # Imprimimos el paso
            imprimir_paso(
                f"Normalizar fila {fila_pivote}, f{fila_pivote} -> {1 / pivote} * f{fila_pivote}", mat)

        # Y dejamos en 0 todas las filas abajo del pivote
        for i in range(fila_pivote + 1, filas + 1):
            # El factor es el numero que encontremos
            factor: Fraction = mat.at(i, columna_pivote)
            # Si el factor ya es 0, no necesitamos hacer nada
            if factor == 0:
                continue
            # Ahora multiplicamos la fila pivote por el factor y la restamos a la actual
            restar_escalar_fila(mat, 1, i, factor, fila_pivote)
            # Imprimimos el paso
            imprimir_paso(
                f"Resta compuesta: f{i} -> f{i} - ({factor}) * f{fila_pivote}", mat)

        # También eliminamos elementos por encima del pivote
        for i in range(1, fila_pivote):
            # El factor es el numero que encontremos
            factor: Fraction = mat.at(i, columna_pivote)
            # Si el factor ya es 0, no necesitamos hacer nada
            if factor == 0:
                continue
            # Restamos la fila pivote escalada
            restar_escalar_fila(mat, 1, i, factor, fila_pivote)
            # Imprimimos el paso
            imprimir_paso(
                f"Resta compuesta: f{i} -> f{i} - ({factor}) * f{fila_pivote}", mat)


def obtener_pivotes(mat: Matriz, filas: int, columnas: int):
    # Pivotes, son una tupla de 2 enteros
    # porque contienen informacion de su fila y columna
    pivotes: list[Posicion] = []
    # Ciclamos por todas las columnas
    fila_actual = 1

    for c in range(1, columnas + 1):
        # Obtenemos el pivote
        pivote: Fraction = mat.at(fila_actual, c)
        # Si es 0, saltamos la columna actual
        if pivote == 0:
            continue
        if pivote != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
        else:
            pivotes.append(Posicion(fila_actual, c))
        # Finalmente, seguimos en la escalera para la fila de abajo
        fila_actual += 1
        # Si nos pasamos de las filas de la matriz, terminamos
        if fila_actual > filas:
            return pivotes

    return pivotes

# Esta funcion transforma una matriz escalonada reducida a una matriz identidad
# Para que esta funcion, funcione, la matriz DEBE ser escalonada reducida,
# se puede reducir con la funcion matriz_escalonada_reducida

# La funcion sigue sirviendo si la matriz tiene multiples soluciones,
# esta funcion colapsara todas las variables basicas en todas las filas,
# dejando tan solo las variables libres


def matriz_identidad(mat: Matriz, filas: int, columnas: int):
    # Ciclamos por todas las columnas para ir reduciendo cada una
    fila_actual = 1

    print("Reduciendo matriz a identidad...")
    for c in range(1, columnas + 1):
        # Obtenemos el pivote
        pivote: Fraction = mat.at(fila_actual, c)
        # Si es 0, saltamos la columna actual
        if pivote == 0:
            continue
        # Si el pivote no es 1, nos mintieron, tiremos un error
        if pivote != 1:
            raise Exception(
                f"La matriz dada no es escalonada reducida, se encontró elemento: {pivote} en posicion de pivote")
        # Si no, actualizamos la fila
        # Ciclamos por todos los espacios arriba del pivote para reducirlas
        for f in range(1, fila_actual):
            # El factor es el numero que encontremos
            factor: Fraction = mat.at(f, c)
            # Si el factor ya es 0, no necesitamos hacer nada
            if factor == 0:
                continue
            # Ahora multiplicamos la fila pivote por el factor y la restamos a la actual
            # de esta manera, si nos encontramos 2, restamos 2 veces la fila principal, cuyo pivote es siempre 1
            # gracias a la normalizacion hecha previamente
            restar_escalar_fila(mat, 1, f, factor, fila_actual)
            # Imprimimos el paso
            imprimir_paso(
                f"Resta compuesta: f{f} -> f{f} - ({factor}) * f{fila_actual}", mat)
        # Finalmente, seguimos en la escalera para la fila de abajo
        fila_actual += 1
        # Si nos pasamos de las filas de la matriz, terminamos
        if fila_actual > filas:
            return

# Funcion para resolver un sistema de ecuaciones


def resolver_sistema(mat: Matriz, ecuaciones: int, incognitas: int):
    """
    Resuelve un sistema de ecuaciones lineales (AX=B o AX=0)
    Extendido para detectar automáticamente si es homogéneo (chequeando si la última columna es toda ceros).
    Reutiliza matriz_escalonada_reducida y obtener_pivotes para mostrar pasos y clasificar soluciones.
    Muestra transformación paso a paso, clasificación (consistente/inconsistente, única/infinita/ninguna),
    y soluciones paramétricas cuando corresponda. Para homogéneos, indica si la solución trivial es única.
    """
    resetear_pasos()

    # Primero revisamos que las medidas de la matriz coincidan con los numeros dados
    if mat.filas != ecuaciones:
        raise Exception(
            "La cantidad de filas no coincide con la cantidad de ecuaciones")
    if mat.columnas != incognitas + 1:
        raise Exception(
            f"La cantidad de columnas esperada era: {incognitas + 1}, pero la dada fue: {mat.columnas}")
    columna_resultados: int = incognitas + 1

    # Detectar si es homogéneo (ultima columna todas ceros). No afecta sistemas generales
    es_homogeneo = True
    for i in range(1, ecuaciones+1):
        if mat.at(i, columna_resultados) != 0:
            es_homogeneo = False
            break
    tipo_sistema = "homogéneo" if es_homogeneo else "no homogéneo"

    # Imprimir paso inicial con tipo de sistema y matriz
    imprimir_paso(
        f"Iniciando Resolución del sistema {tipo_sistema}. Matriz aumentada inicial:", mat)

    # Ahora, colapsamos la matriz a su version escalonada reducida
    matriz_escalonada_reducida(mat, ecuaciones, incognitas)

    # Obtener pivotes temprano para clasificación y saber cuantas variables libres tenemos
    pivotes: list[Posicion] = obtener_pivotes(mat, ecuaciones, incognitas)
    num_pivotes = len(pivotes)
    print(f"El sistema contiene {num_pivotes} pivotes.")

    print(f"Matriz en forma Escalonada Reducida:\n{mat}\n")

    print(f"El sistema es {tipo_sistema}.")
    # Ahora revisaremos si es consistente
    # Revisemos todas las ecuaciones para asegurarnos que no existe una
    # contradiccion
    # Agregamos un 1 por la exclusividad del rango,
    # Si hago un range(1, 5) el resultado es [1..4]
    # necesito agregarle 1 para que quede [1..5]
    inconsistente = False  # Rastrear inconsistencia
    for fila in range(1, ecuaciones + 1):
        # Revisar si la fila son solo ceros
        fila_nula: bool = True
        # Ciclamos hasta encontrar un elemento distinto de cero
        for columna in range(1, incognitas + 1):
            if mat.at(fila, columna) != 0:
                fila_nula = False
                break
        # Si la fila es nula, pero el resultado no, quiere decir que nos estamos contradiciendo,
        # por ende, el sistema es inconsistente
        if fila_nula and mat.at(fila, columna_resultados) != 0:
            inconsistente = True
            print("El sistema es inconsistente. No tiene solución")
            # Terminamos nuestro trabajo
            return

    # Convertir a matriz identidad para obtener resultados e imprimirla como paso intermedio
    matriz_identidad(mat, ecuaciones, incognitas)
    print(f"Matriz en forma identidad:\n{mat}\n")

    print(f"El sistema es {tipo_sistema}.")

    # Para homogéneos, mensaje sobre solución trivial (basado en pivotes).
    # if es_homogeneo:
    #     if num_pivotes == incognitas:
    #         print("El sistema homogéneo solo tiene la solución trivial.")
    #     else:
    #         print("El sistema homogéneo tiene soluciones no triviales (infinitas).")
    # Clasificación general basada en pivotes (consistente, única/infinita).
    if num_pivotes == incognitas:
        print("El sistema es consistente con una solución única.")

        if columna_nula(mat, columna_resultados):
            print(
                "El sistema contiene una unica solución trivial. (linealmente independiente)")
        else:
            print(
                "El sistema contiene una unica solución no trivial. (linealmente dependiente)")
    elif num_pivotes < incognitas:
        print("El sistema es consistente con infinitas soluciones.")
        print(
            "El sistema tiene infinitas soluciones no triviales. (linealmente dependiente)")
    else:
        print("El sistema es consistente.")  # Caso edge, aunque raro.

    # Si no, revisamos las variables libres y las variables basicas
    # Basicamente, si una variable es basica, anotamos su numero de fila
    # si una variable es libre, la apuntamos como None
    # Iniciamos todas en None, cuando los pivotes nos digan lo contrario,
    # marcamos la correspondiente con su fila
    # x1 es libre
    # x2 es basica
    variables: list[int | None] = [None] * incognitas
    # Asignar pivotes a variables basicas
    for pivote in pivotes:
        variables[pivote.columna - 1] = pivote.fila

    # Obtenemos los pivotes para saber cuantas variables libres tenemos
    print(f"El sistema contiene {num_pivotes} pivotes.")

    # Imprimir pivotes individuales
    columnas_pivote: list[int] = []
    for i in range(0, len(pivotes)):
        print(f"Pivote #{i + 1}: {pivotes[i]}")
        # Si la columna del pivote actual no esta en columnas_pivote, la agregamos
        if pivotes[i].columna not in columnas_pivote:
            columnas_pivote.append(pivotes[i].columna)
    print(f"Columnas pivote: {columnas_pivote}")

    # Si el numero de pivotes es igual a las incognitas, el sistema tiene una unica solucion
    # y no hay variables libres
    if num_pivotes == incognitas:
        print("\nEl sistema tiene una unica solución:\n")
        # Obtenemos los resultados de la columna de resultados
        for i in range(1, incognitas + 1):
            print(to_subscript(f"X{i} = ") +
                  f"{mat.at(i, columna_resultados)}")
    # De otra manera, imprimiremos el sistema con sus infinitas soluciones
    else:
        print("\nEl sistema tiene infinitas soluciones (forma paramétrica):\n")
        # Ahora imprimimos las variables basicas con sus condiciones, e imprimimos las variables libres
        for i in range(0, len(variables)):
            fila_variable = variables[i]
            # Si la variable es libre, es libre
            if fila_variable is None:
                print(to_subscript(f"X{i + 1} es libre"))
            else:
                ecuacion: Ecuacion = Ecuacion()
                # Agregamos la variable
                ecuacion.agregar_termino(Termino(1, to_subscript(f"X{i + 1}")))
                # Agregamos el numero primero
                resultado = mat.at(fila_variable, columna_resultados)
                if resultado != 0:
                    ecuacion.agregar_termino(
                        Termino(resultado), lado="derecho")

                # Agregamos el resto de variables como negativo (ya que quedarian con el signo volteado)
                for columna in range(1, incognitas + 1):
                    # Si la columna es la variable, nos la saltamos
                    if columna == i + 1:
                        continue
                    # Si hay un coeficiente, escribimos
                    coeficiente = mat.at(fila_variable, columna) * -1
                    ecuacion.agregar_termino(
                        Termino(coeficiente, to_subscript(f"X{columna}")), lado="derecho")
                # Imprimimos la variable con su ecuación
                print(ecuacion)

                # # De otra manera, vamos a imprimir la ecuacion para la variable
                # ecuacion: str = to_subscript(f"X{i + 1} = ")
                # # Agregamos el numero primero
                # resultado = mat.at(fila_variable, columna_resultados)
                # # Esta variable nos indica cuando ya no es el primer termino, y no necesitamos ubicar el primer +
                # primer_termino: bool = True
                # # Si no es 0, lo agregamos a la ecuacion
                # if resultado != 0:
                #     ecuacion += termino_a_string(coeficiente=resultado,
                #                                  variable=None, es_primer_termino=primer_termino)
                #     primer_termino = False
                # # Despues, agregamos el resto de variables como negativo (ya que quedarian con el signo volteado)
                # # tras el despeje
                # for columna in range(1, incognitas + 1):
                #     # Si la columna es la variable, saltarsela
                #     if columna == i + 1:
                #         continue
                #     # Si hay un coeficiente, entonces escribimos
                #     coeficiente = mat.at(fila_variable, columna) * -1
                #     ecuacion += termino_a_string(
                #         coeficiente=coeficiente, variable=columna, es_primer_termino=primer_termino)
                #     # Ya usamos el primer termino
                #     if primer_termino == True:
                #         primer_termino = False
                # # Finalmente, imprimimos la variable con su ecuacion
                # print(ecuacion)
    print("\nClasificacion: Consistente.")


def resolver_sistema_cramer(mat: Matriz, ecuaciones: int, incognitas: int):
    # Primero revisamos que las medidas de la matriz coincidan con los numeros dados
    if mat.filas != ecuaciones:
        raise Exception(
            "La cantidad de filas no coincide con la cantidad de ecuaciones")
    if mat.columnas != incognitas + 1:
        raise Exception(
            f"La cantidad de columnas esperada era: {incognitas + 1}, pero la dada fue: {mat.columnas}")
    if ecuaciones != incognitas:
        raise Exception(
            f"Cramer solo está disponible en sistemas nxn (n° de ecuaciones = n° de incognitas)")

    # Obtenemos la matriz sin la columna resultados
    mat_sistema = slice_matriz(mat, (1, ecuaciones), (1, incognitas))
    columna_resultados: int = incognitas + 1

    print(
        f"Obtendremos el determinante de la matriz del sistema:\n{mat_sistema}")
    det_sistema = determinante_por_cofactores(mat_sistema, calcprint=True)

    determinantes_variables: list[Fraction] = []
    print(f"Ahora obtendremos los determinantes de cada una de las variables")
    # Vamos por cada una de las variables
    for i in range(1, incognitas + 1):
        n = incognitas
        # Creamos una nueva matriz para cada incognita de NxN
        matriz_incognita = Matriz(n, n)
        # La populamos
        for j in range(1, n + 1):
            for k in range(1, n + 1):
                # Si la columna es igual a i, usamos la columna resultado en lugar de la
                # matriz original
                if k == i:
                    matriz_incognita.set(j, k, mat.at(j, columna_resultados))
                else:
                    matriz_incognita.set(j, k, mat.at(j, k))
        print(to_subscript(f"Matriz de x{i}:\n") + f"{matriz_incognita}")
        # Ahora obtenemos el determinante
        determinantes_variables.append(
            determinante_por_cofactores(matriz_incognita))

    print(f"Δ = {det_sistema}")
    for i in range(1, incognitas + 1):
        print(to_subscript(f"Δx{i} = ") + f"{determinantes_variables[i - 1]}")

    # El sistema no tiene solucion unica
    if det_sistema == 0:
        ct: bool = False
        for det in determinantes_variables:
            if det != 0:
                ct = True
                break
        # Si alguno de los determinantes de las variables es distinto de 0, el sistema es inconsistente
        if ct:
            print(f"El sistema no tiene solución")
        else:
            print(f"El sistema tiene infinitas soluciones")
        return

    print(f"\nSoluciones:")
    for i in range(1, incognitas + 1):
        print(to_subscript(f"x{i} = Δx{i}/ Δ = ") +
              f"({determinantes_variables[i - 1]} / {det_sistema}) = {determinantes_variables[i - 1] / det_sistema}")
    print()


def calcular_inversa(mat: Matriz, tamaño: int):
    if mat.filas != tamaño or mat.columnas != tamaño:
        print(f"La matriz debe ser cuadrada!")
        return

    print("\n==============================================")
    print("      MATRIZ INVERSA")
    print("==============================================\n")

    matriz_completa = Matriz(tamaño, tamaño * 2)
    identidad = hacer_matriz_identidad(tamaño)

    for fila in range(1, tamaño + 1):
        for columna in range(1, tamaño + 1):
            matriz_completa.set(fila, columna, mat.at(fila, columna))
            matriz_completa.set(fila, columna + tamaño,
                                identidad.at(fila, columna))

    print(f"Matriz aumentada inicial: \n{matriz_completa}")

    resetear_pasos()
    matriz_escalonada_reducida(matriz_completa, tamaño, tamaño)

    pivotes: list[Posicion] = obtener_pivotes(matriz_completa, tamaño, tamaño)

    # 2. Propiedades Teóricas a Verificar
    # El programa debe incluir una sección donde se evalúen o verifiquen los siguientes
    # teoremas y propiedades asociados a la invertibilidad de A:
    #  (c) La matriz A tiene n posiciones pivotes.
    #  (d) La ecuación A x = 0 tiene solamente la solución trivial.
    #  (e) Las columnas de A forman un conjunto linealmente independiente.
    # Para cada propiedad, el programa debe mostrar una breve interpretación:
    #  Si A tiene n pivotes, entonces A es invertible.
    #  Si A x = 0 solo tiene la solución trivial, entonces A⁻¹ existe.
    #  Si las columnas son linealmente independientes, entonces A es una matriz
    # invertible

    # === Propiedades teóricas a verificar ===
    print("\n--- Propiedades teóricas sobre invertibilidad ---")

    # (c) La matriz A tiene n posiciones pivote
    print(f"(c) Pivotes encontrados: {len(pivotes)} de {tamaño}")
    if len(pivotes) == tamaño:
        print("Interpretación: A tiene n pivotes, entonces A es invertible.")
    else:
        print("Interpretación: A no tiene n pivotes, entonces A no es invertible.")

    # (d) La ecuación Ax = 0 tiene solo la solución trivial
    print("(d) Resolviendo Ax = 0 para verificar soluciones...")
    matriz_homogenea = Matriz(tamaño, tamaño + 1)
    # Creamos la matriz aumentada [A | 0]
    for fila in range(1, tamaño + 1):
        for columna in range(1, tamaño + 1):
            matriz_homogenea.set(fila, columna, mat.at(fila, columna))
    print("Matriz aumentada [A | 0]:")
    print(matriz_homogenea)
    print("Resolviendo a identidad...")
    matriz_escalonada_reducida(matriz_homogenea, tamaño, tamaño)
    pivotes_homogenea = obtener_pivotes(matriz_homogenea, tamaño, tamaño)
    if len(pivotes_homogenea) == tamaño:
        print("Interpretación: Ax = 0 solo tiene la solución trivial, entonces A⁻¹ existe.")
    else:
        print(
            "Interpretación: Ax = 0 tiene soluciones no triviales, entonces A⁻¹ no existe.")

    # (e) Las columnas de A forman un conjunto linealmente independiente
    print("(e) Verificando independencia lineal de las columnas de A...")
    columnas = [Vector([mat.at(fila, col) for fila in range(1, tamaño + 1)])
                for col in range(1, tamaño + 1)]
    if len(pivotes) == tamaño:
        print("Interpretación: Las columnas de A son linealmente independientes, entonces A es invertible.")
    else:
        print("Interpretación: Las columnas de A no son linealmente independientes, entonces A no es invertible.")

    # Verificar si la parte izquierda es la identidad
    parte_izquierda = slice_matriz(matriz_completa, (1, tamaño), (1, tamaño))

    if parte_izquierda == identidad:
        inversa = slice_matriz(
            matriz_completa, (1, tamaño), (tamaño + 1, tamaño * 2))
        print(
            f"La matriz es no singular (determinante diferente de 0) y su inversa es:\n{inversa}")

        # Verificación adicional: A * A⁻¹ = I
        print("\nVerificación (A * A⁻¹):")
        verificacion = multiplicar_matrices(mat, inversa, calcprint=True)
        print(verificacion)
    else:
        print(f"La matriz es singular (determinante es 0) y no tiene inversa")
        print(f"Parte izquierda resultante:\n{parte_izquierda}")

# Combinacion lineal de vectores


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

    print("\n==============================================")
    print("      COMBINACIÓN LINEAL DE VECTORES")
    print("==============================================\n")

    print("\nMatriz del sistema planteado:\n")
    print(matriz)

    print("\n=== Resolución del sistema ===\n")
    resolver_sistema(matriz, ecuaciones, incognitas)
    print("\n==============================================\n")

    # Mostrar la combinación planteada
    print("Planteando el sistema como combinación lineal:\n")
    ecuacion = "  "
    for i, v in enumerate(vectores):
        coef = to_subscript(f"X{i+1}")
        ecuacion += f"{coef}·{v}"
        if i < len(vectores) - 1:
            ecuacion += " + "
    ecuacion += f" = {resultado}\n"
    print(ecuacion)


def resolver_ecuacion_matricial(A: Matriz, B: Matriz):
    """
    Resuelve la ecuación matricial AX = B, donde:
    - A es una matriz cuadrada n x n
    - B es una matriz n x m
    - X es la matriz solución n x m
    """
    # Verificar que A es cuadrada
    if A.filas != A.columnas:
        raise Exception("La matriz A debe ser cuadrada")
    n = A.filas

    # Verificar compatibilidad de dimensiones
    if B.filas != n:
        raise Exception("El número de filas de B debe coincidir con las de A")

    m = B.columnas

    # Crear matriz aumentada [A | B] de tamaño n x (n + m)
    aumentada = Matriz(n, n + m)

    # Copiar A a la parte izquierda
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            aumentada.set(i, j, A.at(i, j))

    # Copiar B a la parte derecha
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            aumentada.set(i, n + j, B.at(i, j))

    print("Matriz aumentada [A | B]:")
    print(aumentada)

    # Aplicar eliminación de Gauss-Jordan
    resetear_pasos()
    print("\n=== Aplicando eliminación de Gauss-Jordan ===")
    matriz_escalonada_reducida(aumentada, n, n)
    matriz_identidad(aumentada, n, n)

    # Extraer la solución X de la parte derecha
    X = Matriz(n, m)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            valor = aumentada.at(i, n + j)
            X.set(i, j, valor)

    print("\n=== Solución X ===")
    print(X)

    return X


def dependencia_lineal(dimension: int, vectores: list[Vector]) -> None:
    """
    Determina si un conjunto de vectores es linealmente dependiente o independiente.
    Monta un sistema homogéneo (AX=0, donde las columnas de A son los vectores) y lo resuelve usando resolver_sistema.
    Muestra el planteo como ecuación vectorial (c₁·v₁ + ... + cₙ·vₙ = 0) y los pasos de resolución.
    Clasifica según el número de pivotes: si igual al número de vectores, independiente; si menor, dependiente.
    Maneja el caso especial de más vectores que la dimensión (dependiente por teorema).

    Args:
        dimension (int): Dimensión de los vectores (ℝⁿ).
        vectores (list[Vector]): Lista de objetos Vector a evaluar.

    Returns:
        None: Imprime los pasos y el resultado en consola, siguiendo el formato del proyecto.
    """
    num_vectores = len(vectores)
    paso_contador = 1  # Contador local para pasos en dependencia_lineal

    # Validar entrada: más vectores que dimensión implica dependencia lineal
    if num_vectores > dimension:
        imprimir_paso(
            f"Paso {paso_contador}: Más vectores ({num_vectores}) que la dimensión ({dimension}): Dependientes por teorema.")
        print("\nLos vectores ingresados son linealmente dependientes.")
        print("\n==============================================")
        return

    # Montar la matriz aumentada [A | 0], donde A tiene los vectores como columnas
    matriz: Matriz = Matriz(dimension, num_vectores +
                            1)  # +1 para columna de ceros
    for col in range(1, num_vectores + 1):
        vec = vectores[col - 1]
        for row in range(1, dimension + 1):
            matriz.set(row, col, vec.at(row))
            # Última columna = 0 (sistema homogéneo)
            matriz.set(row, num_vectores + 1, Fraction(0))

    # Encabezado visual
    print("\n==============================================")
    print("      DEPENDENCIA LINEAL DE VECTORES")
    print("==============================================\n")

    # Mostrar matriz inicial
    print("\nMatriz del sistema homogéneo planteado:\n")
    print(matriz)

    # Mostrar planteo como ecuación vectorial: c₁·v₁ + ... + cₙ·vₙ = 0
    eq = Ecuacion()
    for i, vec in enumerate(vectores, 1):
        coef = to_subscript(f"c{i}")
        eq.agregar_termino(Termino(1, f"{coef}·{vec}"))
    eq.agregar_termino(Termino(0), lado="derecho")  # = 0
    imprimir_paso(f"Paso {paso_contador}: Planteo: {eq}")
    paso_contador += 1

    # Resolver el sistema homogéneo
    print("\n=== Resolución del sistema homogéneo ===\n")
    resolver_sistema(matriz, dimension, num_vectores)

    # Clasificar dependencia según pivotes
    pivotes = obtener_pivotes(matriz, dimension, num_vectores)
    if len(pivotes) == num_vectores:
        print("Solo solución trivial (c₁=0, ..., cₙ=0): Los vectores son linealmente independientes.")
    else:
        print("Existen soluciones no triviales: Los vectores son linealmente dependientes.")

    print("\n==============================================")
