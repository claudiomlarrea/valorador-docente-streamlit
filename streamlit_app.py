import streamlit as st
from extractor import extraer_items_desde_cv
from generator import generar_excel
import pandas as pd

st.set_page_config(page_title="Valorador Docente", layout="centered")
st.title("🧠 Valorador Docente - Resolución 897")
st.markdown("**Subí tu CV en PDF o DOCX para evaluar automáticamente tus antecedentes.**")

uploaded_file = st.file_uploader("📄 Elegí tu archivo", type=["pdf", "docx"])

if uploaded_file:
    with st.spinner("Analizando el CV..."):
        items_detectados = extraer_items_desde_cv(uploaded_file)
        total = sum(valor for _, valor in items_detectados)
        df_resultado = pd.DataFrame(items_detectados, columns=["Ítem detectado", "Puntaje asignado"])
        categoria = (
            "BECARIO DE INICIACIÓN (VI)" if total < 100 else
            "INVESTIGADOR EN FORMACIÓN (V)" if total < 250 else
            "INVESTIGADOR ASISTENTE (IV)" if total < 500 else
            "INVESTIGADOR ADJUNTO (III)" if total < 800 else
            "INVESTIGADOR PRINCIPAL (II)" if total < 1100 else
            "INVESTIGADOR SUPERIOR (I)"
        )
        st.subheader("📊 Resultados del análisis")
        st.dataframe(df_resultado, use_container_width=True)
        st.markdown(f"**Total acumulado:** {total} puntos")
        st.markdown(f"**Categoría asignada:** 🥇 {categoria}")

        if st.button("📥 Descargar informe en Excel"):
            excel_file = generar_excel(df_resultado, total, categoria)
            st.download_button("Descargar Excel", data=excel_file, file_name="informe_valoracion.xlsx")
