import numpy as np


#funcion que calcula la media geometrica de cada fila de una matriz y devuelve los pesos normalizados
def media_geometrica(matriz: list[list[float]]) -> list[float]:
    mediasfilas = []
    n = len(matriz)

    for fila in matriz:# para cada fila
        producto = 1

        for numero in fila:# para cada valor de la fila
            producto = producto * numero

        mediafila = producto**(1/n)
        mediasfilas.append(mediafila)

    pesosfilas = []
    total = sum(mediasfilas)

    for mediafila in mediasfilas:
        pesosfilas.append(mediafila / total)

    return pesosfilas


#funcion que resuelve el AHP y devuelve las prioridades globales de las alternativas
def resolvedorahp(matrizcriterios: list[list[float]], matricesalternativas: list[list[list[float]]], metodo=media_geometrica) -> list[float]:
    #1. Calcular los pesos de los criterios
    pesoscriterios = metodo(matrizcriterios)

    #2. Calcular las prioridades de alternativas en cada criterio
    prioridadeslocales = []

    for matriz in matricesalternativas:
        pesosalternativas = metodo(matriz)
        prioridadeslocales.append(pesosalternativas)

    #3. Calcular las prioridades globales
    prioridadesglobales = []
    numeroalternativas = len(matricesalternativas[0])

    for alternativa in range(numeroalternativas):
        prioridadglobal = 0

        for criterio in range(len(pesoscriterios)):
            prioridadglobal = prioridadglobal + (pesoscriterios[criterio]* prioridadeslocales[criterio][alternativa])

        prioridadesglobales.append(prioridadglobal)

    return prioridadesglobales


#funcion que calcula la consistencia
def test_consistencia(matriz: list[list[float]]) -> dict:
    n = len(matriz)

    #tabla del tema
    indicesaleatorios = {3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

    if n < 1 or n > 10:
        raise ValueError("La matriz debe tener entre 1 y 10 elementos")

    autovalores = np.linalg.eigvals(matriz)
    autovalormaximo = float(max(autovalores.real))

    indiceconsistencia = 0.0
    razonconsistencia = 0.0

    if n > 2:
        indiceconsistencia = (autovalormaximo-n)/(n-1)

        indicealeatorio = indicesaleatorios[n]
        razonconsistencia = indiceconsistencia/indicealeatorio

    return {"autovalormaximo": autovalormaximo, "CI": indiceconsistencia, "CR": razonconsistencia, "aceptable": razonconsistencia<0.10}

#funcion que calcula los pesos usando el autovector del autovalor maximo
def pesosporautovalor(matriz: list[list[float]]) -> list[float]:
    autovalores, autovectores = np.linalg.eig(matriz)
    n = len(matriz)

    #1.buscar la posicion del autovalor mayor
    posicionmaximo = 0
    for i in range(1, n):
        if autovalores[i].real > autovalores[posicionmaximo].real:
            posicionmaximo = i

    #2.guardar la columna que contiene su autovector
    autovector = []
    for fila in range(n):
        valor = autovectores[fila][posicionmaximo].real
        autovector.append(float(valor))

    #3.normalizar para que los pesos sumen 1
    pesosfilas = []
    total = sum(autovector)
    for valor in autovector:
        pesosfilas.append(valor / total)

    return pesosfilas


#funcion que normaliza las columnas y calcula la media de cada fila
def pesosaproximados(matriz: list[list[float]]) -> list[float]:
    n = len(matriz)
    sumascolumnas = []

    #1.sumar cada columna
    for columna in range(n):
        sumacolumna = 0
        for fila in matriz:
            sumacolumna = sumacolumna + fila[columna]

        sumascolumnas.append(sumacolumna)

    #2.calcular la media de cada fila normalizada
    pesosfilas = []
    for fila in matriz:
        sumafila = 0
        for columna in range(n):
            valornormalizado = fila[columna] / sumascolumnas[columna]
            sumafila = sumafila + valornormalizado
        pesosfilas.append(sumafila / n)

    return pesosfilas


