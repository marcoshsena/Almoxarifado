import sqlite3
from datetime import datetime
import os
from pathlib import Path

def fazer_backup():
    """Cria um backup automático do banco antes de alterações"""
    backup_dir = Path("database/backups")
    backup_dir.mkdir(exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"almoxarifado_{timestamp}.db"

    try:
        with sqlite3.connect('database/almoxarifado.db') as conn:
            with sqlite3.connect(backup_path) as backup:
                conn.backup(backup)
        print(f"✅ Backup criado: {backup_path}")
        return True
    except Exception as e:
        print(f"❌ Falha no backup: {e}")
        return False

def migrar_tabela_itens():
    """Migra a tabela itens de forma segura"""
    with sqlite3.connect('database/almoxarifado.db') as conn:
        cursor = conn.cursor()

        try:
            # Passo 1: Verificar estrutura atual
            cursor.execute("PRAGMA table_info(itens)")
            colunas = {col[1]: col[2] for col in cursor.fetchall()}

            # Passo 2: Criar tabela temporária com nova estrutura
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens_nova (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                marca TEXT,
                quantidade INTEGER NOT NULL,
                unidade TEXT,
                preco REAL NOT NULL,
                tipo TEXT NOT NULL,
                descricao TEXT,
                data_validade TEXT
            )
            """)

            # Passo 3: Mapear colunas para migração segura
            campos_origem = []
            campos_destino = []

            for col in ['id', 'nome', 'marca', 'quantidade', 'unidade',
                        'preco', 'tipo', 'descricao', 'data_validade']:
                if col in colunas:
                    campos_origem.append(col)
                    campos_destino.append(col)

            # Passo 4: Migrar dados
            campos_select = ", ".join(campos_origem)
            campos_insert = ", ".join(campos_destino)

            cursor.execute(f"""
            INSERT INTO itens_nova ({campos_insert})
            SELECT {campos_select} FROM itens
            """)

            # Passo 5: Trocar as tabelas
            cursor.execute("DROP TABLE itens")
            cursor.execute("ALTER TABLE itens_nova RENAME TO itens")

            conn.commit()
            print("✅ Migração concluída com sucesso!")
            return True

        except Exception as e:
            conn.rollback()
            print(f"❌ Erro na migração: {e}")
            return False

def verificar_estrutura():
    """Verifica a estrutura atual da tabela"""
    with sqlite3.connect('database/almoxarifado.db') as conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(itens)")
        print("\nEstrutura atual:")
        for col in cursor.fetchall():
            print(f"{col[1]:<12} {col[2]:<10} {'NULL' if col[3] else 'NOT NULL'}")

if __name__ == "__main__":
    print("\n=== MIGRAÇÃO SEGURA ===")
    print("1. Fazer backup do banco")
    print("2. Verificar estrutura atual")
    print("3. Executar migração segura")

    opcao = input("\nOpção: ").strip()

    if opcao == "1":
        fazer_backup()
    elif opcao == "2":
        verificar_estrutura()
    elif opcao == "3":
        if fazer_backup():  # Sempre faz backup antes
            migrar_tabela_itens()
    else:
        print("Opção inválida")

    input("\nPressione Enter para sair...")