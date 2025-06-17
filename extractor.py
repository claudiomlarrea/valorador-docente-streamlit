
import fitz  # PyMuPDF

PUNTAJES = {
    "Doctorado": 250,
    "Maestría": 150,
    "Especialización": 75,
    "Título de Grado": 30,
    "Profesor Titular": 200,
    "Profesor Asociado": 160,
    "Profesor Adjunto": 120,
    "JTP": 80,
    "Ayudante": 40,
    "Tribunal docente": 60,
    "Docencia Postgrado acreditado": 100,
    "Docencia Postgrado no acreditado": 50,
    "Tribunal de Tesis": 60,
    "Director de Proyecto": 200,
    "Codirector de Proyecto": 150,
    "Investigador": 150,
    "Libro": 120,
    "Capítulo de libro": 60,
    "Publicación con referato": 180,
    "Publicación sin referato": 50,
    "Premio": 60,
    "Participación en congreso": 50,
    "Evaluación de tesis": 50
}

def procesar_cv(file):
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    resultados = {}
    total = 0
    for item, pts in PUNTAJES.items():
        if item.lower() in text.lower():
            resultados[item] = pts
            total += pts

    categoria = asignar_categoria(total)
    return resultados, total, categoria

def asignar_categoria(total):
    if total >= 1500:
        return "INVESTIGADOR SUPERIOR (I)"
    elif total >= 1000:
        return "INVESTIGADOR PRINCIPAL (II)"
    elif total >= 600:
        return "INVESTIGADOR INDEPENDIENTE (III)"
    elif total >= 300:
        return "INVESTIGADOR ADJUNTO (IV)"
    elif total >= 1:
        return "INVESTIGADOR ASISTENTE (V)"
    else:
        return "BECARIO DE INICIACIÓN (VI)"
