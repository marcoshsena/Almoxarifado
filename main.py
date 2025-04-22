from models.item import Item, ItemDAO
from database.db import inicializar_banco
from utils.helpers import (
    validar_data, converter_data_para_banco,
    converter_data_para_exibir, formatar_moeda,
    input_int, input_float
)

def exibir_menu():
    print("\n=== 🏭 MENU ALMOXARIFADO ===")
    print("1. Cadastrar novo item")
    print("2. Listar todos os itens")
    print("3. Buscar item por nome")
    print("4. Atualizar item")
    print("5. Remover item")
    print("6. Itens próximos da validade")
    print("7. Sair")

def cadastrar_item():
    print("\n📝 CADASTRAR ITEM")
    nome = input("Nome: ").strip()
    while not nome:
        print("⚠️ O nome é obrigatório!")
        nome = input("Nome: ").strip()

    marca = input("Marca (opcional): ").strip() or None
    quantidade = input_int("Quantidade: ")
    unidade = input("Unidade (opcional, ex: 'un', 'kg'): ").strip() or None
    preco = input_float("Preço unitário: R$ ")
    tipo = input("Tipo: ").strip()
    while not tipo:
        print("⚠️ O tipo é obrigatório!")
        tipo = input("Tipo: ").strip()

    descricao = input("Descrição (opcional): ").strip() or None

    while True:
        data_validade = input("Data de validade (DD/MM/AAAA): ").strip()
        if validar_data(data_validade):
            data_validade = converter_data_para_banco(data_validade)
            break
        print("❌ Formato inválido! Use DD/MM/AAAA.")

    novo_item = Item(
        id=None,
        nome=nome,
        marca=marca,
        quantidade=quantidade,
        unidade=unidade,
        preco=preco,
        tipo=tipo,
        descricao=descricao,
        data_validade=data_validade
    )

    sucesso, mensagem = ItemDAO.criar(novo_item)
    print(mensagem)

def listar_itens(itens=None):
    if itens is None:
        itens = ItemDAO.listar_todos()

    print("\n📦 LISTA DE ITENS")
    if not itens:
        print("Nenhum item cadastrado.")
        return

    for item in itens:
        print("-" * 60)
        print(f"ID: {item[0]}")
        print(f"Nome: {item[1]}")
        print(f"Marca: {item[2] or 'N/A'}")
        print(f"Quantidade: {item[3]} {item[4] or ''}")
        print(f"Preço unitário: {formatar_moeda(item[5])}")
        print(f"Tipo: {item[6]}")
        print(f"Descrição: {item[7] or 'N/A'}")
        print(f"Data de validade: {converter_data_para_exibir(item[8])}")
    print("-" * 60)
    print(f"Total de itens: {len(itens)}")

def buscar_item_por_nome():
    print("\n🔍 BUSCAR ITEM POR NOME")
    nome = input("Digite o nome ou parte dele: ").strip()
    itens = ItemDAO.buscar_por_nome(nome)
    listar_itens(itens)

def atualizar_item():
    print("\n🔄 ATUALIZAR ITEM")
    item_id = input_int("ID do item a atualizar: ")

    item = ItemDAO.buscar_por_id(item_id)
    if not item:
        print("❌ Item não encontrado!")
        return

    print("\nItem atual:")
    listar_itens([item])

    print("\nDigite os novos dados (deixe em branco para manter o atual):")

    nome = input(f"Nome [{item[1]}]: ").strip() or item[1]
    marca = input(f"Marca [{item[2] or 'N/A'}]: ").strip() or item[2]
    quantidade = input(f"Quantidade [{item[3]}]: ").strip()
    quantidade = int(quantidade) if quantidade else item[3]
    unidade = input(f"Unidade [{item[4] or 'N/A'}]: ").strip() or item[4]
    preco = input(f"Preço [{formatar_moeda(item[5])}]: ").strip()
    preco = float(preco) if preco else item[5]
    tipo = input(f"Tipo [{item[6]}]: ").strip() or item[6]
    descricao = input(f"Descrição [{item[7] or 'N/A'}]: ").strip() or item[7]

    while True:
        data_input = input(f"Data de validade [{converter_data_para_exibir(item[8])}]: ").strip()
        if not data_input:
            data_validade = item[8]
            break
        if validar_data(data_input):
            data_validade = converter_data_para_banco(data_input)
            break
        print("❌ Formato inválido! Use DD/MM/AAAA.")

    item_atualizado = Item(
        id=item_id,
        nome=nome,
        marca=marca if marca != "N/A" else None,
        quantidade=quantidade,
        unidade=unidade if unidade != "N/A" else None,
        preco=preco,
        tipo=tipo,
        descricao=descricao if descricao != "N/A" else None,
        data_validade=data_validade
    )

    sucesso, mensagem = ItemDAO.atualizar(item_id, item_atualizado)
    print(mensagem)

def remover_item():
    print("\n❌ REMOVER ITEM")
    item_id = input_int("ID do item a remover: ")

    item = ItemDAO.buscar_por_id(item_id)
    if not item:
        print("❌ Item não encontrado!")
        return

    print("\nItem selecionado:")
    listar_itens([item])

    confirmacao = input("\nTem certeza? (s/n): ").strip().lower()
    if confirmacao == 's':
        sucesso, mensagem = ItemDAO.remover(item_id)
        print(mensagem)
    else:
        print("Operação cancelada.")

def listar_prox_validade():
    print("\n📅 ITENS PRÓXIMOS DA VALIDADE")
    dias = input("Dias para expirar (padrão: 30): ").strip()
    dias = int(dias) if dias.isdigit() else 30

    itens = ItemDAO.itens_prox_validade(dias)
    if itens:
        print(f"\n⚠️ Itens que expiram em {dias} dias:")
        listar_itens(itens)
    else:
        print(f"Nenhum item expira nos próximos {dias} dias.")

def main():
    inicializar_banco()

    while True:
        exibir_menu()
        opcao = input("\nOpção: ").strip()

        if opcao == "1":
            cadastrar_item()
        elif opcao == "2":
            listar_itens()
        elif opcao == "3":
            buscar_item_por_nome()
        elif opcao == "4":
            atualizar_item()
        elif opcao == "5":
            remover_item()
        elif opcao == "6":
            listar_prox_validade()
        elif opcao == "7":
            print("\n👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!")

        input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main()