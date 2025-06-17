
import pandas as pd
from io import BytesIO

def generar_excel(resultados, total, categoria, docente):
    df = pd.DataFrame(resultados.items(), columns=["Ítem", "Puntaje"])
    df.loc[len(df.index)] = ["TOTAL", total]
    df.loc[len(df.index)] = ["CATEGORÍA", categoria]
    df.loc[len(df.index)] = ["DOCENTE", docente]

    output = BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Resultados", index=False)
    output.seek(0)
    return output
