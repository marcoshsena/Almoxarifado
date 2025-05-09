from src.services import ItemService, MovimentacaoService
from src.cli.menu_itens import MenuItens
from src.cli.menu_movimentacoes import MenuMovimentacoes
from src.utils.helpers import limpar_tela, input_int, validar_data, converter_data_para_banco, \
    converter_data_para_exibir
from src.core.auth import Autenticador
from datetime import datetime

class MenuPrincipal:
    def __init__(self):
        self.item_service = ItemService()
        self.mov_service = MovimentacaoService()
        self.menu_itens = MenuItens(self.item_service)
        self.menu_mov = MenuMovimentacoes(self.mov_service, self.item_service)

    def exibir(self):
        """Exibe o menu principal e gerencia o fluxo do sistema"""
        while True:
            limpar_tela()
            print("====================================")
            print("=== SISTEMA DE ALMOXARIFADO v1.0 ===")
            print("====================================")
            print("\nMENU PRINCIPAL")
            print("1. Gerenciar Itens")
            print("2. Movimentações de Estoque")
            print("3. Relatórios")
            print("4. Sair")

            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.menu_itens.exibir()
            elif opcao == "2":
                self.menu_mov.exibir()
            elif opcao == "3":
                self.exibir_relatorios()
            elif opcao == "4":
                print("\nSaindo do sistema...")
                break
            else:
                print("\nOpção inválida! Tente novamente.")
                input("Pressione Enter para continuar...")

    def exibir_relatorios(self):
        """Submenu de relatórios"""
        while True:
            limpar_tela()
            print("\n=== RELATÓRIOS ===")
            print("1. Itens próximos da validade")
            print("2. Itens com estoque baixo")
            print("3. Movimentações por período")
            print("4. Voltar")

            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.relatorio_prox_validade()
            elif opcao == "2":
                self.relatorio_estoque_baixo()
            elif opcao == "3":
                self.relatorio_movimentacoes_periodo()
            elif opcao == "4":
                break
            else:
                print("Opção inválida!")
                input("Pressione Enter para continuar...")

    def relatorio_prox_validade(self):
        """Relatório de itens próximos da validade"""
        dias = input_int("\nInforme os dias para expiração (padrão 30): ", 30)
        itens = self.item_service.itens_prox_validade(dias)

        print(f"\n⏳ ITENS QUE EXPIREM EM {dias} DIAS:")
        if not itens:
            print("Nenhum item encontrado.")
        else:
            for item in itens:
                dias_restantes = (datetime.strptime(item.data_validade, "%Y-%m-%d") - datetime.now()).days
                print(f"- {item.nome} (Vence em {dias_restantes} dias | Estoque: {item.quantidade})")

        input("\nPressione Enter para voltar...")

    def relatorio_estoque_baixo(self):
        """Relatório de itens com estoque abaixo do mínimo"""
        minimo = input_int("\nInforme o estoque mínimo (padrão 5): ", 5)
        itens = [item for item in self.item_service.listar_todos() if item.quantidade < minimo]

        print(f"\n⚠️ ITENS COM ESTOQUE ABAIXO DE {minimo}:")
        if not itens:
            print("Nenhum item encontrado.")
        else:
            for item in itens:
                print(f"- {item.nome} (Estoque: {item.quantidade})")

        input("\nPressione Enter para voltar...")

    def relatorio_movimentacoes_periodo(self):
        """Relatório completo de movimentações por período"""
        print("\n📅 RELATÓRIO POR PERÍODO")

        while True:
            data_inicio = input("Data inicial (DD/MM/AAAA): ").strip()
            data_fim = input("Data final (DD/MM/AAAA): ").strip()

            # Validação das datas
            if not validar_data(data_inicio) or not validar_data(data_fim):
                print("Datas inválidas! Use o formato DD/MM/AAAA")
                continue

            # Conversão para formato do banco
            data_inicio_db = converter_data_para_banco(data_inicio)
            data_fim_db = converter_data_para_banco(data_fim)
            break

        # Obtém as movimentações
        movimentacoes = self.mov_service.listar_todas(data_inicio_db, data_fim_db)

        print(f"\n📊 MOVIMENTAÇÕES DE {data_inicio} A {data_fim}")
        print("=" * 80)

        if not movimentacoes:
            print("Nenhuma movimentação encontrada no período")
            input("\nPressione Enter para voltar...")
            return

        # Agrupa por item para relatório mais organizado
        itens = {}
        for mov in movimentacoes:
            if mov.item_id not in itens:
                item = self.item_service.buscar_por_id(mov.item_id)
                itens[mov.item_id] = {
                    'nome': item.nome if item else "Item não encontrado",
                    'movimentacoes': []
                }
            itens[mov.item_id]['movimentacoes'].append(mov)

        # Exibe o relatório
        for item_id, dados in itens.items():
            print(f"\n📦 ITEM: {dados['nome']} (ID: {item_id})")
            print("-" * 60)

            total_entradas = 0
            total_saidas = 0

            for mov in dados['movimentacoes']:
                sinal = "+" if mov.tipo == 'entrada' else "-"
                print(f"{converter_data_para_exibir(mov.data)} | {mov.tipo.upper()} ({sinal}{mov.quantidade})")
                print(f"Responsável: {mov.responsavel} | Motivo: {mov.motivo or 'N/A'}")
                print("-" * 60)

                if mov.tipo == 'entrada':
                    total_entradas += mov.quantidade
                else:
                    total_saidas += mov.quantidade

            print(f"TOTAL ENTRADAS: +{total_entradas}")
            print(f"TOTAL SAÍDAS: -{total_saidas}")
            print(f"SALDO DO PERÍODO: {total_entradas - total_saidas}")
            print("=" * 60)

        input("\nPressione Enter para voltar...")

    @classmethod
    def iniciar_sistema(cls):
        """Método principal para iniciar o sistema"""
        if not Autenticador.login():
            print("Acesso negado. Encerrando...")
            return

        sistema = cls()
        sistema.exibir()