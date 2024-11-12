import streamlit as st
import pandas as pd
from datetime import date

# Carregar e aplicar o CSS personalizado
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# Carregar ou inicializar histórico de gastos usando session_state
if "historico" not in st.session_state:
    try:
        st.session_state.historico = pd.read_csv("gastos.csv")
    except FileNotFoundError:
        st.session_state.historico = pd.DataFrame(columns=["Data", "Categoria", "Descrição", "Valor (¥)"])

# Função para salvar os dados
def salvar_dados():
    st.session_state.historico.to_csv("gastos.csv", index=False)

st.title("💰 Controle de Gastos")
st.write("Organize e monitore seus gastos de forma prática e simples.")

# Criar duas colunas
col1, col2 = st.columns([2, 1])

# Formulário para adicionar novo gasto
with col2:
    st.subheader("Adicionar Novo Gasto")
    with st.form("add_expense", clear_on_submit=True):
        data = st.date_input("Data", value=date.today(), help="Selecione a data do gasto")
        
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
        st.session_state.historico = pd.concat([st.session_state.historico, novo_gasto], ignore_index=True)
        salvar_dados()
        st.success("Gasto adicionado com sucesso!")

# Exibir histórico de gastos na coluna 1
with col1:
    st.subheader("Histórico de Gastos")
    if not st.session_state.historico.empty:
        st.dataframe(st.session_state.historico)

        # Exibir o total de gastos
        total_gastos = st.session_state.historico["Valor (¥)"].sum()
        st.write(f"**Total de Gastos:** ¥{total_gastos:,.2f}")
    else:
        st.write("Nenhum gasto registrado.")

# Função para editar ou excluir gastos
st.subheader("Editar ou Excluir Gasto")

if len(st.session_state.historico) > 0:
    selected_index = st.selectbox(
        "Selecione o gasto para editar/excluir:",
        st.session_state.historico.index.tolist(),
        format_func=lambda x: f"{st.session_state.historico.loc[x, 'Data']} - {st.session_state.historico.loc[x, 'Categoria']} - {st.session_state.historico.loc[x, 'Descrição']}"
    )

    # Mostrar os campos de edição com os dados do gasto selecionado
    gasto_selecionado = st.session_state.historico.loc[selected_index]
    
    categoria_edit = st.selectbox("Categoria", [
        "Alimentação", "Transporte", "Lazer", "Educação", "Saúde", 
        "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", 
        "Investimentos", "Outros"
    ], index=["Alimentação", "Transporte", "Lazer", "Educação", "Saúde", "Moradia", "Serviços Públicos", "Entretenimento", "Roupas", "Investimentos", "Outros"].index(gasto_selecionado["Categoria"]))

    descricao_edit = st.text_input("Descrição", value=gasto_selecionado["Descrição"])
    valor_edit = st.number_input("Valor (¥)", min_value=0, value=gasto_selecionado["Valor (¥)"], format="%d")

    if st.button("Salvar Alterações"):
        # Atualizar o gasto no DataFrame
        st.session_state.historico.loc[selected_index, "Categoria"] = categoria_edit
        st.session_state.historico.loc[selected_index, "Descrição"] = descricao_edit
        st.session_state.historico.loc[selected_index, "Valor (¥)"] = valor_edit
        salvar_dados()
        st.success("Gasto editado com sucesso!")
    
    if st.button("Excluir Gasto"):
        confirm = st.checkbox("Tem certeza que deseja excluir este gasto?", value=False)
        if confirm:
            st.session_state.historico.drop(selected_index, inplace=True)
            st.session_state.historico.reset_index(drop=True, inplace=True)
            salvar_dados()
            st.success("Gasto excluído com sucesso!")
else:
    st.warning("Não há gastos registrados para editar ou excluir.")
