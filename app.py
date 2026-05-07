import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Análise de Dados Ambientais do Pantanal",
    page_icon="🌿",
    layout="wide"
)

st.title("Análise de Dados Ambientais do Pantanal")

st.markdown("""
Aplicação para leitura, tratamento e visualização de dados ambientais.
O usuário pode enviar um arquivo CSV próprio ou utilizar o conjunto de dados de exemplo.

**Variáveis monitoradas:**
- 🌡️ Temperatura — Temperatura do ar em graus Celsius
- 🌊 Nivel do rio — Nível do rio em metros
- 🌿 Ndvi — Índice de Vegetação por Diferença Normalizada (NDVI): mede a densidade e saúde da cobertura vegetal via satélite. Valores próximos a 1 indicam vegetação densa e saudável.
""")

COLUNAS_ESPERADAS = ["data", "temperatura_c", "nivel_rio_m", "ndvi"]

arquivo = st.file_uploader("Envie um arquivo CSV", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)
else:
    df = pd.read_csv("dados_pantanal.csv")

df.columns = df.columns.str.strip()

if not all(coluna in df.columns for coluna in COLUNAS_ESPERADAS):
    st.error("O CSV deve conter as colunas: data, temperatura_c, nivel_rio_m, ndvi")
    st.stop()

df["data"] = pd.to_datetime(df["data"], errors="coerce")

for coluna in ["temperatura_c", "nivel_rio_m", "ndvi"]:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

st.subheader("Dados originais")

st.dataframe(df, width="stretch")

sst.subheader("Diagnóstico de dados")
valores_ausentes = df.isnull().sum()
st.write("Valores ausentes por coluna:")
st.dataframe(valores_ausentes.rename("ausentes"))
st.caption("Valores ausentes foram preenchidos por interpolação linear, preservando a tendência temporal da série.")
df_tratado = df.sort_values("data").copy()

for coluna in ["temperatura_c", "nivel_rio_m", "ndvi"]:
    df_tratado[coluna] = df_tratado[coluna].interpolate()

st.subheader("Dados após tratamento")
st.dataframe(df_tratado, width="stretch")

st.subheader("Estatísticas básicas")

col1, col2, col3 = st.columns(3)

col1.metric("Média temperatura", f"{df_tratado['temperatura_c'].mean():.2f} °C")
col2.metric("Média nível do rio", f"{df_tratado['nivel_rio_m'].mean():.2f} m")
col3.metric("Média NDVI", f"{df_tratado['ndvi'].mean():.2f}")

st.subheader("Visualizações")

fig_temp = px.line(
    df_tratado,
    x="data",
    y="temperatura_c",
    title="Evolução da temperatura"
)
st.plotly_chart(fig_temp, width="stretch")

fig_nivel = px.line(
    df_tratado,
    x="data",
    y="nivel_rio_m",
    title="Evolução do nível do rio"
)
st.plotly_chart(fig_nivel, width="stretch")

fig_ndvi = px.line(
    df_tratado,
    x="data",
    y="ndvi",
    title="Evolução do NDVI"
)
st.plotly_chart(fig_ndvi, width="stretch")
st.plotly_chart(fig_ndvi, width="stretch")
st.caption("NDVI: valores entre 0.6 e 0.9 indicam vegetação típica de áreas úmidas como o Pantanal.")