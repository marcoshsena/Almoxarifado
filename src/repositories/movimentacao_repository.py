from src.core.database import db_manager
from src.models.movimentacao import Movimentacao
from typing import List, Tuple, Optional
import logging

class MovimentacaoRepository:
    @staticmethod
    def registrar(movimentacao: Movimentacao) -> Tuple[bool, str]:
        """Registra uma movimentação e atualiza o estoque"""
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()

                # Atualiza estoque
                if movimentacao.tipo == 'entrada':
                    cursor.execute(
                        "UPDATE itens SET quantidade = quantidade + ? WHERE id = ?",
                        (movimentacao.quantidade, movimentacao.item_id))
                else:
                    cursor.execute(
                        "UPDATE itens SET quantidade = quantidade - ? WHERE id = ?",
                        (movimentacao.quantidade, movimentacao.item_id))

                # Insere movimentação
                cursor.execute(
                    """INSERT INTO movimentacoes 
                    (item_id, tipo, quantidade, data, responsavel, motivo)
                    VALUES (?, ?, ?, ?, ?, ?)""",
                    (movimentacao.item_id, movimentacao.tipo,
                     movimentacao.quantidade, movimentacao.data,
                     movimentacao.responsavel, movimentacao.motivo))

                movimentacao.id = cursor.lastrowid
                conn.commit()
                return True, "Movimentação registrada com sucesso"

        except Exception as e:
            logging.error(f"Erro ao registrar movimentação: {e}")
            return False, f"Erro ao registrar movimentação: {e}"

    @staticmethod
    def listar_todas(data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Movimentacao]:
        """Lista todas as movimentações com filtro por período"""
        sql = """
        SELECT id, item_id, tipo, quantidade, data, responsavel, motivo
        FROM movimentacoes
        """
        params = []

        # Adiciona filtro de data se fornecido
        if data_inicio or data_fim:
            sql += " WHERE "
            conditions = []
            if data_inicio:
                conditions.append("data >= ?")
                params.append(data_inicio)
            if data_fim:
                conditions.append("data <= ?")
                params.append(data_fim)
            sql += " AND ".join(conditions)

        sql += " ORDER BY data DESC"

        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return [
                    Movimentacao(
                        id=row[0],
                        item_id=row[1],
                        tipo=row[2],
                        quantidade=row[3],
                        data=row[4],
                        responsavel=row[5],
                        motivo=row[6]
                    ) for row in cursor.fetchall()
                ]
        except Exception as e:
            logging.error(f"Erro ao listar movimentações: {e}")
            return []

    @staticmethod
    def listar_por_item(item_id: int, data_inicio: Optional[str] = None, data_fim: Optional[str] = None) -> List[Movimentacao]:
        """Lista movimentações de um item com filtro por período"""
        sql = """
        SELECT id, item_id, tipo, quantidade, data, responsavel, motivo
        FROM movimentacoes
        WHERE item_id = ?
        """
        params = [item_id]

        # Adiciona filtro de data se fornecido
        if data_inicio or data_fim:
            if data_inicio:
                sql += " AND data >= ?"
                params.append(data_inicio)
            if data_fim:
                sql += " AND data <= ?"
                params.append(data_fim)

        sql += " ORDER BY data DESC"

        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return [
                    Movimentacao(
                        id=row[0],
                        item_id=row[1],
                        tipo=row[2],
                        quantidade=row[3],
                        data=row[4],
                        responsavel=row[5],
                        motivo=row[6]
                    ) for row in cursor.fetchall()
                ]
        except Exception as e:
            logging.error(f"Erro ao listar movimentações: {e}")
            return []

    # ... (implementar outros métodos: listar_todas, filtrar_por_data, etc.)