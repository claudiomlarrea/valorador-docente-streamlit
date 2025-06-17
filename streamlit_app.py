import streamlit as st
import pandas as pd
from evaluador import evaluar_items_detectados

st.title("🧠 Valorador Docente - Resolución 897")

archivo_csv = st.file_uploader("Cargá el archivo CSV con ítems detectados", type=["csv"])
if archivo_csv is not None:
    df_items = pd.read_csv(archivo_csv)
    resultados, total, categoria = evaluar_items_detectados(df_items)
    st.subheader("📊 Resultados del análisis")
    st.dataframe(resultados)
    st.markdown(f"**Total acumulado:** {total} puntos")
    st.markdown(f"**Categoría asignada:** 🥇 {categoria}")
    resultados.to_excel("informe_valorador.xlsx", index=False)
    with open("informe_valorador.xlsx", "rb") as f:
        st.download_button("📥 Descargar informe en Excel", f, file_name="informe_valorador.xlsx")
