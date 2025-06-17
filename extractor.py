from PyPDF2 import PdfReader

ITEMS = {
    "doctorado": ("Doctorado", 250),
    "maestría": ("Maestría", 150),
    "especialización": ("Especialización", 75),
    "título de grado": ("Título de Grado", 30),
    "profesor titular": ("Profesor Titular", 200),
    "profesor asociado": ("Profesor Asociado", 160),
    "profesor adjunto": ("Profesor Adjunto", 120),
    "jtp": ("Jefe de Trabajos Prácticos", 80),
    "ayudante": ("Ayudante", 40),
    "tribunal de tesis": ("Evaluador de tesis", 60),
    "investigador": ("Investigador", 150),
    "proyecto de investigación": ("Proyecto de investigación", 100),
    "libro": ("Libro", 120),
    "capítulo": ("Capítulo de libro", 60),
    "artículo con referato": ("Publicación con referato", 180),
    "premio": ("Premio", 60),
    "beca": ("Beca", 30),
    "extensión": ("Actividad de extensión", 30),
    "evaluador": ("Evaluador", 60)
}

MAX_POR_CATEGORIA = {
    "Formación Académica": 580,
    "Docencia": 870,
    "Investigación": 540,
    "Producción Académica": 470,
    "Actividad Científica": 650,
    "Formación de Recursos Humanos": 640,
    "Gestión Universitaria": 565
}

def extraer_items_desde_pdf(file):
    reader = PdfReader(file)
    texto = ""
    for page in reader.pages:
        texto += page.extract_text().lower() + "
"

    resultados = []
    usados = set()
    for palabra_clave, (descripcion, puntaje) in ITEMS.items():
        if palabra_clave in texto and descripcion not in usados:
            resultados.append({"Ítem detectado": descripcion, "Puntaje asignado": puntaje})
            usados.add(descripcion)

    return resultados