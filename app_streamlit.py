import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração de Página e Estilo
st.set_page_config(page_title="Futuristic Finance App", layout="wide")
st.markdown("""
    <style>
        .main {background-color: #1e1e2e; color: #fafafa; font-family: 'Poppins', sans-serif;}
        h1, h2, h3 {color: #00FFCC;}
        .css-1offfwp {background-color: #323344;}
        button {color: #FFFFFF; background: linear-gradient(145deg, #2f2f3d, #23232b);}
    </style>
""", unsafe_allow_html=True)

# Carregar e Visualizar Dados
historico = pd.DataFrame({
    'Data': ['2024/11/01', '2024/11/02', '2024/11/03'],
    'Categoria': ['Alimentação', 'Transporte', 'Lazer'],
    'Descrição': ['Supermercado', 'Uber', 'Cinema'],
    'Valor': [100.00, 50.00, 30.00]
})

# Exibir o Dashboard
st.title("💰 Controle de Gastos Futurístico")
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.bar(historico, x='Categoria', y='Valor', title="Despesas por Categoria", color="Categoria")
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Adicionar Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data")
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.00, format="%.2f")
        submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        # Lógica para adicionar ao DataFrame
        st.success("Gasto adicionado com sucesso!")

# Painel com Dados
st.subheader("Histórico de Gastos")
st.table(historico)
