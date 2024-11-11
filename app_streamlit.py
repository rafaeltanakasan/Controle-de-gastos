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

# Configurar o título do app
st.title("Controle de Gastos")

# Entradas do usuário
st.header("Adicionar Novo Gasto")
data = st.date_input("Data", datetime.now())
categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Outros"])
descricao = st.text_input("Descrição")
valor = st.number_input("Valor", min_value=0.0, format="%.2f")

# Botão para adicionar o gasto
if st.button("Adicionar Gasto"):
    # Adiciona o novo gasto ao DataFrame histórico
    novo_gasto = pd.DataFrame({
        "Data": [data],
        "Categoria": [categoria],
        "Descrição": [descricao],
        "Valor": [valor]
    })
    historico = pd.concat([historico, novo_gasto], ignore_index=True)
    salvar_historico(historico)  # Salva o histórico atualizado
    st.success("Gasto adicionado com sucesso!")

# Exibe o histórico de gastos
st.header("Histórico de Gastos")
st.dataframe(historico)

# Cálculos
st.header("Resumo dos Gastos")
gasto_por_categoria = historico.groupby("Categoria")["Valor"].sum()
gasto_total = historico["Valor"].sum()

st.write("Total por Categoria:")
st.write(gasto_por_categoria)
st.write("Total Geral:", gasto_total)
