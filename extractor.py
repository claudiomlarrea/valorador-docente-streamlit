import fitz  # PyMuPDF

def extraer_items_desde_pdf(uploaded_file):
    texto_extraido = ""
    with fitz.open(stream=uploaded_file.read(), filetype="pdf") as doc:
        for pagina in doc:
            texto_extraido += pagina.get_text()

    items = {
        "Doctorado": 250 if "doctorado" in texto_extraido.lower() else 0,
        "Maestría": 150 if "maestría" in texto_extraido.lower() else 0,
        "Especialización": 75 if "especialización" in texto_extraido.lower() else 0,
        "Profesor Titular": 200 if "profesor titular" in texto_extraido.lower() else 0,
        "Ayudante": 40 if "ayudante" in texto_extraido.lower() else 0,
        "Libro": 120 if "isbn" in texto_extraido.lower() else 0,
        "Investigador": 150 if "investigador" in texto_extraido.lower() else 0,
        "Premio": 60 if "premio" in texto_extraido.lower() or "distinción" in texto_extraido.lower() else 0,
        "Evaluador de tesis": 60 if "jurado de tesis" in texto_extraido.lower() or "evaluador" in texto_extraido.lower() else 0,
    }

    return {k: v for k, v in items.items() if v > 0}