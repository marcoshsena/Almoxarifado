from typing import List, Tuple, Optional
from datetime import datetime
from src.models.movimentacao import Movimentacao
from src.repositories.movimentacao_repository import MovimentacaoRepository
from src.repositories.item_repository import ItemRepository
from src.utils.helpers import converter_data_para_banco

class MovimentacaoService:

    @staticmethod
    def registrar_movimentacao(
            item_id: int,
            tipo: str,
            quantidade: int,
            responsavel: str,
            motivo: str = None
    ) -> Tuple[bool, str]:
        """Registra uma nova movimentação"""
        mov = Movimentacao(
            item_id=item_id,
            tipo=tipo,
            quantidade=quantidade,
            data=datetime.now().isoformat(sep=' ', timespec='seconds'),
            responsavel=responsavel,
            motivo=motivo
        )

        try:
            # Validações
            if tipo not in ('entrada', 'saída'):
                return False, "Tipo inválido (use 'entrada' ou 'saída')"

            if quantidade <= 0:
                return False, "Quantidade deve ser positiva"

            if not responsavel.strip():
                return False, "Responsável é obrigatório"

            # Verifica estoque para saída
            if tipo == 'saída':
                item = ItemRepository.buscar_por_id(item_id)
                if not item:
                    return False, "Item não encontrado"
                if item.quantidade < quantidade:
                    return False, f"Estoque insuficiente (disponível: {item.quantidade})"

            return MovimentacaoRepository.registrar(mov)

        except Exception as e:
            return False, str(e)

    @staticmethod
    def listar_todas(data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Movimentacao]:
        """Lista todas as movimentações com filtro por período"""
        # Converte datas para formato do banco
        data_inicio_db = converter_data_para_banco(data_inicio) if data_inicio else None
        data_fim_db = converter_data_para_banco(data_fim) if data_fim else None

        return MovimentacaoRepository.listar_todas(data_inicio_db, data_fim_db)

    @staticmethod
    def historico_por_item(item_id: int, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> Tuple[List[Movimentacao], int, int]:
        """Retorna histórico, saldo inicial e saldo final"""
        # Converte datas para formato do banco
        data_inicio_db = converter_data_para_banco(data_inicio) if data_inicio else None
        data_fim_db = converter_data_para_banco(data_fim) if data_fim else None

        movimentacoes = MovimentacaoRepository.listar_por_item(item_id, data_inicio_db, data_fim_db)
        item = ItemRepository.buscar_por_id(item_id)

        if not item:
            return [], 0, 0

        # Calcula saldo inicial (antes de todas as movimentações)
        saldo_inicial = item.quantidade
        for mov in reversed(movimentacoes):
            if mov.tipo == 'entrada':
                saldo_inicial -= mov.quantidade  # Subtrai entradas
            else:
                saldo_inicial += mov.quantidade  # Soma saídas

        saldo_final = item.quantidade
        return movimentacoes, saldo_inicial, saldo_final