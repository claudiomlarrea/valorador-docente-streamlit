import fitz  # PyMuPDF
import docx

PATRONES = {
    "Doctorado": 250,
    "Maestría": 150,
    "Especialización": 75,
    "Profesor Titular": 200,
    "Profesor Asociado": 160,
    "Profesor Adjunto": 120,
    "JTP": 80,
    "Ayudante": 40,
    "Libro": 120,
    "Capítulo de libro": 60,
    "Artículo con referato": 180,
    "Artículo sin referato": 50,
    "Investigador": 150,
    "Premio": 60,
    "Proyecto I+D": 100,
    "Evaluador de tesis": 60,
    "Evaluador de publicaciones": 40,
    "Dirección de becario": 60,
    "Dirección de tesista": 150,
    "Dirección de investigador": 150,
    "Gestión universitaria": 100
}

def extraer_texto_pdf(file):
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        return "\n".join([page.get_text() for page in doc])

def extraer_texto_docx(file):
    doc = docx.Document(file)
    return "\n".join([para.text for para in doc.paragraphs])

def extraer_items_desde_cv(file):
    filename = file.name.lower()
    texto = ""
    if filename.endswith(".pdf"):
        texto = extraer_texto_pdf(file)
    elif filename.endswith(".docx"):
        texto = extraer_texto_docx(file)

    texto = texto.lower()
    resultados = []
    for patron, puntaje in PATRONES.items():
        if patron.lower() in texto:
            resultados.append((patron, puntaje))
    return resultados
