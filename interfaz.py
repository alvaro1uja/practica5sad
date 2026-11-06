"""Interfaz AHP. Guardar junto a ahp.py y ejecutar: python3 interfaz.py.

Requiere NumPy y Tkinter. Los cálculos se realizan en el backend ahp.py.
"""

from math import isclose
from ahp import media_geometrica, resolvedorahp, test_consistencia
from ahp import pesosaproximados, pesosporautovalor

METODOS = {
    "Media geométrica": media_geometrica,
    "Aproximado": pesosaproximados,
    "Autovalor": pesosporautovalor,
}


# El valor compara el elemento izquierdo con el derecho.
OPCIONES = ["Igual importancia"]
VALORES = [1.0]
for numero in range(2, 10):
    OPCIONES.append(f"Izquierda: {numero}")
    VALORES.append(float(numero))
    OPCIONES.append(f"Derecha: {numero}")
    VALORES.append(1 / numero)


def leer_nombres(texto: str) -> list[str]:
    nombres = [nombre.strip() for nombre in texto.split(",")]
    if not 2 <= len(nombres) <= 10:
        raise ValueError("Introduce entre 2 y 10 nombres en cada lista.")
    if any(not nombre for nombre in nombres):
        raise ValueError("Hay un nombre vacío. Revisa las comas.")
    if len(set(nombre.casefold() for nombre in nombres)) != len(nombres):
        raise ValueError("No repitas nombres dentro de una misma lista.")
    return nombres


def construir_matriz(n: int, respuestas: list[str]) -> list[list[float]]:
    if len(respuestas) != n * (n - 1) // 2:
        raise ValueError("Faltan comparaciones.")
    matriz = [[1.0 for columna in range(n)] for fila in range(n)]
    posicion = 0
    for fila in range(n):
        for columna in range(fila + 1, n):
            respuesta = respuestas[posicion]
            if respuesta not in OPCIONES:
                raise ValueError("Completa todas las comparaciones antes de resolver.")
            valor = VALORES[OPCIONES.index(respuesta)]
            matriz[fila][columna] = valor
            matriz[columna][fila] = 1 / valor
            posicion += 1
    return matriz


def preparar_resultados(criterios, alternativas, matrices, metodo="Media geométrica") -> str:
    """La primera matriz es la de criterios; las demás siguen su mismo orden."""
    calcularpesos = METODOS[metodo]
    globales = resolvedorahp(matrices[0], matrices[1:], calcularpesos)
    texto = ["RESULTADOS AHP — " + metodo.upper(), ""]
    revisiones = []
    titulos = ["Criterios"] + [f"Alternativas según {c}" for c in criterios]

    for posicion, matriz in enumerate(matrices):
        nombres = criterios if posicion == 0 else alternativas
        pesos = calcularpesos(matriz)
        consistencia = test_consistencia(matriz)
        titulo = titulos[posicion]
        texto.append(titulo.upper())
        texto.append(f"Autovalor máximo: {consistencia['autovalormaximo']:.6f}")
        # Evita mostrar -0.000000 por pequeños errores de redondeo.
        ci = max(0.0, consistencia["CI"])
        cr = max(0.0, consistencia["CR"])
        estado = "Aceptable" if consistencia["aceptable"] else "Revisar juicios"
        texto.append(f"CI: {ci:.6f} | CR: {cr:.6f} ({cr:.2%}) | {estado}")
        if not consistencia["aceptable"]:
            revisiones.append(titulo)
        texto.append("Vector de prioridad (en este orden):")
        for nombre, peso in zip(nombres, pesos):
            texto.append(f"  {nombre}: {peso:.6f}")
        texto.append("Filas y columnas de la matriz: " + ", ".join(nombres))
        for fila in matriz:
            texto.append("  " + "  ".join(f"{valor:9.4f}" for valor in fila))
        texto.append("")

    texto.extend(["RANKING — PRIORIDADES GLOBALES", "Mayor prioridad = mejor posición."])
    orden = sorted(range(len(alternativas)), key=lambda i: globales[i], reverse=True)
    puesto = 0
    anterior = None
    for posicion, indice in enumerate(orden, start=1):
        prioridad = globales[indice]
        if anterior is None or not isclose(prioridad, anterior, rel_tol=1e-9, abs_tol=1e-12):
            puesto = posicion
        texto.append(f"{puesto}. {alternativas[indice]}: {prioridad:.6f} ({prioridad:.2%})")
        anterior = prioridad

    texto.append("\nCriterio de aceptación: CR < 0.10 (10 %) en cada matriz.")
    if revisiones:
        texto.append("ATENCIÓN: revisa las comparaciones de: " + "; ".join(revisiones))
        texto.append("El ranking se ha calculado, pero requiere revisar estos juicios.")
    else:
        texto.append("Todas las matrices tienen una consistencia aceptable.")
    if any(len(matriz) == 2 for matriz in matrices):
        texto.append("En matrices recíprocas de tamaño 2, CI y CR se muestran como 0.")
    return "\n".join(texto)


def main():
    import tkinter as tk
    from tkinter import ttk, messagebox
    from tkinter.scrolledtext import ScrolledText

    ventana = tk.Tk()
    ventana.title("Práctica 5 — AHP")
    ventana.geometry("1000x760")
    ventana.minsize(840, 620)
    ventana.configure(background="#eef2f6")

    # Estilos compartidos: solo afectan a la apariencia de los controles.
    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")
    estilo.configure(".", font=("DejaVu Sans", 10), background="#ffffff",
                     foreground="#243247")
    estilo.configure("TFrame", background="#ffffff")
    estilo.configure("TLabel", background="#ffffff")
    estilo.configure("Titulo.TLabel", font=("DejaVu Sans", 17, "bold"))
    estilo.configure("Ayuda.TLabel", foreground="#52647a")
    estilo.configure("Campo.TLabel", font=("DejaVu Sans", 10, "bold"))
    estilo.configure("TNotebook", background="#eef2f6", borderwidth=0)
    estilo.configure("TNotebook.Tab", padding=(20, 11), background="#e2e8f0",
                     foreground="#52647a", font=("DejaVu Sans", 10, "bold"))
    estilo.map("TNotebook.Tab", background=[("selected", "#ffffff")],
               foreground=[("disabled", "#78879a"), ("selected", "#087e8b")])
    estilo.configure("TEntry", padding=10, fieldbackground="#f8fafc",
                     bordercolor="#cbd5e1", lightcolor="#cbd5e1", darkcolor="#cbd5e1")
    estilo.map("TEntry", bordercolor=[("focus", "#087e8b")])
    estilo.configure("TCombobox", padding=8, arrowsize=14)
    estilo.map("TCombobox", fieldbackground=[("readonly", "#f8fafc")],
               selectbackground=[("readonly", "#f8fafc")],
               selectforeground=[("readonly", "#243247")])
    estilo.configure("TButton", padding=(16, 10), borderwidth=0,
                     background="#e8eef4", font=("DejaVu Sans", 10, "bold"))
    estilo.map("TButton", background=[("active", "#dbe4ed")])
    estilo.configure("Principal.TButton", background="#087e8b", foreground="white")
    estilo.map("Principal.TButton", background=[("pressed", "#065d67"),
               ("active", "#096d79")], foreground=[("active", "white")])
    estilo.configure("Vertical.TScrollbar", background="#cbd5e1",
                     troughcolor="#f1f5f9", borderwidth=0, arrowsize=12)
    estilo.layout("Escala.TRadiobutton", estilo.layout("Toolbutton"))
    estilo.configure("Escala.TRadiobutton", width=2, anchor="center",
                     padding=(3, 8), font=("DejaVu Sans", 9, "bold"),
                     background="#f1f5f9", foreground="#405269", borderwidth=1)
    estilo.map("Escala.TRadiobutton",
               background=[("selected", "#087e8b"), ("active", "#dcecef")],
               foreground=[("selected", "white")],
               relief=[("selected", "sunken"), ("!selected", "raised")])

    criterios = []
    alternativas = []
    respuestas = []  # Una lista de StringVar por cada matriz.

    pestanas = ttk.Notebook(ventana)
    pestanas.pack(fill="both", expand=True, padx=20, pady=20)
    datos = ttk.Frame(pestanas, padding=24)
    comparaciones = ttk.Frame(pestanas, padding=20)
    resultados = ttk.Frame(pestanas, padding=20)
    pestanas.add(datos, text="1. Datos")
    pestanas.add(comparaciones, text="2. Comparaciones", state="disabled")
    pestanas.add(resultados, text="3. Resultados", state="disabled")

    ttk.Label(datos, text="Define tu problema", style="Titulo.TLabel").pack(
        anchor="w", pady=(0, 8))
    ttk.Label(datos, style="Ayuda.TLabel", text="Escribe los nombres separados por comas (entre 2 y 10).",
              wraplength=650).pack(anchor="w", pady=(0, 16))
    ttk.Label(datos, text="Criterios. Ejemplo: Precio, Calidad, Autonomía", style="Campo.TLabel").pack(anchor="w")
    nombrescriterios = tk.StringVar()
    ttk.Entry(datos, textvariable=nombrescriterios).pack(fill="x", pady=(5, 16))
    ttk.Label(datos, text="Alternativas. Ejemplo: Opción A, Opción B, Opción C", style="Campo.TLabel").pack(anchor="w")
    nombresalternativas = tk.StringVar()
    ttk.Entry(datos, textvariable=nombresalternativas).pack(fill="x", pady=(5, 16))

    def limpiar_resultados(*args):
        salida.configure(state="normal")
        salida.delete("1.0", "end")
        salida.configure(state="disabled")
        pestanas.tab(resultados, state="disabled")

    def cambiar_nombres(*args):
        # Hay que generar de nuevo si cambian los nombres o su orden.
        pestanas.tab(comparaciones, state="disabled")
        limpiar_resultados()

    def mostrar_comparaciones(event=None):
        for widget in filas.winfo_children():
            widget.destroy()
        indice = selector.current()
        nombres = criterios if indice == 0 else alternativas
        posicion = 0
        for i in range(len(nombres)):
            for j in range(i + 1, len(nombres)):
                ttk.Label(filas, text=nombres[i], style="Campo.TLabel", wraplength=100).grid(
                    row=posicion, column=0, sticky="w", padx=8, pady=5)
                escala = ttk.Frame(filas)
                escala.grid(row=posicion, column=1, padx=8, pady=5)
                # Una sola elección por fila: 9 ... 2, 1, 2 ... 9.
                for columna in range(17):
                    numero = abs(8 - columna) + 1
                    if columna < 8:
                        valor = f"Izquierda: {numero}"
                    elif columna == 8:
                        valor = "Igual importancia"
                    else:
                        valor = f"Derecha: {numero}"
                    ttk.Radiobutton(
                        escala, text=str(numero), value=valor,
                        variable=respuestas[indice][posicion],
                        style="Escala.TRadiobutton"
                    ).grid(row=0, column=columna, padx=1)
                ttk.Label(filas, text=nombres[j], style="Campo.TLabel", wraplength=100).grid(
                    row=posicion, column=2, sticky="w", padx=8, pady=5)
                posicion += 1
        lienzo.yview_moveto(0)

    def generar():
        nonlocal criterios, alternativas, respuestas
        try:
            nuevoscriterios = leer_nombres(nombrescriterios.get())
            nuevasalternativas = leer_nombres(nombresalternativas.get())
        except ValueError as error:
            messagebox.showerror("Revisa los nombres", str(error))
            return
        if respuestas and not messagebox.askyesno(
                "Generar comparaciones", "Se borrarán las respuestas anteriores. ¿Continuar?"):
            return
        criterios = nuevoscriterios
        alternativas = nuevasalternativas
        respuestas = []
        for nombres in [criterios] + [alternativas for criterio in criterios]:
            grupo = []
            for pareja in range(len(nombres) * (len(nombres) - 1) // 2):
                variable = tk.StringVar()
                variable.trace_add("write", limpiar_resultados)
                grupo.append(variable)
            respuestas.append(grupo)
        selector["values"] = ["Criterios"] + [f"Alternativas: {c}" for c in criterios]
        selector.current(0)
        limpiar_resultados()
        mostrar_comparaciones()
        pestanas.tab(comparaciones, state="normal")
        pestanas.select(comparaciones)

    def resolver():
        matrices = []
        for indice, grupo in enumerate(respuestas):
            nombres = criterios if indice == 0 else alternativas
            try:
                matriz = construir_matriz(len(nombres), [v.get() for v in grupo])
            except ValueError as error:
                selector.current(indice)
                mostrar_comparaciones()
                messagebox.showerror("Comparaciones incompletas", str(error))
                return
            matrices.append(matriz)
        texto = preparar_resultados(criterios, alternativas, matrices, metodo.get())
        salida.configure(state="normal")
        salida.delete("1.0", "end")
        salida.insert("1.0", texto)
        # Resalta los apartados sin modificar el contenido del resultado.
        titulos = ["CRITERIOS", "RESULTADOS AHP — " + metodo.get().upper(),
                   "RANKING — PRIORIDADES GLOBALES"]
        titulos += [f"Alternativas según {c}".upper() for c in criterios]
        for numero, linea in enumerate(texto.splitlines(), start=1):
            etiqueta = None
            if linea in titulos:
                etiqueta = "titulo"
            elif linea.startswith("ATENCIÓN") or (linea.startswith("CI:") and "Revisar" in linea):
                etiqueta = "aviso"
            elif linea.startswith("Todas las matrices") or (linea.startswith("CI:") and "Aceptable" in linea):
                etiqueta = "correcto"
            if etiqueta:
                salida.tag_add(etiqueta, f"{numero}.0", f"{numero}.end")
        salida.configure(state="disabled")
        pestanas.tab(resultados, state="normal")
        pestanas.select(resultados)

    ttk.Button(datos, text="Generar comparaciones", style="Principal.TButton", command=generar).pack(anchor="w")
    ttk.Label(comparaciones, text="Compara tus preferencias", style="Titulo.TLabel").pack(
        anchor="w", pady=(0, 8))
    ttk.Label(comparaciones, style="Ayuda.TLabel", text="Selecciona la matriz que quieres completar:").pack(anchor="w")
    selector = ttk.Combobox(comparaciones, state="readonly")
    selector.pack(fill="x", pady=8)
    selector.bind("<<ComboboxSelected>>", mostrar_comparaciones)
    ttk.Label(comparaciones, text=(
        "Pulsa un número: la izquierda favorece al nombre izquierdo y la derecha al derecho. "
        "El 1 central indica igualdad. Escala: 1 igual, 2 ligera, 3 moderada, "
        "4 entre moderada y fuerte, 5 fuerte, 6 entre fuerte y muy fuerte, "
        "7 muy fuerte, 8 entre muy fuerte y extrema, 9 extrema.\n"
        "En criterios comparas importancia; en alternativas, preferencia según el criterio. "
        "Para un coste, recuerda que un valor menor suele ser mejor."),
        style="Ayuda.TLabel", wraplength=710).pack(anchor="w", pady=(0, 10))

    # Área desplazable: admite hasta 45 parejas por matriz.
    zona = ttk.Frame(comparaciones)
    zona.pack(fill="both", expand=True)
    lienzo = tk.Canvas(zona, highlightthickness=0, background="#ffffff")
    barra = ttk.Scrollbar(zona, orient="vertical", command=lienzo.yview)
    lienzo.configure(yscrollcommand=barra.set)
    barra.pack(side="right", fill="y")
    lienzo.pack(side="left", fill="both", expand=True)
    filas = ttk.Frame(lienzo)
    contenido = lienzo.create_window((0, 0), window=filas, anchor="nw")
    filas.bind("<Configure>", lambda event: lienzo.configure(scrollregion=lienzo.bbox("all")))
    lienzo.bind("<Configure>", lambda event: lienzo.itemconfigure(contenido, width=event.width))
    filas.columnconfigure(0, weight=1)
    filas.columnconfigure(2, weight=1)
    acciones = ttk.Frame(comparaciones)
    acciones.pack(pady=(12, 0))
    ttk.Label(acciones, text="Método:").pack(side="left")
    metodo = tk.StringVar(value="Media geométrica")
    ttk.Combobox(acciones, textvariable=metodo, values=list(METODOS),
                 state="readonly", width=18).pack(side="left", padx=8)
    metodo.trace_add("write", limpiar_resultados)
    ttk.Button(acciones, text="Resolver AHP", style="Principal.TButton",
               command=resolver).pack(side="left")

    ttk.Label(resultados, text="Resultados de la decisión", style="Titulo.TLabel").pack(
        anchor="w", pady=(0, 14))
    salida = ScrolledText(resultados, wrap="word", font=("DejaVu Sans Mono", 10),
                          state="disabled", background="#f8fafc", foreground="#243247",
                          relief="flat", borderwidth=0, padx=16, pady=16, spacing1=3,
                          selectbackground="#cce8ec", selectforeground="#243247")
    salida.tag_configure("titulo", font=("DejaVu Sans", 11, "bold"),
                         foreground="#087e8b", spacing1=12, spacing3=6)
    salida.tag_configure("aviso", foreground="#9a4311", background="#fff2df")
    salida.tag_configure("correcto", foreground="#136749")
    salida.pack(fill="both", expand=True)
    ttk.Button(resultados, text="Volver a las comparaciones",
               command=lambda: pestanas.select(comparaciones)).pack(pady=(10, 0))
    nombrescriterios.trace_add("write", cambiar_nombres)
    nombresalternativas.trace_add("write", cambiar_nombres)
    ventana.mainloop()


if __name__ == "__main__":
    main()