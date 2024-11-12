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

# Estilo de Stranger Things
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap');

        /* Aplicando a fonte no app */
        body {
            font-family: 'Press Start 2P', sans-serif;
            background-color: #1c1c1c;
            color: #ffffff;
        }

        /* Estilo para os títulos */
        h1, h2, h3 {
            color: #ff4c4c;
        }

        /* Fundo para os botões */
        button {
            background-color: #ff4c4c;
            border: none;
            padding: 10px;
            color: #fff;
            font-family: 'Press Start 2P', sans-serif;
            border-radius: 5px;
            cursor: pointer;
        }

        button:hover {
            background-color: #d43535;
        }

        /* Personalizando as caixas de texto */
        .stTextInput input, .stNumberInput input, .stSelectbox select {
            background-color: #2a2a2a;
            color: #ffffff;
            border: 2px solid #ff4c4c;
            border-radius: 5px;
            padding: 10px;
        }

        .stTextInput input:focus, .stNumberInput input:focus, .stSelectbox select:focus {
            border-color: #d43535;
            box-shadow: 0px 0px 10px 2px rgba(255, 76, 76, 0.8);
        }

        /* Estilo das tabelas */
        .stDataFrame table {
            color: #ffffff;
            border: 1px solid #ff4c4c;
        }

        .stDataFrame th {
            background-color: #ff4c4c;
            color: white;
        }

        /* Efeito de sombra no conteúdo */
        .stForm, .stColumns {
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
        }
    </style>
""", unsafe_allow_html=True)

# Título e descrição do aplicativo
st.title("💰 Controle de Gastos - Stranger Things Style")
st.write("Organize e monitore seus gastos de forma prática e misteriosa.")

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

# Excluir gasto
if st.button("Excluir Gasto"):
    if len(historico) > 0:
        historico.drop(selected_index, inplace=True)
        historico.reset_index(drop=True, inplace=True)
        salvar_dados()
        st.success("Gasto excluído com sucesso!")

# Atualizar gasto (exemplo simples de edição)
if st.button("Editar Gasto"):
    if len(historico) > 0:
        # Exibir o gasto selecionado para edição
        gasto_editado = historico.iloc[selected_index]
        
        # Formulário para editar gasto
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
