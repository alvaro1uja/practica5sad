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
        # Propuesta editable: pesos relativos 8:4:2:2:1.
        # Liderazgo y adaptabilidad: Alto frente a Medio recibe un 3.
        "parejas": [[2, 4, 4, 8, 2, 2, 4, 1, 2, 2],
                    [-3, -3, -3, 1, 1, 1], [1, -3, -3, -3, -3, 1]],
        "cuantitativos": [[12, 11, 10, 16], [8, 1, 6, 10], [15, 11, 10, 13]],
        "precios": [125, 125, 137.3],  # millones de euros de los tres comparables
    },
}
