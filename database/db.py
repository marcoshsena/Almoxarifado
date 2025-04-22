import sqlite3
from sqlite3 import Error

def criar_conexao():
    """Cria conexão com o banco SQLite."""
    try:
        conexao = sqlite3.connect("database/almoxarifado.db")
        return conexao
    except Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def criar_tabela_itens():
    """Cria a tabela de itens com a estrutura correta"""
    sql = """
    CREATE TABLE IF NOT EXISTS itens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        marca TEXT,
        quantidade INTEGER NOT NULL,
        unidade TEXT,
        preco REAL NOT NULL,
        tipo TEXT NOT NULL,
        descricao TEXT,
        data_validade TEXT
    );
    """
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()

            # Verifica se a tabela já existe com estrutura diferente
            cursor.execute("DROP TABLE IF EXISTS itens_backup")
            cursor.execute("CREATE TABLE itens_backup AS SELECT * FROM itens")

            # Cria nova tabela com estrutura correta
            cursor.execute("DROP TABLE IF EXISTS itens")
            cursor.execute(sql)

            # Migra os dados mantendo a ordem correta
            cursor.execute("""
                INSERT INTO itens (id, nome, marca, quantidade, unidade, preco, tipo, descricao, data_validade)
                SELECT id, nome, marca, quantidade, unidade, preco, tipo, descricao, data_validade
                FROM itens_backup
            """)

            conexao.commit()
            print("✅ Estrutura da tabela corrigida com sucesso!")
        except Error as e:
            print(f"❌ Erro ao corrigir estrutura: {e}")
            conexao.rollback()
        finally:
            conexao.close()

def inicializar_banco():
    """Garante que o banco e a tabela existam."""
    criar_tabela_itens()

def corrigir_tipos_precos():
    """Corrige valores de preço armazenados como texto"""
    conexao = criar_conexao()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("UPDATE itens SET preco = CAST(preco AS REAL)")
            conexao.commit()
            print("✅ Preços convertidos para numéricos com sucesso!")
        except Error as e:
            print(f"❌ Erro ao converter preços: {e}")
        finally:
            conexao.close()