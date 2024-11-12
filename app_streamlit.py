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
