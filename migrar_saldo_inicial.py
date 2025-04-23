# migrar_saldo_inicial.py
from database.db import criar_conexao

def migrar_saldos():
    conn = criar_conexao()
    if conn:
        try:
            cursor = conn.cursor()
            # Define saldo_inicial = quantidade para itens existentes
            cursor.execute("ALTER TABLE itens ADD COLUMN saldo_inicial INTEGER DEFAULT 0")
            cursor.execute("UPDATE itens SET saldo_inicial = quantidade")
            conn.commit()
            print("✅ Migração de saldos concluída!")
        except Error as e:
            print(f"❌ Erro na migração: {e}")
        finally:
            conn.close()

if __name__ == "__main__":
    migrar_saldos()