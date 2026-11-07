"""Problemas de la parte B. Cada lista recorre las parejas por filas.
Un número positivo favorece al primero; uno negativo, al segundo.
El 1 indica igualdad. La primera lista compara los criterios.
"""

PROBLEMAS = {
    "1. Ubicación del local": {
        "criterios": ["Compradores", "Visibilidad", "Competencia", "Costo"],
        "alternativas": ["Mall A", "Centro B", "Pasaje C"],
        "metodo": "Media geométrica",
        "parejas": [[3, 7, 8, 3, 6, 3], [8, 6, -3], [5, -3, -7],
                    [-7, -2, 4], [-8, -4, 3]],
    },
    "2. Herramienta de gestión": {
        "criterios": ["P. Tareas", "Colaboración", "E. Riesgos", "V. Gráfica"],
        "alternativas": ["T1", "T2", "T3"],
        "metodo": "Autovalor",
        "parejas": [[2, 6, 2, 7, 1, 5], [-6, 6, 4], [5, 2, -7],
                    [-4, -2, 4], [-5, -2, 1]],
    },
    "3. Tasación de Alex Rivera": {
        "criterios": ["Goles", "Asistencias", "Potencial", "Liderazgo", "Adaptabilidad"],
        "alternativas": ["Diomande", "Barcola", "Rogers", "Rivera"],
        "metodo": "Autovalor",
        "parejas": [
            [3, 4, 4, 8, 2, 2, 2, 1, 2, 2],# Criterios
            [1, 1, 1, 1, 1, 1],# Goles
            [1, 1, 1, 1, 1, 1],# Asistencias
            [1, 1, 1, 1, 1, 1],# Potencial
            [6, 4, 2, 2, 2, 1],# Liderazgo
            [-6, 4, 1, 4, 2, 1],# Adaptabilidad
        ],
    },
}
