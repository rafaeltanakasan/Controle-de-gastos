import streamlit as st
import pandas as pd
from datetime import date

# Definir estilo com Streamlit
st.set_page_config(page_title="Controle de Gastos", page_icon="💰", layout="wide")

# Estilo personalizado para a página
st.markdown("""
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 16px;
        padding: 10px;
        border-radius: 5px;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .stDataFrame {
        background-color: #f9f9f9;
        border-radius: 10px;
    }
    .stSelectbox, .stNumberInput, .stTextInput {
        font-size: 14px;
        padding: 10px;
    }
    .stSubtitle {
        font-size: 22px;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializar histórico de gastos
try:
    historico = pd.read_csv("gastos.csv")
except FileNotFoundError:
    historico = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor (¥)"])

# Função para salvar os dados
def salvar_dados():
    historico.to_csv("gastos.csv", index=False)

st.title("💰 Controle de Gastos")
st.write("Organize e monitore seus gastos de forma prática e simples.")

# Criar duas colunas
col1, col2 = st.columns([2, 1])

# Formulário para adicionar novo gasto
with col2:
    st.subheader("Adicionar Novo Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data", value=date.today(), help="Selecione a data do gasto")
        
        # Categoria com pesquisa rápida
        categoria = st.selectbox("Categoria", [
            "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
            "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
            "Investimentos", "Outros"
        ], help="Escolha a categoria do gasto")
        
        descricao = st.text_input("Descrição", placeholder="Descrição breve do gasto", help="Digite uma descrição do gasto")
        valor = st.number_input("Valor (¥)", min_value=0, format="%d", help="Informe o valor do gasto")
        submit_button = st.form_submit_button("Adicionar Gasto")

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
    if not historico.empty:
        st.dataframe(historico)

        # Exibir o total de gastos
        total_gastos = historico["Valor (¥)"].sum()
        st.write(f"**Total de Gastos:** ¥{total_gastos:,.2f}")
    else:
        st.write("Nenhum gasto registrado.")

# Filtros e busca de gastos
st.subheader("Buscar ou Editar Gasto")

# Adicionar filtro de categoria
categoria_filtro = st.selectbox("Filtrar por Categoria", ["Todas"] + historico["Categoria"].unique().tolist())

# Filtrar os dados com base na categoria selecionada
if categoria_filtro != "Todas":
    historico_filtrado = historico[historico["Categoria"] == categoria_filtro]
else:
    historico_filtrado = historico

# Exibir os gastos filtrados
if not historico_filtrado.empty:
    st.dataframe(historico_filtrado)
else:
    st.write("Nenhum gasto encontrado para a categoria selecionada.")

# Função para editar ou excluir gastos
st.subheader("Editar ou Excluir Gasto")
if len(historico) > 0:
    selected_index = st.selectbox("Selecione o gasto para editar/excluir:", historico.index.tolist(), format_func=lambda x: f"{historico.loc[x, 'Data']} - {historico.loc[x, 'Categoria']}")

    if st.button("Excluir Gasto"):
        confirm = st.checkbox("Tem certeza que deseja excluir este gasto?", value=False)
        if confirm:
            historico.drop(selected_index, inplace=True)
            historico.reset_index(drop=True, inplace=True)
            salvar_dados()
            st.success("Gasto excluído com sucesso!")

    # Atualizar gasto (exemplo simples de edição)
    if st.button("Editar Gasto"):
        categoria_edit = st.selectbox("Categoria", [
            "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
            "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
            "Investimentos", "Outros"
        ])
        descricao_edit = st.text_input("Descrição", value=historico.loc[selected_index, "Descrição"])
        valor_edit = st.number_input("Valor (¥)", min_value=0, value=historico.loc[selected_index, "Valor (¥)"], format="%d")
        
        if st.button("Salvar Alterações"):
            historico.loc[selected_index, "Categoria"] = categoria_edit
            historico.loc[selected_index, "Descrição"] = descricao_edit
            historico.loc[selected_index, "Valor (¥)"] = valor_edit
            salvar_dados()
            st.success("Gasto editado com sucesso!")
else:
    st.warning("Não há gastos registrados para editar ou excluir.")
