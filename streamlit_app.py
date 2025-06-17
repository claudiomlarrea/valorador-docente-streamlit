
import streamlit as st
from extractor import procesar_cv
from generator import generar_excel
import pandas as pd

st.set_page_config(page_title="Valorador Docente - UCCuyo", layout="wide")
st.title("🎓 Universidad Católica de Cuyo")
st.subheader("Secretaría de Investigación")
st.markdown("## Valorador Docente - Resolución 897")

docente = st.text_input("Nombre completo del docente:")

uploaded_file = st.file_uploader("📄 Sube tu CV en PDF (SIGEVA-CONICET)", type=["pdf"])

if uploaded_file and docente:
    st.success("✔️ Archivo cargado correctamente.")
    resultados, total, categoria = procesar_cv(uploaded_file)

    st.markdown("### 📊 Resultados del análisis")
    df = pd.DataFrame(resultados.items(), columns=["Ítem detectado", "Puntaje asignado"])
    st.dataframe(df)
    st.markdown(f"**Total acumulado:** {total} puntos")
    st.markdown(f"**Categoría asignada:** 🏅 {categoria}")

    excel_data = generar_excel(resultados, total, categoria, docente)
    st.download_button("📥 Descargar informe en Excel", excel_data, file_name=f"Informe_{docente}.xlsx")
else:
    st.info("Sube tu CV y completa tu nombre para comenzar el análisis.")
