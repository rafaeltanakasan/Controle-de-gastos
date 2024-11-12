import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

# Configuração de Página e Estilo
st.set_page_config(page_title="Controle de Gastos em Ienes", layout="wide")
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
    'Data': [date(2024, 11, 1), date(2024, 11, 2), date(2024, 11, 3)],
    'Categoria': ['Alimentação', 'Transporte', 'Lazer'],
    'Descrição': ['Supermercado', 'Uber', 'Cinema'],
    'Valor (¥)': [1000, 500, 300]
})

# Exibir o Dashboard
st.title("💰 Controle de Gastos em Ienes")
col1, col2 = st.columns([3, 1])

with col1:
    fig = px.bar(historico, x='Categoria', y='Valor (¥)', title="Despesas por Categoria", color="Categoria",
                 labels={'Valor (¥)': 'Valor em Ienes (¥)'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Adicionar Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data", value=date.today())
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (¥)", min_value=0, format="%d")  # Formato inteiro sem casas decimais
        submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        # Adiciona o gasto ao DataFrame
        novo_gasto = pd.DataFrame({
            'Data': [data],
            'Categoria': [categoria],
            'Descrição': [descricao],
            'Valor (¥)': [valor]
        })
        historico = pd.concat([historico, novo_gasto], ignore_index=True)
        st.success("Gasto adicionado com sucesso!")

# Painel com Dados
st.subheader("Histórico de Gastos")
st.table(historico)

# Totalizador em Ienes
gasto_total = historico['Valor (¥)'].sum()
st.write(f"### Total de Gastos: ¥ {gasto_total:,}")
