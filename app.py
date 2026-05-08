import streamlit as st
import pandas as pd
import plotly.express as px
import base64

st.set_page_config(
    page_title="Análise de Dados Ambientais do Pantanal",
    page_icon="🌿",
    layout="wide"
)

def get_base64(imagem):
    with open(imagem, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_base64 = get_base64("bg.png")

st.markdown(f"""
<style>
.onca {{
    position: fixed;
    bottom: 10px;
    right: 10px;
    width: 520px;
    opacity: 0.6;
    z-index: 0;
    pointer-events: none;
}}

.block-container {{
    padding-top: 2rem;
    max-width: 1100px;
    margin: auto;
}}

div[data-testid="metric-container"] {{
    background-color: rgba(30, 80, 60, 0.18);
    border: 1px solid rgba(80, 160, 120, 0.25);
    padding: 16px;
    border-radius: 12px;
}}

[data-testid="stAppViewContainer"] {{
    background-color: #ffffff;
}}

.stAlert {{
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
}}
</style>

<img src="data:image/png;base64,{img_base64}" class="onca">
""", unsafe_allow_html=True)

st.title("🌿 Análise de Dados Ambientais do Pantanal")

st.markdown("""
Aplicação para leitura, tratamento e visualização de dados ambientais.

**Variáveis monitoradas:**
- 🌡️ Temperatura do ar em °C
- 🌊 Nível do rio em metros
- 🌿 NDVI: índice de vegetação por diferença normalizada
""")

COLUNAS_ESPERADAS = ["data", "temperatura_c", "nivel_rio_m", "ndvi"]

arquivo = st.file_uploader("Envie um arquivo CSV", type=["csv"])

if arquivo is not None:
    df = pd.read_csv(arquivo)
    dataset_id = arquivo.name
    df.columns = df.columns.str.strip()

    if not all(coluna in df.columns for coluna in COLUNAS_ESPERADAS):
        st.error("O CSV deve conter as colunas: data, temperatura_c, nivel_rio_m, ndvi")
        st.stop()

    st.success(f"✅ Arquivo carregado — {len(df)} registros encontrados.")
else:
    df = pd.read_csv("dados_pantanal.csv")
    dataset_id = "dados_pantanal.csv"
    df.columns = df.columns.str.strip()
    st.info("📂 Carregado o conjunto de dados do Pantanal (janeiro/2025). Você pode substituir enviando seu próprio CSV.")


df["data"] = pd.to_datetime(df["data"], errors="coerce")

for coluna in ["temperatura_c", "nivel_rio_m", "ndvi"]:
    df[coluna] = pd.to_numeric(df[coluna], errors="coerce")

df = df.sort_values("data")

valores_ausentes = df.isnull().sum()
total_ausentes = int(valores_ausentes.sum())

if st.session_state.get("dataset_id") != dataset_id:
    st.session_state["dataset_id"] = dataset_id
    st.session_state["mostrar_originais"] = False
    st.session_state["mostrar_graficos"] = False

    if "df_tratado" in st.session_state:
        del st.session_state["df_tratado"]

if "mostrar_originais" not in st.session_state:
    st.session_state["mostrar_originais"] = False

if "mostrar_graficos" not in st.session_state:
    st.session_state["mostrar_graficos"] = False

st.divider()
if st.button("Visualizar Tabela de Dados"):
    st.session_state["mostrar_originais"] = True

if st.session_state["mostrar_originais"]:
    st.subheader("Dados Carregados") 
    df_exibir = df.rename(columns={
        "temperatura_c": "Temperatura (°C)",
        "nivel_rio_m": "Nível do rio (m)",
        "ndvi": "NDVI"
    })
    st.dataframe(df_exibir.head(5), width="stretch")
    st.caption(f"Exibindo 5 de {len(df)} registros. O arquivo completo é usado na análise.")

    st.divider()

    st.subheader("Resumo Inicial dos Dados")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Nº de Registros", len(df))
    col2.metric("Período inicial", df["data"].min().strftime("%d/%m/%Y"))
    col3.metric("Período final", df["data"].max().strftime("%d/%m/%Y"))
    col4.metric("Valores ausentes", total_ausentes)
    st.divider()
    st.subheader("Diagnóstico de Dados Ausentes")
    
    col1, col2, col3 = st.columns(3)

    col1.metric("Temperatura ausente", int(valores_ausentes["temperatura_c"]))
    col2.metric("Nível ausente", int(valores_ausentes["nivel_rio_m"]))
    col3.metric("NDVI ausente", int(valores_ausentes["ndvi"]))

st.divider()

if st.button("Tratar Dados"):
    df_tratado = df.copy()

    for coluna in ["temperatura_c", "nivel_rio_m", "ndvi"]:
        df_tratado[coluna] = df_tratado[coluna].interpolate()

    st.session_state["df_tratado"] = df_tratado
    st.session_state["mostrar_graficos"] = False
    st.success("Dados tratados com interpolação linear.")
    
if "df_tratado" in st.session_state:
    df_tratado = st.session_state["df_tratado"]

    st.subheader("Dados após tratamento")
    df_tratado_exibir = df_tratado.rename(columns={
        "temperatura_c": "Temperatura (°C)",
        "nivel_rio_m": "Nível do rio (m)",
        "ndvi": "NDVI"
    })
    st.dataframe(df_tratado_exibir.head(5), width="stretch")
    
    st.caption(f"Exibindo 5 de {len(df_tratado)} registros. O arquivo completo é usado na análise.")

    st.caption(
        "A interpolação linear foi utilizada por ser adequada para séries temporais contínuas, "
        "preservando a tendência entre observações conhecidas."
    )

    st.subheader("Estatísticas básicas")

    col1, col2, col3 = st.columns(3)
    col1.metric("Média temperatura", f"{df_tratado['temperatura_c'].mean():.2f} °C")
    col2.metric("Média nível do rio", f"{df_tratado['nivel_rio_m'].mean():.2f} m")
    col3.metric("Média NDVI", f"{df_tratado['ndvi'].mean():.2f}")

    col4, col5, col6 = st.columns(3)
    col4.metric("Temperatura máx.", f"{df_tratado['temperatura_c'].max():.2f} °C")
    col5.metric("Nível máx.", f"{df_tratado['nivel_rio_m'].max():.2f} m")
    col6.metric("NDVI máx.", f"{df_tratado['ndvi'].max():.2f}")

    st.divider()

    if st.button("Gerar gráficos"):
        st.session_state["mostrar_graficos"] = True

    if st.session_state["mostrar_graficos"]:
        st.subheader("Visualizações")

        fig_temp = px.line(
            df_tratado,
            x="data",
            y="temperatura_c",
            markers=True,
            title="Evolução da temperatura",
            labels={"temperatura_c": "Temperatura (°C)", "data": "Data"}
        )
        st.plotly_chart(fig_temp, width="stretch", key="grafico_temperatura")

        fig_nivel = px.line(
            df_tratado,
            x="data",
            y="nivel_rio_m",
            markers=True,
            title="Evolução do nível do rio",
            labels={"nivel_rio_m": "Nível do rio (m)", "data": "Data"}
        )
        st.plotly_chart(fig_nivel, width="stretch", key="grafico_nivel_rio")

        fig_ndvi = px.line(
            df_tratado,
            x="data",
            y="ndvi",
            markers=True,
            title="Evolução do NDVI",
            labels={"ndvi": "NDVI", "data": "Data"}
        )
        st.plotly_chart(fig_ndvi, width="stretch", key="grafico_ndvi")

        df_normalizado = df_tratado.copy()
        for coluna in ["temperatura_c", "nivel_rio_m", "ndvi"]:
            minv = df_normalizado[coluna].min()
            maxv = df_normalizado[coluna].max()
            df_normalizado[coluna] = (df_normalizado[coluna] - minv) / (maxv - minv)

        fig_comparativo = px.line(
            df_normalizado,
            x="data",
            y=["temperatura_c", "nivel_rio_m", "ndvi"],
            markers=True,
            title="Comparativo entre variáveis ambientais (valores normalizados)"
        )
        st.plotly_chart(fig_comparativo, width="stretch", key="grafico_comparativo")
        st.caption(
            "Variáveis normalizadas entre 0 e 1 para permitir comparação visual na mesma escala. "
            "Valores originais são exibidos nos gráficos individuais acima."
        )

        st.caption(
            "O gráfico comparativo permite observar padrões gerais entre temperatura, nível do rio e NDVI."
        )

elif st.session_state["mostrar_originais"]:
    st.warning("Execute o tratamento dos dados antes de visualizar estatísticas e gráficos.")