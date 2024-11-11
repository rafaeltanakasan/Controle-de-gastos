import streamlit as st
import pandas as pd
from datetime import datetime

# Nome do arquivo CSV para salvar o histórico
HISTORICO_ARQUIVO = 'historico_gastos.csv'

# Função para carregar o histórico de gastos do arquivo CSV
def carregar_historico():
    try:
        return pd.read_csv(HISTORICO_ARQUIVO)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])

# Função para salvar o histórico de gastos no arquivo CSV
def salvar_historico(dados):
    dados.to_csv(HISTORICO_ARQUIVO, index=False)

# Carregar o histórico de gastos ao iniciar o app
historico = carregar_historico()

# Configurações gerais
st.set_page_config(page_title="Controle de Gastos", layout="centered")
st.markdown("<style>footer {visibility: hidden;}</style>", unsafe_allow_html=True)

# Título e subtítulo minimalistas
st.title("💰 Controle de Gastos")
st.caption("Organize e monitore seus gastos de forma prática.")

# Seção para entrada de dados com layout em colunas
st.header("Adicionar Gasto")
col1, col2 = st.columns(2)
with col1:
    data = st.date_input("Data", datetime.now())
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Outros"])
with col2:
    descricao = st.text_input("Descrição")
    valor = st.number_input("Valor", min_value=0.0, format="%.2f")

# Botão para adicionar o gasto
if st.button("Adicionar Gasto"):
    novo_gasto = pd.DataFrame({
        "Data": [data],
        "Categoria": [categoria],
        "Descrição": [descricao],
        "Valor": [valor]
    })
    historico = pd.concat([historico, novo_gasto], ignore_index=True)
    salvar_historico(historico)  # Salva o histórico atualizado
    st.success("Gasto adicionado com sucesso!")

# Seção para exibir o histórico e resumo dos gastos
with st.expander("📅 Histórico de Gastos", expanded=True):
    st.dataframe(historico[["Data", "Categoria", "Descrição", "Valor"]])  # Exibe a tabela sem .style

with st.expander("📊 Resumo dos Gastos"):
    gasto_por_categoria = historico.groupby("Categoria")["Valor"].sum()
    gasto_total = historico["Valor"].sum()
    st.write("**Total por Categoria:**")
    st.write(gasto_por_categoria)
    st.write("**Total Geral:**", f"R$ {gasto_total:.2f}")
