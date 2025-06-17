import streamlit as st
import pandas as pd
from extractor import extraer_items_desde_pdf

st.title("🧠 Valorador Docente - Resolución 897")
st.write("La app se ha desplegado correctamente. Ahora podés empezar a cargar funcionalidades.")

uploaded_file = st.file_uploader("Subí tu CV para análisis automático mejorado (PDF, Word o texto)", type=["pdf", "docx", "txt"])
if uploaded_file:
    st.success("📄 Archivo cargado correctamente. Analizando...")
    items_detectados = extraer_items_desde_pdf(uploaded_file)
    if isinstance(items_detectados, dict) and items_detectados:
        df = pd.DataFrame([{'Ítem detectado': k, 'Puntaje asignado': v} for k, v in items_detectados.items()])
        total = df['Puntaje asignado'].sum()

        if total >= 1000:
            categoria = "🥇 INVESTIGADOR SUPERIOR (I)"
        elif total >= 700:
            categoria = "🥈 INVESTIGADOR PRINCIPAL (II)"
        elif total >= 400:
            categoria = "🥉 INVESTIGADOR ADJUNTO (III)"
        else:
            categoria = "🎓 BECARIO DE INICIACIÓN (VI)"

        st.subheader("📊 Resultados del análisis")
        st.dataframe(df, use_container_width=True)
        st.markdown(f"**Total acumulado:** {total} puntos")
        st.markdown(f"**Categoría asignada:** {categoria}")

        # Descargar Excel
        df.to_excel("reporte_puntajes.xlsx", index=False)
        with open("reporte_puntajes.xlsx", "rb") as f:
            st.download_button("📥 Descargar informe en Excel", data=f, file_name="reporte_puntajes.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    else:
        st.warning("⚠️ No se detectaron ítems válidos en el archivo.")