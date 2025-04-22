from dataclasses import dataclass
from database.db import criar_conexao
from sqlite3 import Error
from utils.helpers import converter_data_para_banco, converter_data_para_exibir, formatar_moeda

@dataclass
class Item:
    id: int
    nome: str
    quantidade: int
    preco: float
    tipo: str
    data_validade: str  # Armazenado como 'AAAA-MM-DD' no banco
    marca: str = None
    unidade: str = None
    descricao: str = None

class ItemDAO:
    @staticmethod
    def criar(item):
        sql = """
        INSERT INTO itens (
            nome, marca, quantidade, unidade, preco, tipo, descricao, data_validade
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (
                    item.nome, item.marca, item.quantidade, item.unidade,
                    item.preco, item.tipo, item.descricao, item.data_validade
                ))
                conexao.commit()
                return True, "✅ Item cadastrado com sucesso!"
            except Error as e:
                return False, f"❌ Erro ao cadastrar: {e}"
            finally:
                conexao.close()
        return False, "❌ Erro ao conectar ao banco."

    @staticmethod
    def listar_todos():
        sql = "SELECT * FROM itens ORDER BY nome"
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql)
                # Converter os tipos dos dados manualmente
                itens = []
                for item in cursor.fetchall():
                    itens.append((
                        item[0],  # id
                        item[1],  # nome
                        item[2],  # marca
                        item[3],  # quantidade
                        item[4],  # unidade
                        float(item[5]),  # preco convertido para float
                        item[6],  # tipo
                        item[7],  # descricao
                        item[8]   # data_validade
                    ))
                return itens
            except Error as e:
                print(f"❌ Erro ao listar: {e}")
            finally:
                conexao.close()
        return []

    @staticmethod
    def buscar_por_id(item_id):
        sql = "SELECT * FROM itens WHERE id = ?"
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (item_id,))
                return cursor.fetchone()
            except Error as e:
                print(f"❌ Erro ao buscar item: {e}")
            finally:
                conexao.close()
        return None

    @staticmethod
    def atualizar(item_id, novo_item):
        sql = """
        UPDATE itens SET
            nome=?, marca=?, quantidade=?, unidade=?, preco=?, tipo=?, descricao=?, data_validade=?
        WHERE id=?
        """
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (
                    novo_item.nome, novo_item.marca, novo_item.quantidade, novo_item.unidade,
                    novo_item.preco, novo_item.tipo, novo_item.descricao, novo_item.data_validade,
                    item_id
                ))
                conexao.commit()
                return True, "✅ Item atualizado com sucesso!"
            except Error as e:
                return False, f"❌ Erro ao atualizar: {e}"
            finally:
                conexao.close()
        return False, "❌ Erro ao conectar ao banco."

    @staticmethod
    def remover(item_id):
        sql = "DELETE FROM itens WHERE id=?"
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (item_id,))
                conexao.commit()
                return True, "✅ Item removido com sucesso!"
            except Error as e:
                return False, f"❌ Erro ao remover: {e}"
            finally:
                conexao.close()
        return False, "❌ Erro ao conectar ao banco."

    @staticmethod
    def buscar_por_nome(nome):
        sql = "SELECT * FROM itens WHERE nome LIKE ? ORDER BY nome"
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (f"%{nome}%",))
                return cursor.fetchall()
            except Error as e:
                print(f"❌ Erro ao buscar: {e}")
            finally:
                conexao.close()
        return []

    @staticmethod
    def itens_prox_validade(dias=30):
        sql = "SELECT * FROM itens WHERE data_validade BETWEEN DATE('now') AND DATE('now', ?) ORDER BY data_validade"
        conexao = criar_conexao()
        if conexao:
            try:
                cursor = conexao.cursor()
                cursor.execute(sql, (f"+{dias} days",))
                return cursor.fetchall()
            except Error as e:
                print(f"❌ Erro ao buscar: {e}")
            finally:
                conexao.close()
        return []