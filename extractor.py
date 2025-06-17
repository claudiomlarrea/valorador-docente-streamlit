
from typing import Dict
import fitz  # PyMuPDF

def extraer_items_desde_pdf(file) -> Dict[str, int]:
    text = ""
    with fitz.open(stream=file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()

    text = text.lower()

    items_detectados = {}

    # Diccionario de patrones clave y puntajes máximos
    patrones = {
        "doctorado": 250,
        "maestr[ií]a": 150,
        "especializaci[oó]n": 75,
        "profesor titular": 200,
        "profesor asociado": 160,
        "profesor adjunto": 120,
        "jtp": 80,
        "ayudante": 40,
        "tribunal de tesis": 60,
        "publicaci[oó]n con referato": 180,
        "publicaci[oó]n sin referato": 50,
        "libro": 120,
        "cap[ií]tulo de libro": 60,
        "patente": 60,
        "premio": 60,
        "beca": 60,
        "expositor": 40,
        "conferencista": 50,
        "evaluador": 60,
        "jurado": 60,
        "director de tesis": 150,
        "co-director de tesis": 100,
        "investigador": 150,
        "proyecto de investigaci[oó]n": 100,
        "presentaci[oó]n en congreso": 40
    }

    import re
    for clave, puntaje in patrones.items():
        if re.search(clave, text):
            items_detectados[clave.capitalize()] = puntaje

    return items_detectados
