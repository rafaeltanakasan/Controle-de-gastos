import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Nome do arquivo CSV para salvar o histórico
HISTORICO_ARQUIVO = 'historico_gastos.csv'

# Função para carregar e salvar histórico de gastos
def carregar_historico():
    try:
        return pd.read_csv(HISTORICO_ARQUIVO)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])

def salvar_historico(dados):
    dados.to_csv(HISTORICO_ARQUIVO, index=False)

# Função para converter dados para CSV para download
@st.cache_data
def converter_para_csv(dados):
    return dados.to_csv(index=False).encode('utf-8')

# Carregar histórico de gastos ao iniciar o app
historico = carregar_historico()

# Configurações gerais
st.set_page_config(page_title="Controle de Gastos", layout="centered", page_icon="💸")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Título e subtítulo minimalistas
st.title("💰 Controle de Gastos")
st.caption("Organize e monitore seus gastos de forma prática.")

# Seção para entrada de dados
st.header("Adicionar Gasto")
col1, col2 = st.columns(2)
with col1:
    data = st.date_input("Data", datetime.now())
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Outros"])
with col2:
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")

if st.button("Adicionar Gasto"):
    novo_gasto = pd.DataFrame({
        "Data": [data],
        "Categoria": [categoria],
        "Descrição": [descricao],
        "Valor": [valor]
    })
    historico = pd.concat([historico, novo_gasto], ignore_index=True)
    salvar_historico(historico)  
    st.success("Gasto adicionado com sucesso!")

# Filtro por categoria e data
st.header("Filtrar Gastos")
categorias_unicas = historico['Categoria'].unique()
categoria_filtro = st.selectbox("Filtrar por Categoria", options=["Todas"] + list(categorias_unicas))
data_inicial = st.date_input("Data Inicial", historico['Data'].min() if not historico.empty else datetime.now())
data_final = st.date_input("Data Final", historico['Data'].max() if not historico.empty else datetime.now())

# Aplicação dos filtros
if categoria_filtro != "Todas":
    historico_filtrado = historico[(historico["Categoria"] == categoria_filtro)]
else:
    historico_filtrado = historico
historico_filtrado = historico_filtrado[(pd.to_datetime(historico_filtrado["Data"]) >= pd.to_datetime(data_inicial)) &
                                        (pd.to_datetime(historico_filtrado["Data"]) <= pd.to_datetime(data_final))]
st.dataframe(historico_filtrado)

# Gráficos
st.header("Gráficos de Gastos")
fig1, ax1 = plt.subplots()
historico.groupby("Categoria")["Valor"].sum().plot(kind="bar", ax=ax1)
ax1.set_ylabel("Total Gasto")
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
historico.groupby("Data")["Valor"].sum().plot(ax=ax2)
ax2.set_ylabel("Total Gasto Diário")
st.pyplot(fig2)

# Exportar histórico
csv = converter_para_csv(historico)
st.download_button(
    label="📥 Baixar Histórico",
    data=csv,
    file_name="historico_gastos.csv",
    mime="text/csv"
)

# Limite de gastos e alerta
st.header("Configurações de Limite de Gasto")
limite = st.number_input("Defina o Limite de Gasto Mensal", min_value=0.0, format="%.2f")
total_mes = historico[pd.to_datetime(historico["Data"]).dt.month == datetime.now().month]["Valor"].sum()

if total_mes >= limite > 0:
    st.error("⚠️ Atenção! Você ultrapassou o limite de gasto mensal!")
elif limite > 0 and total_mes >= 0.8 * limite:
    st.warning("⚠️ Aviso! Você está próximo de ultrapassar o limite de gasto mensal!")

# Resumo mensal
st.header("Resumo Mensal dos Gastos")
mes_selecionado = st.selectbox("Escolha o Mês", options=pd.to_datetime(historico["Data"]).dt.strftime('%Y-%m').unique())
historico_mes = historico[pd.to_datetime(historico["Data"]).dt.strftime('%Y-%m') == mes_selecionado]

gasto_por_categoria_mes = historico_mes.groupby("Categoria")["Valor"].sum()
gasto_total_mes = historico_mes["Valor"].sum()

st.write("Total por Categoria:")
st.write(gasto_por_categoria_mes)
st.write("Total do Mês:", f"R$ {gasto_total_mes:.2f}") de 
