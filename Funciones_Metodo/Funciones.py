import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Función para evaluar la ecuación
def f(x, funcion):
    return eval(funcion, {"x": x, "np": np})

# Función para calcular la derivada de la ecuación
def df(x, funcion):
    h = 1e-5  # Paso pequeño para la derivada numérica
    return (f(x + h, funcion) - f(x - h, funcion)) / (2 * h)

# Método de bisección
def metodo_biseccion():
    funcion = funcion_entry.get()
    a = float(a_entry.get())
    b = float(b_entry.get())
    umbral = float(umbral_entry.get())
    max_iter = int(max_iter_entry.get())

    # Limpiar tabla
    tabla.delete(*tabla.get_children())

    if f(a, funcion) * f(b, funcion) > 0:
        messagebox.showerror("Error", "Los valores iniciales no cumplen la condición f(a) * f(b) < 0.")
        return

    i = 0
    while i < max_iter:
        c = (a + b) / 2
        fc = f(c, funcion)

        color_fila = "#e8f6ff" if i % 2 == 0 else "#d1e7fd"
        tabla.insert("", "end", values=(i, "{:.8f}".format(c), "{:.8f}".format(fc)), tags=("even" if i % 2 == 0 else "odd"))

        if abs(fc) <= umbral:
            break  # Sale del bucle

        if f(a, funcion) * fc < 0:
            b = c
        else:
            a = c

        i += 1

    # Graficar función
    graficar_funcion(funcion, a, b)

# Método de falsa posición
def metodo_falsa_posicion():
    funcion = funcion_entry.get()
    a = float(a_entry.get())
    b = float(b_entry.get())
    umbral = float(umbral_entry.get())
    max_iter = int(max_iter_entry.get())

    # Limpiar tabla
    tabla.delete(*tabla.get_children())

    if f(a, funcion) * f(b, funcion) > 0:
        messagebox.showerror("Error", "Los valores iniciales no cumplen la condición f(a) * f(b) < 0.")
        return

    i = 0
    while i < max_iter:
        c = b - (f(b, funcion) * (b - a)) / (f(b, funcion) - f(a, funcion))
        fc = f(c, funcion)

        color_fila = "#e8f6ff" if i % 2 == 0 else "#d1e7fd"
        tabla.insert("", "end", values=(i, "{:.8f}".format(c), "{:.8f}".format(fc)), tags=("even" if i % 2 == 0 else "odd"))

        if abs(fc) <= umbral:
            break

        if f(a, funcion) * fc < 0:
            b = c
        else:
            a = c

        i += 1

    # Graficar función
    graficar_funcion(funcion, a, b)

# Método de Newton-Raphson
def metodo_newton_raphson():
    funcion = funcion_entry.get()
    x0 = float(x0_entry.get())
    umbral = float(umbral_entry.get())
    max_iter = int(max_iter_entry.get())

    # Limpiar tabla
    tabla.delete(*tabla.get_children())

    i = 0
    while i < max_iter:
        fx0 = f(x0, funcion)
        dfx0 = df(x0, funcion)

        if dfx0 == 0:
            messagebox.showerror("Error", "La derivada en x0 es cero. El método no converge.")
            return

        x1 = x0 - fx0 / dfx0

        color_fila = "#e8f6ff" if i % 2 == 0 else "#d1e7fd"
        tabla.insert("", "end", values=(i, "{:.8f}".format(x1), "{:.8f}".format(f(x1, funcion))), tags=("even" if i % 2 == 0 else "odd"))

        if abs(f(x1, funcion)) <= umbral:
            break

        x0 = x1
        i += 1

    # Graficar función
    graficar_funcion(funcion, x0 - 1, x0 + 1)

# Función para graficar la ecuación
def graficar_funcion(funcion, a, b):
    x = np.linspace(a - 1, b + 1, 100)
    y = [f(val, funcion) for val in x]

    ax.clear()
    ax.plot(x, y, label=f"f(x) = {funcion}", color='#ff7f50', linewidth=2)
    ax.axhline(0, color='black', linewidth=1)
    ax.axvline(0, color='black', linewidth=1)
    ax.legend()
    canvas.draw()

# Crear ventana
root = tk.Tk()
root.title("Métodos Numéricos")
root.geometry("850x600")
root.configure(bg="#1e3d59")  # Fondo azul oscuro elegante

# Estilo de fuente y colores
estilo_fuente = ("Arial", 12, "bold")
color_fondo = "#1e3d59"
color_texto = "white"
color_botones = "#ff7f50"

# Marco superior para organizar entradas
frame_top = tk.Frame(root, bg=color_fondo)
frame_top.pack(pady=10)

# Etiquetas y entradas en la parte superior
tk.Label(frame_top, text="Función:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=0, column=0, padx=5)
funcion_entry = tk.Entry(frame_top, font=estilo_fuente, width=15)
funcion_entry.grid(row=0, column=1, padx=5)

tk.Label(frame_top, text="a:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=0, column=2, padx=5)
a_entry = tk.Entry(frame_top, font=estilo_fuente, width=7)
a_entry.grid(row=0, column=3, padx=5)

tk.Label(frame_top, text="b:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=0, column=4, padx=5)
b_entry = tk.Entry(frame_top, font=estilo_fuente, width=7)
b_entry.grid(row=0, column=5, padx=5)

tk.Label(frame_top, text="x0:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=0, column=6, padx=5)
x0_entry = tk.Entry(frame_top, font=estilo_fuente, width=7)
x0_entry.grid(row=0, column=7, padx=5)

tk.Label(frame_top, text="Umbral:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=1, column=0, padx=5)
umbral_entry = tk.Entry(frame_top, font=estilo_fuente, width=7)
umbral_entry.grid(row=1, column=1, padx=5)

tk.Label(frame_top, text="Max. Iter.:", fg=color_texto, bg=color_fondo, font=estilo_fuente).grid(row=1, column=2, padx=5)
max_iter_entry = tk.Entry(frame_top, font=estilo_fuente, width=7)
max_iter_entry.grid(row=1, column=3, padx=5)

# Botones para ejecutar los métodos
frame_botones = tk.Frame(root, bg=color_fondo)
frame_botones.pack(pady=10)

boton_biseccion = tk.Button(frame_botones, text="Bisección", command=metodo_biseccion, font=estilo_fuente, bg=color_botones, fg="white", padx=10)
boton_biseccion.grid(row=0, column=0, padx=5)

boton_falsa_posicion = tk.Button(frame_botones, text="Falsa Posición", command=metodo_falsa_posicion, font=estilo_fuente, bg=color_botones, fg="white", padx=10)
boton_falsa_posicion.grid(row=0, column=1, padx=5)

boton_newton_raphson = tk.Button(frame_botones, text="Newton-Raphson", command=metodo_newton_raphson, font=estilo_fuente, bg=color_botones, fg="white", padx=10)
boton_newton_raphson.grid(row=0, column=2, padx=5)

# Marco para la tabla y la gráfica
frame_bottom = tk.Frame(root, bg=color_fondo)
frame_bottom.pack(pady=10, fill="both", expand=True)

# Tabla de resultados con mejor diseño
frame_tabla = tk.Frame(frame_bottom, bg=color_fondo)
frame_tabla.pack(side="left", padx=10)

cols = ("Iteración", "c", "f(c)")
tabla = ttk.Treeview(frame_tabla, columns=cols, show="headings", height=10, style="mystyle.Treeview")
for col in cols:
    tabla.heading(col, text=col, anchor="center")
    tabla.column(col, width=120, anchor="center")

# Definir colores en la tabla
style = ttk.Style()
style.configure("Treeview", font=("Arial", 11), rowheight=25)
style.configure("Treeview.Heading", font=("Arial", 12, "bold"), background="#4a90e2", foreground="white")
style.map("Treeview", background=[("selected", "#ff7f50")])
tabla.tag_configure("even", background="#e8f6ff")
tabla.tag_configure("odd", background="#d1e7fd")

tabla.pack()

# Gráfica
frame_grafica = tk.Frame(frame_bottom, bg=color_fondo)
frame_grafica.pack(side="right", padx=10)

fig, ax = plt.subplots(figsize=(5, 3))
canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.get_tk_widget().pack()

root.mainloop()