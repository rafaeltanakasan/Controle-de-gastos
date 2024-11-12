import streamlit as st
import pandas as pd
from datetime import date

# Inicializar histórico de gastos
try:
    historico = pd.read_csv("gastos.csv")
except FileNotFoundError:
    historico = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor (¥)"])

# Função para salvar os dados
def salvar_dados():
    historico.to_csv("gastos.csv", index=False)

st.title("💰 Controle de Gastos")
st.write("Organize e monitore seus gastos de forma prática.")

# Criar duas colunas
col1, col2 = st.columns(2)

# Formulário para adicionar novo gasto
with col2:
    st.subheader("Adicionar Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data", value=date.today())
        
        # Lista de categorias ampliada
        categoria = st.selectbox("Categoria", [
            "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
            "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
            "Investimentos", "Outros"
        ])
        
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

# Exibir histórico de gastos na coluna 1
with col1:
    st.subheader("Histórico de Gastos")
    st.dataframe(historico)

# Função para excluir gastos
st.subheader("Editar ou Excluir Gasto")
selected_index = st.number_input("Índice do gasto para editar/excluir:", min_value=0, max_value=len(historico)-1, step=1)

if st.button("Excluir Gasto"):
    if len(historico) > 0:
        historico.drop(selected_index, inplace=True)
        historico.reset_index(drop=True, inplace=True)
        salvar_dados()
        st.success("Gasto excluído com sucesso!")

# Atualizar gasto (exemplo simples de edição)
if st.button("Editar Gasto"):
    if len(historico) > 0:
        historico.loc[selected_index, "Categoria"] = st.selectbox("Categoria", [
            "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
            "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
            "Investimentos", "Outros"
        ])
        historico.loc[selected_index, "Descrição"] = st.text_input("Descrição")
        historico.loc[selected_index, "Valor (¥)"] = st.number_input("Valor (¥)", min_value=0, format="%d")
        salvar_dados()
        st.success("Gasto editado com sucesso!")
