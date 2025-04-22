import sqlite3
from sqlite3 import Error
from .migrations import fazer_backup

def criar_conexao():
    """Cria conexão com o banco SQLite."""
    try:
        conexao = sqlite3.connect("database/almoxarifado.db")
        return conexao
    except Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return None

def criar_tabela_itens():
    """Cria a tabela de itens se não existir"""
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

            # Verifica se a tabela existe
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='itens'")
            if not cursor.fetchone():
                print("ℹ️ Tabela 'itens' não encontrada. Criando nova tabela...")
                cursor.execute(sql)
                conexao.commit()
                print("✅ Tabela 'itens' criada com sucesso!")
            else:
                print("ℹ️ Tabela 'itens' já existe.")

        except Error as e:
            print(f"❌ Erro ao criar tabela: {e}")
        finally:
            conexao.close()

    """Versão segura que faz backup antes de alterações"""
    fazer_backup()  # Backup automático

    conn = criar_conexao()
    try:
        cursor = conn.cursor()
        # ... (restante do código original)
    except Exception as e:
        conn.rollback()
        print(f"Erro: {e}")
    finally:
        conn.close()

def inicializar_banco():
    """Garante que o banco está pronto para uso"""
    print("\n🔍 Verificando estrutura do banco de dados...")
    criar_tabela_itens()
    print("✅ Banco de dados verificado.\n")

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