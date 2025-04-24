from typing import List, Optional
from src.services.movimentacao_service import MovimentacaoService
from src.services.item_service import ItemService
from src.utils.helpers import input_int, validar_data, converter_data_para_exibir
from datetime import datetime

class MenuMovimentacoes:
    def __init__(self, mov_service: MovimentacaoService, item_service: ItemService):
        self.mov_service = mov_service
        self.item_service = item_service

    def exibir(self):
        while True:
            print("\n=== MENU DE MOVIMENTAÇÕES ===")
            print("1. Registrar Entrada")
            print("2. Registrar Saída")
            print("3. Histórico Completo")
            print("4. Histórico por Item")
            print("5. Voltar")

            opcao = input("\nOpção: ").strip()

            if opcao == "1":
                self.registrar_entrada()
            elif opcao == "2":
                self.registrar_saida()
            elif opcao == "3":
                self.exibir_historico_completo()
            elif opcao == "4":
                self.exibir_historico_item()
            elif opcao == "5":
                break
            else:
                print("Opção inválida!")

    def registrar_entrada(self):
        print("\n📥 REGISTRAR ENTRADA DE ITEM")
        self._listar_itens_simplificado()

        try:
            item_id = input_int("ID do item: ")
            quantidade = input_int("Quantidade: ", min_val=1)
            responsavel = input("Responsável: ").strip()
            motivo = input("Motivo (opcional): ").strip() or None

            sucesso, mensagem = self.mov_service.registrar_movimentacao(
                item_id=item_id,
                tipo='entrada',
                quantidade=quantidade,
                responsavel=responsavel,
                motivo=motivo
            )

            print(f"\n{mensagem}")
            if sucesso:
                item = self.item_service.buscar_por_id(item_id)
                print(f"Novo saldo: {item.quantidade} unidades")

        except ValueError as e:
            print(f"\nErro: {e}")

    def registrar_saida(self):
        print("\n📤 REGISTRAR SAÍDA DE ITEM")
        self._listar_itens_simplificado()

        try:
            item_id = input_int("ID do item: ")
            quantidade = input_int("Quantidade: ", min_val=1)
            responsavel = input("Responsável: ").strip()
            motivo = input("Motivo (opcional): ").strip() or None

            sucesso, mensagem = self.mov_service.registrar_movimentacao(
                item_id=item_id,
                tipo='saída',
                quantidade=quantidade,
                responsavel=responsavel,
                motivo=motivo
            )

            print(f"\n{mensagem}")
            if sucesso:
                item = self.item_service.buscar_por_id(item_id)
                print(f"Novo saldo: {item.quantidade} unidades")

        except ValueError as e:
            print(f"\nErro: {e}")

    def exibir_historico_completo(self):
        print("\n🕰️ HISTÓRICO COMPLETO DE MOVIMENTAÇÕES")

        # Solicita período se desejar filtrar
        data_inicio, data_fim = self._solicitar_periodo()

        movimentacoes = self.mov_service.listar_todas(data_inicio, data_fim)

        if not movimentacoes:
            periodo_msg = self._formatar_periodo_msg(data_inicio, data_fim)
            print(f"Nenhuma movimentação encontrada {periodo_msg}")
            return

        print(f"\n📊 MOVIMENTAÇÕES {self._formatar_periodo_msg(data_inicio, data_fim)}")
        print("-" * 80)
        for mov in movimentacoes:
            print(f"📅 {converter_data_para_exibir(mov.data)} | #{mov.item_id} | {mov.tipo.upper():<6} | Qtd: {mov.quantidade:>4}")
            print(f"👤 {mov.responsavel:<15} | 💬 {mov.motivo or 'Sem motivo informado'}")
            print("-" * 80)

    def exibir_historico_item(self):
        print("\n🔍 HISTÓRICO POR ITEM")
        self._listar_itens_simplificado()

        item_id = input_int("\nID do item: ")
        item = self.item_service.buscar_por_id(item_id)

        if not item:
            print("Item não encontrado!")
            return

        data_inicio, data_fim = self._solicitar_periodo()

        # Agora recebe 3 valores de retorno
        movimentacoes, saldo_inicial, saldo_final = self.mov_service.historico_por_item(
            item_id=item_id,
            data_inicio=data_inicio,
            data_fim=data_fim
        )

        periodo_msg = self._formatar_periodo_msg(data_inicio, data_fim)
        print(f"\n📋 Item: {item.nome} {periodo_msg}")
        print(f"🔢 Código: {item.id} | Tipo: {item.tipo}")
        print(f"📦 Saldo inicial: {saldo_inicial} {item.unidade or 'un'}")
        print(f"🏁 Saldo final: {saldo_final} {item.unidade or 'un'}")
        print("-" * 60)

        # Processa movimentações em ordem cronológica
        saldo_atual = saldo_inicial
        for mov in movimentacoes:
            # Exibe com sinal CORRETO
            sinal = '+' if mov.tipo == 'entrada' else '-'
            print(f"\n📅 {converter_data_para_exibir(mov.data)} | {mov.tipo.upper()} ({sinal}{mov.quantidade})")
            print(f"👤 {mov.responsavel:<15} | 💬 {mov.motivo or 'N/A'}")

            # Atualiza saldo CORRETAMENTE
            if mov.tipo == 'entrada':
                saldo_atual += mov.quantidade
            else:
                saldo_atual -= mov.quantidade

            print(f"🔄 Saldo após movimentação: {saldo_atual} {item.unidade or 'un'}")

        # Resumo com totais
        total_entradas = sum(m.quantidade for m in movimentacoes if m.tipo == 'entrada')
        total_saidas = sum(m.quantidade for m in movimentacoes if m.tipo == 'saída')

        print("\n" + "=" * 60)
        print(f"📊 Resumo Final:")
        print(f"🔢 Saldo inicial: {saldo_inicial} {item.unidade or 'un'}")
        print(f"🟢 Total entradas: +{total_entradas}")
        print(f"🔴 Total saídas: -{total_saidas}")
        print(f"📦 Saldo final: {saldo_final} {item.unidade or 'un'}")
        print("=" * 60)

        if not movimentacoes:
            print(f"Nenhuma movimentação encontrada {periodo_msg}")
            return

        for mov in movimentacoes:
            print(f"\n{converter_data_para_exibir(mov.data)} | {mov.tipo.upper()} ({mov.quantidade:+})")
            print(f"Responsável: {mov.responsavel} | Motivo: {mov.motivo or 'N/A'}")
            print(f"Saldo após: {saldo_inicial} {item.unidade or 'un'}")

            # Atualiza saldo para próxima movimentação
            if mov.tipo == 'entrada':
                saldo_inicial += mov.quantidade
            else:
                saldo_inicial -= mov.quantidade

    def _solicitar_periodo(self) -> tuple:
        """Solicita período ao usuário e retorna datas formatadas"""
        print("\nFiltrar por período? (Deixe em branco para listar tudo)")
        data_inicio = input("Data inicial (DD/MM/AAAA): ").strip()
        data_fim = input("Data final (DD/MM/AAAA): ").strip()

        # Valida as datas se fornecidas
        if data_inicio and not validar_data(data_inicio):
            print("Data inicial inválida! Usando data mais antiga disponível.")
            data_inicio = ""

        if data_fim and not validar_data(data_fim):
            print("Data final inválida! Usando data mais recente disponível.")
            data_fim = ""

        return (data_inicio if data_inicio else None,
                data_fim if data_fim else None)

    def _formatar_periodo_msg(self, data_inicio: Optional[str], data_fim: Optional[str]) -> str:
        """Formata mensagem do período para exibição"""
        if not data_inicio and not data_fim:
            return ""

        msg = "no período: "
        if data_inicio:
            msg += f"de {data_inicio}"
            if data_fim:
                msg += f" a {data_fim}"
        elif data_fim:
            msg += f"até {data_fim}"

        return f"({msg})"

    def _listar_itens_simplificado(self):
        """Lista resumida de itens para seleção"""
        itens = self.item_service.listar_todos()

        if not itens:
            print("Nenhum item cadastrado.")
            return

        print("\n📝 ITENS DISPONÍVEIS:")
        print("-" * 60)
        for item in itens:
            print(f"ID: {item.id:<3} | {item.nome:<20} | Estoque: {item.quantidade:>4} {item.unidade or ''}")
        print("-" * 60)