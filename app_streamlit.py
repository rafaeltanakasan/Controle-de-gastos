import datetime

# Dicionário para armazenar os gastos
gastos = []

# Função para adicionar um gasto
def adicionar_gasto():
    data = input("Digite a data (dd/mm/aaaa): ")
    categoria = input("Digite a categoria (ex: Alimentação, Transporte): ")
    descricao = input("Digite uma descrição do gasto: ")
    valor = float(input("Digite o valor (em JPY): "))
    tipo = input("Digite o tipo (Fixo/Variável): ")
    
    gasto = {
        "data": data,
        "categoria": categoria,
        "descricao": descricao,
        "valor": valor,
        "tipo": tipo
    }
    gastos.append(gasto)
    print("Gasto adicionado com sucesso!")

# Função para listar todos os gastos
def listar_gastos():
    if not gastos:
        print("Nenhum gasto registrado.")
    else:
        print("Lista de gastos:")
        for gasto in gastos:
            print(f"Data: {gasto['data']}, Categoria: {gasto['categoria']}, Descrição: {gasto['descricao']}, Valor: {gasto['valor']} JPY, Tipo: {gasto['tipo']}")

# Função para calcular o total por categoria
def calcular_total_categoria():
    categoria_totais = {}
    for gasto in gastos:
        categoria = gasto["categoria"]
        valor = gasto["valor"]
        categoria_totais[categoria] = categoria_totais.get(categoria, 0) + valor
    
    print("Total por categoria:")
    for categoria, total in categoria_totais.items():
        print(f"{categoria}: {total} JPY")

# Função principal do programa
def main():
    while True:
        print("\nControle de Gastos")
        print("1. Adicionar Gasto")
        print("2. Listar Gastos")
        print("3. Calcular Total por Categoria")
        print("4. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            adicionar_gasto()
        elif opcao == "2":
            listar_gastos()
        elif opcao == "3":
            calcular_total_categoria()
        elif opcao == "4":
            print("Saindo do programa...")
            break
        else:
            print("Opção inválida! Tente novamente.")

# Executa o programa
main()
