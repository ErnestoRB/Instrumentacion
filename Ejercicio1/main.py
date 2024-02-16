import pandas as pd
import matplotlib.pyplot as plt
import tabula
import os
import tkinter as tk
from tkinter import filedialog
from fpdf import FPDF, XPos, YPos

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if file_path:
        entry_input.delete(0, tk.END)
        entry_input.insert(0, file_path)

def show_alert(message):
    alert_window = tk.Toplevel(root)
    alert_window.title("Alerta")
    alert_label = tk.Label(alert_window, text=message, fg="red")
    alert_label.pack(padx=10, pady=10)

def process_pdf():
    pdf_path = entry_input.get()
    if not pdf_path:
        show_alert("Por favor, selecciona un archivo.")
        return
    
    output_path = entry_output.get()
    if not output_path:
        show_alert("Por favor, ingresa un nombre de archivo de salida.")
        return

    if not os.path.exists("output"):
        os.mkdir("output")

    df = tabula.read_pdf(pdf_path, pages="all")
    df = df[0]
    df = df.dropna()
    v_real = 127
    voltaje = df.iloc[:, 2]
    err_df = pd.DataFrame()
    err_df["voltaje"] = voltaje
    err_df["err_abs"] = voltaje.apply(lambda x: abs(v_real - x))
    err_df["err_rel"] = err_df["err_abs"].apply(lambda x: x / abs(v_real))

    moda = voltaje.mode().max()
    prom = voltaje.mean()
    mediana = voltaje.median()

    desv_est = voltaje.std()
    desv_prom = (voltaje - prom).abs().mean()

    rango = voltaje.max() - voltaje.min()
    varianza = voltaje.var()
    coef_variacion = desv_est / prom

    plt.figure("Histograma")
    voltaje.hist()  # Histograma
    plt.axvline(x=prom, color="r", label="Promedio")
    plt.axvline(x=mediana, color="g", label="Mediana")
    plt.title("Histograma de voltaje")
    plt.xlabel("Voltaje")
    plt.ylabel("Ocurrencias")
    plt.savefig("output/histograma.png")  # Guardar histograma
    plt.figure("Variacion de voltaje")
    plt.scatter(range(1, len(voltaje) + 1), voltaje)
    plt.title("Variacion de voltaje sobre tiempo")
    plt.xlabel("# Elemento")
    plt.ylabel("Voltaje")
    plt.savefig("output/variacion_voltaje.png")  # Guardar el gráfico de dispersión


    pdf = FPDF()
    pdf.add_page()
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 20, "Reporte", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.image("output/histograma.png", w=100, h=100, x=(pdf.epw / 2) - 50)
    pdf.image("output/variacion_voltaje.png", w=100, h=100, x=(pdf.epw / 2) - 50)
    pdf.set_font('Arial', '', 12)
    with pdf.table() as table:
        row = table.row()
        row.cell("Voltaje")
        row.cell("Voltaje absoluto")
        row.cell("Voltaje relativo")
        for i, data_row in err_df.iterrows():
            row = table.row()
            for i, value in data_row.items():
                if type(value) is float:
                    row.cell(f"{value:.2f}")
                else:
                    row.cell(str(value))

    pdf.cell(0, 10, f"Media: {prom:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Mediana: {mediana:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Moda: {moda:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Desviacion media: {desv_prom:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Desviacion Estandar: {desv_est:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Varianza: {varianza:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Rango: {rango:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Coeficiente de variacion: {coef_variacion:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.cell(0, 10, f"Semi-Intercuartil (Q1-Q3)/2 : {coef_variacion:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

    pdf.output(os.path.join("output", entry_output.get().replace(".pdf", "") + ".pdf"))
    plt.show()  # Mostrar el gráfico

root = tk.Tk()
root.title("Análisis de voltaje")

label_input = tk.Label(root, text="Archivo de PDF:")
label_input.grid(row=0, column=0, padx=10, pady=10)

entry_input = tk.Entry(root, width=50)
entry_input.grid(row=0, column=1, padx=10, pady=10)

button_browse = tk.Button(root, text="Seleccionar archivo", command=browse_file)
button_browse.grid(row=0, column=2, padx=10, pady=10)

label_output = tk.Label(root, text="Nombre del archivo a generar:")
label_output.grid(row=1, column=0, padx=10, pady=10)

entry_output = tk.Entry(root, width=50)
entry_output.grid(row=1, column=1, padx=10, pady=10)
entry_output.insert(0, "report")

label_output = tk.Label(root, text=".pdf")
label_output.grid(row=1, column=2, padx=10, pady=10)

button_execute = tk.Button(root, text="Analizar y generar reporte", command=process_pdf)
button_execute.grid(row=3, column=0, columnspan=3, pady=20)
root.mainloop()
