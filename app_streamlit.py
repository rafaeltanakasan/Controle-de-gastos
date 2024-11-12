# Inserir o conteúdo CSS diretamente no código Python
st.markdown("""
    <style>
        /* Fonte com estilo retrô */
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
