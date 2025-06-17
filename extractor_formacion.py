
import re
import unicodedata

def normalizar(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFKD', texto).encode('ascii', 'ignore').decode('utf-8')
    return texto

def extraer_items_desde_texto(texto):
    texto = normalizar(texto)

    patrones_items = {
        # Formación Académica
        "Títulos de Grado": [
            r"licenciado en [a-záéíóúñ\s]+",
            r"licenciatura en [a-záéíóúñ\s]+",
            r"ingeniero en [a-záéíóúñ\s]+",
            r"contador|abogado|médico|odontólogo"
        ],
        "Cursos de Postgrado": [
            r"curso de postgrado",
            r"curso.*posgrado"
        ],
        "Especializaciones": [
            r"especialista en [a-záéíóúñ\s]+",
            r"especializacion en [a-záéíóúñ\s]+"
        ],
        "Maestrías": [
            r"maestr[ií]a en [a-záéíóúñ\s]+",
            r"mag[íi]ster en [a-záéíóúñ\s]+"
        ],
        "Doctorados": [
            r"doctorado en [a-záéíóúñ\s]+",
            r"doctor en [a-záéíóúñ\s]+"
        ]
    }

    puntajes = {
        "Títulos de Grado": 30,
        "Cursos de Postgrado": 75,
        "Especializaciones": 75,
        "Maestrías": 150,
        "Doctorados": 250
    }

    resultados = {}
    for item, patrones in patrones_items.items():
        for patron in patrones:
            if re.search(patron, texto):
                resultados[item] = puntajes[item]
                break

    return resultados
