from typing import List, Tuple, Optional
from src.core.database import db_manager
from src.models.item import Item
import logging

class ItemRepository:

    # ... (outros métodos existentes)
    @staticmethod
    def salvar(item: Item) -> Tuple[bool, str]:
        """Salva ou atualiza um item no banco de dados"""
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()

                if item.id is None:  # Novo item
                    sql = """
                    INSERT INTO itens (
                        nome, marca, quantidade, saldo_inicial, unidade, 
                        preco, tipo, descricao, data_validade
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """
                    params = (
                        item.nome, item.marca, item.quantidade, item.quantidade,
                        item.unidade, item.preco, item.tipo, item.descricao,
                        item.data_validade
                    )
                    cursor.execute(sql, params)
                    item.id = cursor.lastrowid
                else:  # Atualização
                    sql = """
                    UPDATE itens SET
                        nome=?, marca=?, quantidade=?, unidade=?,
                        preco=?, tipo=?, descricao=?, data_validade=?
                    WHERE id=?
                    """
                    params = (
                        item.nome, item.marca, item.quantidade,
                        item.unidade, item.preco, item.tipo,
                        item.descricao, item.data_validade, item.id
                    )
                    cursor.execute(sql, params)

                conn.commit()
                return True, "Item salvo com sucesso"

        except Exception as e:
            logging.error(f"Erro ao salvar item: {e}")
            return False, f"Erro ao salvar item: {e}"

    @staticmethod
    def buscar_por_id(item_id: int) -> Optional[Item]:
        """Busca um item pelo ID"""
        sql = "SELECT * FROM itens WHERE id = ?"
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (item_id,))
                row = cursor.fetchone()
                if row:
                    return Item(
                        id=row[0], nome=row[1], marca=row[2],
                        quantidade=row[3], saldo_inicial=row[4],
                        unidade=row[5], preco=row[6], tipo=row[7],
                        descricao=row[8], data_validade=row[9]
                    )
                return None
        except Exception as e:
            logging.error(f"Erro ao buscar item: {e}")
            return None

    @staticmethod
    def buscar_por_nome(nome: str) -> List[Item]:
        """Busca itens onde o nome contém a string fornecida (case-insensitive)"""
        sql = "SELECT * FROM itens WHERE LOWER(nome) LIKE LOWER(?) ORDER BY nome"
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (f"%{nome}%",))
                return [ItemRepository._row_to_item(row) for row in cursor.fetchall()]
        except Exception as e:
            logging.error(f"Erro ao buscar itens: {e}")
            return []

    @staticmethod
    def remover(item_id: int) -> Tuple[bool, str]:
        """Remove um item pelo ID"""
        sql = "DELETE FROM itens WHERE id = ?"
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql, (item_id,))
                conn.commit()
                return (True, "Item removido com sucesso") if cursor.rowcount > 0 else (False, "Item não encontrado")
        except Exception as e:
            logging.error(f"Erro ao remover item: {e}")
            return False, f"Erro ao remover item: {e}"

    @staticmethod
    def _row_to_item(row) -> Item:
        """Converte uma linha do banco para objeto Item"""
        return Item(
            id=row[0],
            nome=row[1],
            marca=row[2],
            quantidade=row[3],
            saldo_inicial=row[4],
            unidade=row[5],
            preco=row[6],
            tipo=row[7],
            descricao=row[8],
            data_validade=row[9]
        )

    @staticmethod
    def listar_todos() -> List[Item]:
        """Lista todos os itens cadastrados ordenados por nome"""
        sql = "SELECT * FROM itens ORDER BY nome"
        try:
            with db_manager.criar_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(sql)
                return [
                    Item(
                        id=row[0],
                        nome=row[1],
                        marca=row[2],
                        quantidade=row[3],
                        saldo_inicial=row[4],
                        unidade=row[5],
                        preco=float(row[6]),  # Garante conversão para float
                        tipo=row[7],
                        descricao=row[8],
                        data_validade=row[9]
                    ) for row in cursor.fetchall()
                ]
        except Exception as e:
            logging.error(f"Erro ao listar itens: {e}")
            return []