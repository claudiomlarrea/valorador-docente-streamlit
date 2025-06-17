from io import BytesIO
import pandas as pd

def generar_excel(df, total, categoria):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Resultados", index=False)
        resumen = pd.DataFrame({"Total": [total], "Categoría": [categoria]})
        resumen.to_excel(writer, sheet_name="Resumen", index=False)
    output.seek(0)
    return output
