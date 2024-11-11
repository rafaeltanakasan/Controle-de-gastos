import streamlit as st

# Link para o Manifesto
st.markdown("""
<link rel="manifest" href="/manifest.json">
""", unsafe_allow_html=True)

# Script para registrar o Service Worker
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
    console.log('Service Worker registrado com sucesso:', registration);
  }).catch(function(error) {
    console.log('Falha ao registrar o Service Worker:', error);
  });
}
</script>
""", unsafe_allow_html=True)

# Script para registrar o Service Worker
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
    console.log('Service Worker registrado com sucesso:', registration);
  }).catch(function(error) {
    console.log('Falha ao registrar o Service Worker:', error);
  });
}
</script>
""", unsafe_allow_html=True)
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Nome do arquivo CSV para salvar o histórico
HISTORICO_ARQUIVO = 'historico_gastos.csv'

# Função para carregar e salvar histórico de gastos
def carregar_historico():
    try:
        return pd.read_csv(HISTORICO_ARQUIVO)
    except FileNotFoundError:
        return pd.DataFrame(columns=['Data', 'Categoria', 'Descrição', 'Valor'])

def salvar_historico(dados):
    dados.to_csv(HISTORICO_ARQUIVO, index=False)

# Função para converter dados para CSV para download
@st.cache_data
def converter_para_csv(dados):
    return dados.to_csv(index=False).encode('utf-8')

# Carregar histórico de gastos ao iniciar o app
historico = carregar_historico()

# Estilos CSS personalizados para dar um visual mais tecnológico
st.markdown("""
    <style>
        .main {
            font-family: 'Roboto', sans-serif;
            background-color: #1e1e1e;
            color: #f0f0f0;
        }
        .title {
            font-size: 3em;
            font-weight: bold;
            color: #00bcd4;
            text-align: center;
            text-shadow: 2px 2px 8px rgba(0, 188, 212, 0.6);
        }
        .subtitle {
            font-size: 1.4em;
            color: #888;
            text-align: center;
            margin-bottom: 30px;
        }
        .card {
            background-color: #2e2e2e;
            padding: 20px;
            margin: 10px 0;
            border-radius: 10px;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.3);
        }
        .button {
            background-color: #00bcd4;
            color: white;
            font-size: 1.2em;
            border-radius: 5px;
            padding: 10px 20px;
            border: none;
            cursor: pointer;
            box-shadow: 0px 4px 8px rgba(0, 188, 212, 0.3);
        }
        .button:hover {
            background-color: #0097a7;
        }
        .error {
            color: #f44336;
            font-weight: bold;
        }
        .warning {
            color: #ff9800;
            font-weight: bold;
        }
        .success {
            color: #4caf50;
            font-weight: bold;
        }
        .section {
            margin-top: 50px;
        }
        .stDownloadButton {
            background-color: #00bcd4 !important;
            font-size: 1em;
            color: white !important;
        }
        .stDataFrame {
            color: #f0f0f0;
        }
    </style>
""", unsafe_allow_html=True)

# Título e subtítulo com efeito de sombreamento
st.markdown('<div class="title">💰 Controle de Gastos</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Organize seus gastos com facilidade e estilo.</div>', unsafe_allow_html=True)

# Seção para entrada de dados
with st.expander("Adicionar Gasto", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        data = st.date_input("Data", datetime.now())
        categoria = st.selectbox("Categoria", ["Alimentação", "Transporte", "Saúde", "Outros"])
    with col2:
        descricao = st.text_input("Descrição")
        valor = st.number_input("Valor", min_value=0.0, format="%.2f")

    if st.button("Adicionar Gasto", key="adicionar", use_container_width=True):
        if not descricao or valor <= 0:
            st.markdown('<p class="error">Por favor, preencha todos os campos corretamente (Descrição e Valor).</p>', unsafe_allow_html=True)
        else:
            novo_gasto = pd.DataFrame({
                "Data": [data],
                "Categoria": [categoria],
                "Descrição": [descricao],
                "Valor": [valor]
            })
            historico = pd.concat([historico, novo_gasto], ignore_index=True)
            salvar_historico(historico)
            st.markdown('<p class="success">Gasto adicionado com sucesso!</p>', unsafe_allow_html=True)

# Filtro por categoria e data
with st.expander("Filtrar Gastos", expanded=True):
    categorias_unicas = historico['Categoria'].unique()
    categoria_filtro = st.selectbox("Filtrar por Categoria", options=["Todas"] + list(categorias_unicas))
    data_inicial = st.date_input("Data Inicial", historico['Data'].min() if not historico.empty else datetime.now())
    data_final = st.date_input("Data Final", historico['Data'].max() if not historico.empty else datetime.now())

    if categoria_filtro != "Todas":
        historico_filtrado = historico[(historico["Categoria"] == categoria_filtro)]
    else:
        historico_filtrado = historico
    historico_filtrado = historico_filtrado[(pd.to_datetime(historico_filtrado["Data"]) >= pd.to_datetime(data_inicial)) &
                                            (pd.to_datetime(historico_filtrado["Data"]) <= pd.to_datetime(data_final))]
    st.dataframe(historico_filtrado)

# Gráficos
with st.expander("Gráficos de Gastos", expanded=True):
    if not historico.empty:
        # Gráfico de barras com efeito interativo
        fig1 = px.bar(historico.groupby("Categoria")["Valor"].sum().reset_index(), 
                      x="Categoria", y="Valor", title="Gastos por Categoria", color="Categoria", 
                      color_discrete_sequence=["#00bcd4", "#0097a7", "#004d40", "#ff9800"])
        fig1.update_layout(title="Gastos por Categoria", template="plotly_dark")
        st.plotly_chart(fig1)

        # Gráfico de linha com animação
        fig2 = px.line(historico.groupby("Data")["Valor"].sum().reset_index(), 
                       x="Data", y="Valor", title="Gastos Diários", markers=True)
        fig2.update_layout(title="Gastos Diários", template="plotly_dark")
        st.plotly_chart(fig2)
    else:
        st.write("Ainda não há dados suficientes para exibir gráficos.")

# Exportar histórico
csv = converter_para_csv(historico)
with st.expander("Exportar Dados", expanded=True):
    st.download_button(
        label="📥 Baixar Histórico",
        data=csv,
        file_name="historico_gastos.csv",
        mime="text/csv",
        use_container_width=True
    )

# Resumo mensal
with st.expander("Resumo Mensal dos Gastos", expanded=True):
    mes_selecionado = st.selectbox("Escolha o Mês", options=pd.to_datetime(historico["Data"]).dt.strftime('%Y-%m').unique())
    historico_mes = historico[pd.to_datetime(historico["Data"]).dt.strftime('%Y-%m') == mes_selecionado]

    gasto_por_categoria_mes = historico_mes.groupby("Categoria")["Valor"].sum()
    gasto_total_mes = historico_mes["Valor"].sum()

    st.write("Total por Categoria:")
    st.write(gasto_por_categoria_mes)
    st.write("Total do Mês:", f"R$ {gasto_total_mes:.2f}")
import streamlit as st

# Link para o Manifesto
st.markdown("""
<link rel="manifest" href="/manifest.json">
""", unsafe_allow_html=True)

# Link para o Service Worker
st.markdown("""
<script>
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('/service-worker.js').then(function(registration) {
    console.log('Service Worker registrado com sucesso:', registration);
  }).catch(function(error) {
    console.log('Falha ao registrar o Service Worker:', error);
  });
}
</script>
""", unsafe_allow_html=True)
