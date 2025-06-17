
import pandas as pd

def calcular_puntaje(file):
    # Simula una tabla de puntajes de ejemplo
    data = {
        "Ítem": ["Títulos de Grado", "Maestrías", "Doctorados", "Profesor Titular", "Libros", "Premios, Becas y Distinciones"],
        "Puntaje": [30, 150, 250, 200, 120, 60]
    }
    df = pd.DataFrame(data)
    df["Área"] = ["Formación Académica", "Formación Académica", "Formación Académica",
                  "Docencia", "Producción Académica", "Actividad Científica"]
    df_total = df.groupby("Área").agg({"Puntaje": "sum"}).reset_index()
    df_total["Categoría Sugerida"] = "A definir"
    return df_total
