from src.services.item_service import ItemService
from src.models.item import Item
from src.utils.helpers import input_int, input_float
from datetime import datetime
from typing import Optional

class MenuItens:
    def __init__(self, item_service: ItemService):
        self.service = item_service

    def exibir(self):
        while True:
            print("\n=== MENU DE ITENS ===")
            print("1. Cadastrar novo item")
            print("2. Listar todos os itens")
            print("3. Buscar item por nome")
            print("4. Editar item")
            print("5. Excluir item")
            print("6. Voltar ao menu principal")

            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.cadastrar_item()
            elif opcao == "2":
                self.listar_itens()
            elif opcao == "3":
                self.buscar_item()
            elif opcao == "4":
                self.editar_item()
            elif opcao == "5":
                self.excluir_item()
            elif opcao == "6":
                break
            else:
                print("Opção inválida! Tente novamente.")

    def cadastrar_item(self):
        print("\n📝 CADASTRAR NOVO ITEM")

        nome = self._obter_nome()
        marca = input("Marca (opcional): ").strip() or None
        quantidade = input_int("Quantidade inicial: ", min_val=0)
        unidade = input("Unidade (ex: un, kg, lt): ").strip() or None
        preco = input_float("Preço unitário: R$ ", min_val=0)
        tipo = input("Tipo/categoria: ").strip()
        descricao = input("Descrição (opcional): ").strip() or None
        data_validade = self._obter_data_validade()

        novo_item = Item(
            nome=nome,
            marca=marca,
            quantidade=quantidade,
            unidade=unidade,
            preco=preco,
            tipo=tipo,
            descricao=descricao,
            data_validade=data_validade
        )

        sucesso, mensagem = self.service.cadastrar(novo_item)
        print(f"\n{mensagem}")

    def listar_itens(self, itens: Optional[list] = None):
        itens = itens or self.service.listar_todos()

        print("\n📦 LISTA DE ITENS")
        if not itens:
            print("Nenhum item cadastrado.")
            return

        print("-" * 60)
        for item in itens:
            print(f"ID: {item.id} | Nome: {item.nome}")
            print(f"Tipo: {item.tipo} | Quantidade: {item.quantidade} {item.unidade or ''}")
            print(f"Preço: R$ {item.preco:.2f} | Validade: {self._formatar_data(item.data_validade)}")
            print("-" * 60)
        print(f"Total de itens: {len(itens)}")

    def buscar_item(self):
        print("\n🔍 BUSCAR ITEM")
        termo = input("Digite o nome ou parte do nome: ").strip()
        itens = self.service.buscar_por_nome(termo)
        self.listar_itens(itens)

    def editar_item(self):
        print("\n✏️ EDITAR ITEM")
        self.listar_itens()

        item_id = input_int("\nID do item a editar: ")
        item = self.service.buscar_por_id(item_id)

        if not item:
            print("Item não encontrado!")
            return

        print("\nDeixe em branco para manter o valor atual:")
        nome = self._obter_nome(item.nome)
        marca = input(f"Marca [{item.marca or 'N/A'}]: ").strip() or item.marca
        quantidade = input_int(f"Quantidade [{item.quantidade}]: ", min_val=0) or item.quantidade
        unidade = input(f"Unidade [{item.unidade or 'N/A'}]: ").strip() or item.unidade
        preco = input_float(f"Preço [R$ {item.preco:.2f}]: ", min_val=0) or item.preco
        tipo = input(f"Tipo [{item.tipo}]: ").strip() or item.tipo
        descricao = input(f"Descrição [{item.descricao or 'N/A'}]: ").strip() or item.descricao
        data_validade = self._obter_data_validade(item.data_validade)

        item_atualizado = Item(
            id=item.id,
            nome=nome,
            marca=marca,
            quantidade=quantidade,
            unidade=unidade,
            preco=preco,
            tipo=tipo,
            descricao=descricao,
            data_validade=data_validade
        )

        sucesso, mensagem = self.service.atualizar(item_atualizado)
        print(f"\n{mensagem}")

    def excluir_item(self):
        print("\n❌ EXCLUIR ITEM")
        self.listar_itens()

        item_id = input_int("\nID do item a excluir: ")
        confirmacao = input("Tem certeza? (s/n): ").strip().lower()

        if confirmacao == 's':
            sucesso, mensagem = self.service.remover(item_id)
            print(f"\n{mensagem}")
        else:
            print("Operação cancelada.")

    # Métodos auxiliares
    def _obter_nome(self, valor_atual: str = "") -> str:
        while True:
            nome = input(f"Nome [{valor_atual}]: " if valor_atual else "Nome: ").strip() or valor_atual
            if nome:
                return nome
            print("O nome é obrigatório!")

    def _obter_data_validade(self, valor_atual: str = None) -> Optional[str]:
        while True:
            entrada = input(
                f"Data de validade (DD/MM/AAAA) [{self._formatar_data(valor_atual) or 'N/A'}]: "
            ).strip()

            if not entrada and valor_atual:
                return valor_atual
            if not entrada:
                return None

            try:
                data = datetime.strptime(entrada, "%d/%m/%Y")
                return data.strftime("%Y-%m-%d")
            except ValueError:
                print("Formato inválido! Use DD/MM/AAAA ou deixe em branco.")

    def _formatar_data(self, data_str: Optional[str]) -> str:
        if not data_str:
            return "N/A"
        try:
            return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            return data_str