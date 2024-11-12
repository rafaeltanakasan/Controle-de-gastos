# Função para excluir gastos
st.subheader("Editar ou Excluir Gasto")

# Verificar se o histórico tem itens antes de permitir a edição ou exclusão
if len(historico) > 0:
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
