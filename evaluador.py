import pandas as pd

PUNTAJES = {
    "Doctorado": 250,
    "Maestría": 150,
    "Especialización": 75,
    "Profesor Titular": 200,
    "Ayudante": 40,
    "Investigador": 150,
    "Libro": 120,
    "Premio": 60,
    "Evaluador de tesis": 60,
    "Artículo": 50,
    "Capítulo de libro": 40,
    "Ponencia": 30
}

def evaluar_items_detectados(df_items):
    conteo = df_items["Ítem detectado"].value_counts().to_dict()
    resultados = []
    for item, puntaje in PUNTAJES.items():
        cantidad = conteo.get(item, 0)
        if cantidad > 0:
            resultados.append({
                "Ítem detectado": item,
                "Cantidad": cantidad,
                "Puntaje asignado": cantidad * puntaje
            })
    df_resultados = pd.DataFrame(resultados)
    total = df_resultados["Puntaje asignado"].sum()
    categoria = asignar_categoria(total)
    return df_resultados, total, categoria

def asignar_categoria(puntaje_total):
    if puntaje_total >= 1000:
        return "INVESTIGADOR SUPERIOR (I)"
    elif puntaje_total >= 800:
        return "INVESTIGADOR PRINCIPAL (II)"
    elif puntaje_total >= 600:
        return "INVESTIGADOR INDEPENDIENTE (III)"
    elif puntaje_total >= 400:
        return "INVESTIGADOR ADJUNTO (IV)"
    else:
        return "INVESTIGADOR ASISTENTE (V)"
