import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Lista para armazenar os gastos
if 'gastos' not in st.session_state:
    st.session_state.gastos = []

# Título do app
st.title("Controle de Gastos")

# Entrada de dados com campo de data melhorado
data = st.date_input("Data", pd.to_datetime("today"))
categoria = st.text_input("Categoria (ex: Alimentação, Transporte)")
descricao = st.text_input("Descrição")
valor = st.number_input("Valor (JPY)", min_value=0.0, step=100.0)
tipo = st.selectbox("Tipo", ["Fixo", "Variável"])

# Botão para adicionar gasto
if st.button("Adicionar Gasto"):
    if categoria and descricao and valor > 0:
        gasto = {
            "data": data.strftime('%d/%m/%Y'),
            "categoria": categoria,
            "descricao": descricao,
            "valor": valor,
            "tipo": tipo
        }
        st.session_state.gastos.append(gasto)  # Armazena o gasto na lista de gastos
        st.success("Gasto adicionado com sucesso!")
    else:
        st.error("Por favor, preencha todos os campos corretamente.")

# Exibir lista de gastos
st.subheader("Lista de Gastos")
if st.session_state.gastos:
    gastos_df = pd.DataFrame(st.session_state.gastos)
    st.write(gastos_df)
else:
    st.write("Nenhum gasto registrado.")

# Calcular total de todos os gastos
if st.button("Calcular Total de Todos os Gastos"):
    if st.session_state.gastos:
        total = sum(gasto['valor'] for gasto in st.session_state.gastos)
        st.subheader("Total de Todos os Gastos")
        st.write(f"Total: {total} JPY")
    else:
        st.write("Nenhum gasto registrado para calcular o total.")

# Calcular total por categoria
if st.button("Calcular Total por Categoria"):
    if st.session_state.gastos:
        categoria_totais = {}
        for gasto in st.session_state.gastos:
            categoria = gasto["categoria"]
            valor = gasto["valor"]
            categoria_totais[categoria] = categoria_totais.get(categoria, 0) + valor

        st.subheader("Total por Categoria")
        for categoria, total in categoria_totais.items():
            st.write(f"{categoria}: {total} JPY")
    else:
        st.write("Nenhum gasto registrado para calcular o total.")

# Exibir Gráfico de Total por Categoria
if st.session_state.gastos:
    categoria_totais = {}
    for gasto in st.session_state.gastos:
        categoria = gasto["categoria"]
        valor = gasto["valor"]
        categoria_totais[categoria] = categoria_totais.get(categoria, 0) + valor

    st.subheader("Gráfico de Gastos por Categoria")
    categorias = list(categoria_totais.keys())
    totais = list(categoria_totais.values())
    
    # Gerando o gráfico com Matplotlib
    fig, ax = plt.subplots()
    ax.bar(categorias, totais, color='skyblue')
    ax.set_xlabel('Categoria')
    ax.set_ylabel('Total (JPY)')
    ax.set_title('Gastos por Categoria')

    # Exibindo o gráfico no Streamlit
    st.pyplot(fig)
