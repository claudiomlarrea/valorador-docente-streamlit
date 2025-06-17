import streamlit as st
import pandas as pd
from extractor import extraer_items_desde_pdf
from generator import generar_excel

st.set_page_config(page_title="🧠 Valorador Docente - Resolución 897", layout="centered")

st.title("🧠 Valorador Docente - Resolución 897")
st.write("Subí tu CV generado por SIGEVA-CONICET (PDF) para analizarlo automáticamente.")

uploaded_file = st.file_uploader("📄 Subí tu CV aquí", type=["pdf", "docx"])

if uploaded_file:
    st.success("✅ Archivo cargado correctamente. Analizando...")
    items_detectados = extraer_items_desde_pdf(uploaded_file)

    if not items_detectados:
        st.warning("⚠️ No se detectaron ítems reconocibles. Revisá el formato del archivo.")
    else:
        df = pd.DataFrame(items_detectados)
        total = df["Puntaje asignado"].sum()

        # Asignar categoría según total
        if total >= 1100:
            categoria = "🥇 INVESTIGADOR SUPERIOR (I)"
        elif total >= 900:
            categoria = "🥈 INVESTIGADOR PRINCIPAL (II)"
        elif total >= 700:
            categoria = "🥉 INVESTIGADOR INDEPENDIENTE (III)"
        elif total >= 500:
            categoria = "🏅 INVESTIGADOR ASISTENTE (IV)"
        elif total >= 300:
            categoria = "🏅 BECARIO POSTDOCTORAL (V)"
        else:
            categoria = "🎓 BECARIO DE INICIACIÓN (VI)"

        st.subheader("📊 Resultados del análisis")
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Total acumulado:** {total} puntos")
        st.markdown(f"**Categoría asignada:** {categoria}")

        # Descargar informe en Excel
        excel_file = generar_excel(df, total, categoria)
        st.download_button("📥 Descargar informe en Excel", data=excel_file, file_name="informe_valorador.xlsx")