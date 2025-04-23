from dataclasses import dataclass
from datetime import datetime
from database.db import criar_conexao
from sqlite3 import Error

@dataclass
class Movimentacao:
    id: int
    item_id: int
    tipo: str  # 'entrada' ou 'saída'
    quantidade: int
    data: str  # Armazenaremos como string no formato ISO
    responsavel: str = None
    motivo: str = None

    @staticmethod
    def data_atual():
        """Retorna a data/hora atual no formato ISO"""
        return datetime.now().isoformat(sep=' ', timespec='seconds')

class MovimentacaoDAO:
    @staticmethod
    def registrar(movimentacao):
        """Registra uma nova movimentação e atualiza o estoque"""
        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()

                # 1. Registrar a movimentação
                sql_mov = """
                INSERT INTO movimentacoes 
                (item_id, tipo, quantidade, data, responsavel, motivo)
                VALUES (?, ?, ?, ?, ?, ?)
                """
                cursor.execute(sql_mov, (
                    movimentacao.item_id,
                    movimentacao.tipo,
                    movimentacao.quantidade,
                    movimentacao.data,
                    movimentacao.responsavel,
                    movimentacao.motivo
                ))

                # 2. Atualizar o estoque
                operacao = '+' if movimentacao.tipo == 'entrada' else '-'
                sql_estoque = f"""
                UPDATE itens 
                SET quantidade = quantidade {operacao} ? 
                WHERE id = ?
                """
                cursor.execute(sql_estoque, (
                    movimentacao.quantidade,
                    movimentacao.item_id
                ))

                conn.commit()
                return True, "Movimentação registrada com sucesso!"

            except Error as e:
                conn.rollback()
                return False, f"Erro ao registrar movimentação: {e}"
            finally:
                conn.close()
        return False, "Erro ao conectar ao banco"

    @staticmethod
    def listar_por_item_com_filtros(item_id, data_inicio=None, data_fim=None):
        """Lista movimentações com filtros de período"""
        sql = """
        SELECT * FROM movimentacoes 
        WHERE item_id = ? 
        """
        params = [item_id]

        # Adiciona filtros de data se fornecidos
        if data_inicio:
            sql += " AND data >= ?"
            params.append(datetime.strptime(data_inicio, "%d/%m/%Y").strftime("%Y-%m-%d 00:00:00"))
        if data_fim:
            sql += " AND data <= ?"
            params.append(datetime.strptime(data_fim, "%d/%m/%Y").strftime("%Y-%m-%d 23:59:59"))

        sql += " ORDER BY data DESC"

        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, params)
                return cursor.fetchall()
            except Error as e:
                print(f"Erro ao filtrar movimentações: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def primeiro_saldo(item_id):
        """Retorna o saldo inicial do item antes de qualquer movimentação"""
        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("""
                SELECT quantidade FROM itens WHERE id = ?
                """, (item_id,))
                return cursor.fetchone()[0]
            except:
                return 0
            finally:
                conn.close()
        return 0

    @staticmethod
    def listar_por_item(item_id):
        """Lista todas movimentações de um item"""
        sql = """
        SELECT * FROM movimentacoes 
        WHERE item_id = ?
        ORDER BY data DESC
        """
        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql, (item_id,))
                return cursor.fetchall()
            except Error as e:
                print(f"Erro ao listar movimentações: {e}")
            finally:
                conn.close()
        return []

    @staticmethod
    def listar_todas():
        """Lista todas as movimentações ordenadas por data (mais recente primeiro)"""
        sql = """
        SELECT m.*, i.nome as item_nome 
        FROM movimentacoes m
        JOIN itens i ON m.item_id = i.id
        ORDER BY m.data DESC
        """
        conn = criar_conexao()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(sql)
                return cursor.fetchall()
            except Error as e:
                print(f"❌ Erro ao listar movimentações: {e}")
            finally:
                conn.close()
        return []

