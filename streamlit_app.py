
import streamlit as st
import pandas as pd
import fitz  # PyMuPDF
import docx
import base64
from io import BytesIO

st.set_page_config(page_title="Valorador Docente", layout="centered")

st.markdown("<h1 style='text-align: center; color: navy;'>Universidad Católica de Cuyo</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: navy;'>Secretaría de Investigación</h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: navy;'>Valorador Docente</h3>", unsafe_allow_html=True)

# Ítems y puntajes actualizados según Resolución 897
ITEMS = {
    "Formación Académica": {
        "Títulos de Grado": 30,
        "Cursos de Postgrado": 75,
        "Especializaciones": 75,
        "Maestrías": 150,
        "Doctorados": 250,
        "_max": 580
    },
    "Docencia en Instituciones Universitarias": {
        "Profesor Titular": 200,
        "Profesor Asociado": 160,
        "Profesor Adjunto": 120,
        "Jefe de Trabajos Prácticos": 80,
        "Ayudante de primera categoría": 40,
        "Integrante de Tribunal de concursos docentes": 60,
        "Docencia en Postgrados acreditados": 100,
        "Docencia en Postgrados no acreditados": 50,
        "Integrante de Tribunal de Tesis de Postgrado": 60,
        "_max": 870
    },
    "Investigación Científica y Tecnológica": {
        "Dirección de Programa de Investigación": 200,
        "Co-dirección de Programa o Director de proyecto": 150,
        "Co-dirección de Proyecto": 100,
        "Integrante de proyecto con un año como mínimo": 60,
        "Auxiliar o becario o adscripto": 30,
        "_max": 540
    },
    "Producción Académica": {
        "Libros": 120,
        "Capítulo de libro": 60,
        "Patente o registro de propiedad intelectual": 60,
        "Publicación con referato": 180,
        "Publicación sin referato en medios académicos-científicos": 50,
        "_max": 470
    },
    "Actividad Científica": {
        "Premios, Becas y Distinciones": 60,
        "Conferencista por invitación": 50,
        "Expositor o panelista": 40,
        "Organizador o coordinador": 30,
        "Asistente": 20,
        "Desarrollo científico-tecnológico con evaluación externa": 200,
        "Desarrollo científico-tecnológico sin evaluación": 50,
        "Miembro de Sociedades Científicas": 100,
        "Miembro de Comisión Evaluadora de Investigaciones": 100,
        "_max": 650
    },
    "Formación de Recursos Humanos": {
        "Dirección de tesis de postgrado": 150,
        "Co-dirección de tesis postgrado": 100,
        "Dirección de investigadores": 150,
        "Co-dirección de investigadores": 100,
        "Dirección de becarios o pasantes": 60,
        "Dirección de auxiliares de docencia": 30,
        "Dirección de tesis de grado": 30,
        "Co-dirección de tesis de grado": 20,
        "_max": 640
    },
    "Gestión Universitaria": {
        "Rector": 100,
        "Vicerrector o Directorio": 80,
        "Decano": 80,
        "Vicedecano": 60,
        "Secretario de Universidad": 60,
        "Secretario de Facultad": 40,
        "Director de centro/instituto/escuela": 35,
        "Co-director": 20,
        "Consejero de Consejo Superior": 15,
        "Consejero de Facultad o Directivo": 10,
        "Responsable de programa institucional": 35,
        "Participante de programa institucional": 10,
        "Miembro de comisiones asesoras o consejero departamental": 10,
        "Otros antecedentes de interés": 10,
        "_max": 565
    }
}

def leer_texto_cv(uploaded_file):
    if uploaded_file.name.endswith(".pdf"):
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        return " ".join([page.get_text() for page in doc])
    elif uploaded_file.name.endswith(".docx"):
        doc = docx.Document(uploaded_file)
        return " ".join([p.text for p in doc.paragraphs])
    return ""

def analizar_cv(texto):
    resultados = []
    total_general = 0
    for area, items in ITEMS.items():
        subtotal = 0
        encontrados = []
        for item, puntaje in items.items():
            if item.startswith("_"):
                continue
            if item.lower() in texto.lower():
                subtotal += puntaje
                encontrados.append((item, puntaje))
        subtotal = min(subtotal, items["_max"])
        total_general += subtotal
        resultados.append((area, subtotal, encontrados))
    return resultados, total_general

def generar_excel(resultado, total):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        rows = []
        for area, subtotal, detalles in resultado:
            for item, pts in detalles:
                rows.append([area, item, pts])
        df = pd.DataFrame(rows, columns=["Área", "Ítem", "Puntaje"])
        df.loc[len(df.index)] = ["TOTAL", "", total]
        df.to_excel(writer, index=False, sheet_name="Valoración")
    return output.getvalue()

uploaded = st.file_uploader("Subí el CV en PDF o Word", type=["pdf", "docx"])
if uploaded:
    texto = leer_texto_cv(uploaded)
    resultado, total = analizar_cv(texto)
    for area, subtotal, detalles in resultado:
        st.subheader(f"{area} – Total: {subtotal} puntos")
        for item, pts in detalles:
            st.markdown(f"- {item}: {pts} puntos")
    st.success(f"Total general: {total} puntos")
    
    # Categoría según total
    if total >= 1500:
        categoria = "Investigador Superior (I)"
    elif total >= 1000:
        categoria = "Investigador Principal (II)"
    elif total >= 600:
        categoria = "Investigador Independiente (III)"
    elif total >= 300:
        categoria = "Investigador Adjunto (IV)"
    elif total >= 1:
        categoria = "Investigador Asistente (V)"
    else:
        categoria = "Becario de Iniciación (VI)"
    st.info(f"Categoría asignada: **{categoria}**")

    excel = generar_excel(resultado, total)
    b64 = base64.b64encode(excel).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="valoracion_docente.xlsx">📥 Descargar informe en Excel</a>'
    st.markdown(href, unsafe_allow_html=True)
