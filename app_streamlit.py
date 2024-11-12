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

# Função para excluir ou editar gastos
if len(historico) > 0:
    st.subheader("Editar ou Excluir Gasto")

    selected_index = st.number_input("Índice do gasto para editar/excluir:", min_value=0, max_value=len(historico)-1, step=1)

    # Excluir gasto
    if st.button("Excluir Gasto"):
        historico.drop(selected_index, inplace=True)
        historico.reset_index(drop=True, inplace=True)
        salvar_dados()
        st.success("Gasto excluído com sucesso!")

    # Atualizar gasto
    if st.button("Editar Gasto"):
        gasto_editado = historico.iloc[selected_index]
        
        categoria_editada = st.selectbox("Categoria", [
            "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
            "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
            "Investimentos", "Outros"], index=["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
                                                "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
                                                "Investimentos", "Outros"].index(gasto_editado["Categoria"]))
        
        descricao_editada = st.text_input("Descrição", value=gasto_editado["Descrição"])
        valor_editado = st.number_input("Valor (¥)", min_value=0, value=gasto_editado["Valor (¥)"], format="%d")
        
        if st.button("Salvar Alteração"):
            historico.loc[selected_index, "Categoria"] = categoria_editada
            historico.loc[selected_index, "Descrição"] = descricao_editada
            historico.loc[selected_index, "Valor (¥)"] = valor_editado
            salvar_dados()
            st.success("Gasto editado com sucesso!")
            st.experimental_rerun()  # Recarregar a página para refletir as alterações imediatamente
else:
    st.warning("Não há gastos registrados para editar ou excluir.")
