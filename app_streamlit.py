import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
import os

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

# Nome do arquivo onde os dados serão salvos
arquivo_dados = 'historico_gastos.csv'

# Carregar os dados do arquivo se ele existir
if os.path.exists(arquivo_dados):
    historico = pd.read_csv(arquivo_dados)
else:
    historico = pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor (¥)'])

# Funções de manipulação de dados
def salvar_dados():
    historico.to_csv(arquivo_dados, index=False)

def atualizar_gasto(idx, nova_data, nova_categoria, nova_descricao, novo_valor):
    historico.at[idx, 'Data'] = nova_data
    historico.at[idx, 'Categoria'] = nova_categoria
    historico.at[idx, 'Descrição'] = nova_descricao
    historico.at[idx, 'Valor (¥)'] = novo_valor
    salvar_dados()

def excluir_gasto(idx):
    global historico
    historico = historico.drop(idx).reset_index(drop=True)
    salvar_dados()

# Exibir o Dashboard
st.title("💰 Controle de Gastos em Ienes")
col1, col2 = st.columns([3, 1])

# Gráfico de despesas por categoria
with col1:
    if not historico.empty:
        fig = px.bar(historico, x='Categoria', y='Valor (¥)', title="Despesas por Categoria", color="Categoria",
                     labels={'Valor (¥)': 'Valor em Ienes (¥)'})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Nenhum gasto registrado para exibir o gráfico.")

# Formulário para adicionar novo gasto
with col2:
    st.subheader("Adicionar Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data", value=date.today())
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde"])
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor (¥)", min_value=0, format="%d")
        submit_button = st.form_submit_button("Adicionar")

    if submit_button:
        novo_gasto = pd.DataFrame({
            'Data': [data],
            'Categoria': [categoria],
            'Descrição': [descricao],
            'Valor (¥)': [valor]
        })
        historico = pd.concat([historico, novo_gasto], ignore_index=True)
        salvar_dados()
        st.success("Gasto adicionado com sucesso!")

# Painel com Dados e Opções de Edição/Exclusão
st.subheader("Histórico de Gastos")
if not historico.empty:
    selecionado = st.selectbox("Selecione o gasto para editar ou excluir", historico.index, format_func=lambda x: f"{historico.loc[x, 'Data']} - {historico.loc[x, 'Categoria']} - ¥{historico.loc[x, 'Valor (¥)']}")

    st.write("### Editar Gasto Selecionado")
    data = st.date_input("Data", value=pd.to_datetime(historico.loc[selecionado, "Data"]))
    categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Lazer", "Educação", "Saúde"], index=["Alimentação", "Transporte", "Lazer", "Educação", "Saúde"].index(historico.loc[selecionado, "Categoria"]))
    descricao = st.text_input("Descrição", value=historico.loc[selecionado, "Descrição"])
    valor = st.number_input("Valor (¥)", min_value=0, value=int(historico.loc[selecionado, "Valor (¥)"]), format="%d")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Atualizar Gasto"):
            atualizar_gasto(selecionado, data, categoria, descricao, valor)
            st.success("Gasto atualizado com sucesso!")

    with col2:
        if st.button("Excluir Gasto"):
            excluir_gasto(selecionado)
            st.success("Gasto excluído com sucesso!")

    st.table(historico)
else:
    st.write("Nenhum gasto registrado ainda.")

# Totalizador em Ienes
gasto_total = historico['Valor (¥)'].sum()
st.write(f"### Total de Gastos: ¥ {gasto_total:,}")
