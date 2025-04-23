import csv
from datetime import datetime
from sqlite3 import Error
from models.item import Item, ItemDAO
from models.movimentacao import Movimentacao, MovimentacaoDAO
from database.db import inicializar_banco
from database.db import criar_conexao
from utils.helpers import (
    validar_data, converter_data_para_banco,
    converter_data_para_exibir, formatar_moeda,
    input_int, input_float
)
inicializar_banco()

def exibir_menu():
    print("\n=== 🏭 MENU ALMOXARIFADO ===")
    print("1. Cadastrar novo item")
    print("2. Listar todos os itens")
    print("3. Buscar item por nome")
    print("4. Atualizar item")
    print("5. Remover item")
    print("6. Itens próximos da validade")
    print("7. Controle de Movimentação")
    print("8. Sair")

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

    data_validade = None
    while True:
        data_input = input("Data de validade (DD/MM/AAAA - deixe em branco se não aplicável): ").strip()
        if not data_input:
            break
        if validar_data(data_input):
            data_validade = converter_data_para_banco(data_input)
            break
        print("❌ Formato inválido! Use DD/MM/AAAA ou deixe em branco.")

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
        print(f"Data de validade: {converter_data_para_exibir(item[8]) if item[8] else 'N/A'}")
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
        data_input = input(f"Data de validade [{converter_data_para_exibir(item[8]) if item[8] else 'N/A'}]: ").strip()
        if not data_input:
            data_validade = item[8] if item[8] else None
            break
        if validar_data(data_input):
            data_validade = converter_data_para_banco(data_input)
            break
        print("❌ Formato inválido! Use DD/MM/AAAA ou deixe em branco.")

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
    # Garante que todas tabelas existam
    from database.db import criar_tabelas
    criar_tabelas()  # Esta função deve criar todas as tabelas necessárias
    criar_tabela_movimentacoes()  # Garante extra
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
            menu_movimentacoes()
        elif opcao == "8":
            print("\n👋 Saindo do sistema...")
            break
        else:
            print("❌ Opção inválida!")

        input("\nPressione Enter para continuar...")

def criar_tabela_movimentacoes():
    """Cria a tabela de movimentações se não existir"""
    sql = """
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_id INTEGER NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('entrada', 'saída')),
        quantidade INTEGER NOT NULL,
        data TEXT NOT NULL,
        responsavel TEXT,
        motivo TEXT,
        FOREIGN KEY (item_id) REFERENCES itens (id)
    );
    """
    conn = criar_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            conn.commit()
            print("✅ Tabela 'movimentacoes' criada com sucesso!")
        except Error as e:
            print(f"❌ Erro ao criar tabela: {e}")
        finally:
            conn.close()

def menu_movimentacoes():
    while True:
        print("\n📦 CONTROLE DE MOVIMENTAÇÕES")
        print("1. Registrar entrada")
        print("2. Registrar saída")
        print("3. Histórico de movimentações")
        print("4. Histórico por item")
        print("5. Voltar ao menu principal")

        opcao = input("Opção: ").strip()

        if opcao == "1":
            registrar_entrada()
        elif opcao == "2":
            registrar_saida()
        elif opcao == "3":
            listar_movimentacoes()
        elif opcao == "4":
            historico_por_item()
        elif opcao == "5":
            break
        else:
            print("Opção inválida!")
        input("\nPressione Enter para continuar...")

def registrar_entrada():
    print("\n📥 REGISTRAR ENTRADA DE ITEM")
    listar_itens()

    try:
        item_id = int(input("\nID do item: "))
        quantidade = int(input("Quantidade: "))
        responsavel = input("Responsável: ").strip()
        motivo = input("Motivo (opcional): ").strip() or None

        mov = Movimentacao(
            id=None,
            item_id=item_id,
            tipo='entrada',
            quantidade=quantidade,
            data=Movimentacao.data_atual(),
            responsavel=responsavel,
            motivo=motivo
        )

        sucesso, msg = MovimentacaoDAO.registrar(mov)
        print(msg)

    except ValueError:
        print("Erro: ID e quantidade devem ser números inteiros")

def registrar_saida():
    print("\n📤 REGISTRAR SAÍDA DE ITEM")
    listar_itens()

    try:
        item_id = int(input("\nID do item: "))
        quantidade = int(input("Quantidade retirada: "))
        responsavel = input("Responsável pela saída: ").strip()
        motivo = input("Motivo (opcional): ").strip() or None

        # Verifica se o item existe
        item = ItemDAO.buscar_por_id(item_id)
        if not item:
            print("❌ Item não encontrado!")
            return

        # Verifica estoque suficiente
        saldo_atual = item[3]  # quantidade está na posição 3
        if saldo_atual < quantidade:
            print(f"❌ Saldo insuficiente! Disponível: {saldo_atual} unidades")
            return

        mov = Movimentacao(
            id=None,
            item_id=item_id,
            tipo='saída',
            quantidade=quantidade,
            data=Movimentacao.data_atual(),
            responsavel=responsavel,
            motivo=motivo
        )

        sucesso, msg = MovimentacaoDAO.registrar(mov)
        print(f"\n{msg}")
        if sucesso:
            print(f"Novo saldo: {ItemDAO.buscar_por_id(item_id)[3]} unidades")

    except ValueError:
        print("❌ Erro: ID e quantidade devem ser números inteiros")

def listar_movimentacoes():
    print("\n🕰️ HISTÓRICO COMPLETO DE MOVIMENTAÇÕES")

    # Obtém todas as movimentações do banco de dados
    movimentacoes = MovimentacaoDAO.listar_todas()

    if not movimentacoes:
        print("Nenhuma movimentação registrada.")
        return

    # Exibe cada movimentação formatada
    for mov in movimentacoes:
        print("\n" + "-" * 60)
        print(f"📆 Data: {mov[4]}")
        print(f"🆔 ID Item: {mov[1]} | 🔄 Tipo: {mov[2].upper()}")
        print(f"🔢 Quantidade: {mov[3]} | 👤 Responsável: {mov[5]}")
        print(f"📝 Motivo: {mov[6] or 'N/A'}")

    print("\n" + "-" * 60)
    print(f"📊 Total de movimentações: {len(movimentacoes)}")

def historico_por_item():
    print("\n🔍 HISTÓRICO POR ITEM")
    listar_itens()

    try:
        item_id = int(input("\nID do item para consulta: "))
        item = ItemDAO.buscar_por_id(item_id)
        if not item:
            print("❌ Item não encontrado!")
            return

        movimentacoes = MovimentacaoDAO.listar_por_item(item_id)

        print(f"\nHistórico para: {item[1]} (Saldo atual: {item[3]} {item[4] or 'unidades'})")
        print("-" * 60)

        if not movimentacoes:
            print("Nenhuma movimentação registrada para este item.")
            return

        # Começa com o saldo inicial (antes de qualquer movimentação)
        saldo_acumulado = item[3]  # Saldo atual

        # Subtrai todas as movimentações para encontrar o saldo inicial real
        for mov in movimentacoes:
            if mov[2] == 'entrada':
                saldo_acumulado -= mov[3]
            else:
                saldo_acumulado += mov[3]

        print(f"Saldo inicial: {saldo_acumulado} {item[4] or 'unidades'}")
        print("-" * 60)

        # Agora processa as movimentações em ordem cronológica
        for mov in reversed(movimentacoes):  # Inverte para ordem cronológica
            data_formatada = datetime.strptime(mov[4], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
            tipo = "📥 ENTRADA" if mov[2] == 'entrada' else "📤 SAÍDA"
            quantidade = mov[3]

            # Atualiza o saldo corretamente
            if mov[2] == 'entrada':
                saldo_acumulado += quantidade
            else:
                saldo_acumulado -= quantidade

            print(f"\n{data_formatada} | {tipo} ({quantidade:+})")
            print(f"👤 {mov[5]} | 📝 {mov[6] or 'N/A'}")
            print(f"🔄 Saldo após movimentação: {saldo_acumulado} {item[4] or 'unidades'}")

        print("\n" + "-" * 60)
        print(f"📊 Total de movimentações: {len(movimentacoes)}")

    except ValueError:
        print("❌ ID deve ser um número inteiro")

def exportar_para_csv(item, movimentacoes):
    """Exporta o histórico para um arquivo CSV"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nome_arquivo = f"historico_{item[1]}_{timestamp}.csv".replace(" ", "_")

    try:
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as arquivo:
            writer = csv.writer(arquivo, delimiter=';')

            # Cabeçalho
            writer.writerow([
                "Data", "Tipo", "Quantidade", "Responsável",
                "Motivo", "Saldo Parcial", "Unidade"
            ])

            # Obtém o saldo inicial diretamente do item
            saldo_acumulado = item[3]  # Quantidade atual do item

            # Subtrai todas as movimentações para reconstituir o histórico
            for mov in reversed(movimentacoes):
                if mov[2] == 'entrada':
                    saldo_acumulado -= mov[3]
                else:
                    saldo_acumulado += mov[3]

            # Agora processa as movimentações em ordem cronológica
            for mov in movimentacoes:
                data_formatada = datetime.strptime(mov[4], "%Y-%m-%d %H:%M:%S").strftime("%d/%m/%Y %H:%M")
                tipo = mov[2].upper()
                quantidade = mov[3]

                # Atualiza saldo acumulado
                if mov[2] == 'entrada':
                    saldo_acumulado += quantidade
                else:
                    saldo_acumulado -= quantidade

                writer.writerow([
                    data_formatada,
                    tipo,
                    quantidade,
                    mov[5],
                    mov[6] or '',
                    saldo_acumulado,
                    item[4] or 'unidades'
                ])

        print(f"✅ Arquivo exportado com sucesso: {nome_arquivo}")
        return True
    except Exception as e:
        print(f"❌ Falha ao exportar CSV: {e}")
        return False

if __name__ == "__main__":
    main()