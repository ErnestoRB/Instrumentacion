import pandas as pd
import matplotlib.pyplot as plt
import tabula 
import os
from fpdf import FPDF, XPos, YPos

if not os.path.exists("output"):
   os.mkdir("output")
   
   

df = tabula.read_pdf("./input.pdf", pages="all")
df = df[0]
df = df.dropna()
v_real = 127
print(df.head())
voltaje = df.iloc[:,2]
print(voltaje)
err_df = pd.DataFrame()
err_df["voltaje"] = voltaje
err_df["err_abs"] = voltaje.apply(lambda x: abs(v_real-x))
err_df["err_rel"] = err_df["err_abs"].apply(lambda x: x / abs(v_real))

moda = voltaje.mode().max()
prom = voltaje.mean()
mediana = voltaje.median()

desv_est = voltaje.std()
desv_prom = (voltaje - prom).abs().mean()

rango = voltaje.max() - voltaje.min()
varianza = voltaje.var()
coef_variacion = desv_est / prom
inter = (voltaje.quantile(.25) - voltaje.quantile(.50)) / 2
voltaje.hist() #histograma

plt.axvline(x=prom, color="r", label="Promedio") # Linea 
plt.axvline(x=mediana, color="g", label="Mediana")
plt.title("Histograma de voltaje")
plt.xlabel("Voltaje")
plt.ylabel("Ocurrencias")

pdf = FPDF()
pdf.add_page()
pdf.set_font('Arial', 'B', 16)

pdf.cell(0, 20, "Reporte",align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
plt.savefig("output/histograma.png") # Guardar histograma
pdf.image("output/histograma.png", w=100, h=100, x=(pdf.epw/2)-50)
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


pdf.cell(0,10, f"Media: {prom:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Mediana: {mediana:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Moda: {moda:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Desviacion media: {desv_prom:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Desviacion Estandar: {desv_est:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Varianza: {varianza:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Rango: {rango:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Coeficiente de variacion: {coef_variacion:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
pdf.cell(0,10, f"Semi-Intercuartil (Q1-Q3)/2 : {coef_variacion:.2f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)

pdf.output("output/report.pdf")
plt.show()
plt.scatter(range(1,len(voltaje)+1),voltaje)
plt.title("Variacion de voltaje sobre tiempo")
plt.xlabel("Elemento")
plt.ylabel("Voltaje")
plt.show()
