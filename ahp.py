#funcion que calcula la media geometrica de cada fila de una matriz y devuelve los pesos normalizados
def media_geometrica(matriz):
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

#funcion que resuelve el AHP dado una matriz de criterios y una lista de matrices de alternativas
def resolvedorahp(matrizcriterios, matricesalternativas):
    # 1. Calcular los pesos de los criterios
    pesoscriterios = media_geometrica(matrizcriterios)

    # 2. Calcular las prioridades de alternativas para cada criterio
    prioridadeslocales = []

    for matriz in matricesalternativas:
        pesosalternativas = media_geometrica(matriz)
        prioridadeslocales.append(pesosalternativas)

    # 3. Calcular las prioridades globales
    prioridadesglobales = {}
    numeroalternativas = len(matricesalternativas[0])

    for alternativa in range(numeroalternativas):
        prioridadglobal = 0

        for criterio in range(len(pesoscriterios)):
            prioridadglobal = prioridadglobal + (pesoscriterios[criterio]* prioridadeslocales[criterio][alternativa])

        prioridadesglobales[alternativa] = prioridadglobal

    return prioridadesglobales