import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cotações Históricas", page_icon="💱", layout="centered")

st.title("💱 Cotações Históricas (últimos 30 dias)")
st.write("Dados reais fornecidos pela [AwesomeAPI](https://docs.awesomeapi.com.br/), em relação ao Real (BRL).")

MOEDAS = {
    "Dólar (USD)": "USD",
    "Euro (EUR)": "EUR",
    "Bitcoin (BTC)": "BTC",
}

moeda_label = st.selectbox("Escolha a moeda:", list(MOEDAS.keys()))
moeda_codigo = MOEDAS[moeda_label]


@st.cache_data(ttl=600)
def buscar_historico(codigo: str) -> pd.DataFrame:
    url = f"https://economia.awesomeapi.com.br/json/daily/{codigo}-BRL/30"
    resposta = requests.get(url, timeout=10)
    resposta.raise_for_status()
    dados = resposta.json()

    if not dados:
        raise ValueError("A API retornou uma lista vazia de cotações.")

    df = pd.DataFrame(dados)
    df["data"] = pd.to_datetime(df["timestamp"].astype(int), unit="s")
    df["fechamento"] = df["bid"].astype(float)
    df = df.sort_values("data")
    df["data_formatada"] = df["data"].dt.strftime("%d/%m/%Y")
    return df[["data", "data_formatada", "fechamento"]]


try:
    with st.spinner("Buscando dados na AwesomeAPI..."):
        df = buscar_historico(moeda_codigo)
except requests.exceptions.RequestException:
    st.error("Não foi possível conectar à AwesomeAPI. Verifique sua conexão com a internet e tente novamente.")
    st.stop()
except (ValueError, KeyError):
    st.error("Não foi possível interpretar os dados retornados pela API. Tente novamente mais tarde.")
    st.stop()

st.subheader(f"Evolução do preço — {moeda_label} → BRL")
grafico = df.set_index("data_formatada")[["fechamento"]]
st.line_chart(grafico)

preco_maximo = df["fechamento"].max()
preco_minimo = df["fechamento"].min()

col1, col2 = st.columns(2)
col1.metric("Preço mais alto no período", f"R$ {preco_maximo:,.2f}")
col2.metric("Preço mais baixo no período", f"R$ {preco_minimo:,.2f}")

with st.expander("Ver dados brutos"):
    st.dataframe(
        df[["data_formatada", "fechamento"]].rename(
            columns={"data_formatada": "Data", "fechamento": "Fechamento (R$)"}
        ),
        hide_index=True,
        width="stretch",
    )
