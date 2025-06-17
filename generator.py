import pandas as pd
from io import BytesIO

def generar_excel(df, total, categoria):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Puntajes")
        resumen = pd.DataFrame({
            "Total de puntos": [total],
            "Categoría asignada": [categoria]
        })
        resumen.to_excel(writer, index=False, sheet_name="Resumen")
    output.seek(0)
    return output