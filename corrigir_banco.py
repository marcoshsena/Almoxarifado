import sqlite3
from database.db import criar_conexao

def corrigir_precos():
    conn = criar_conexao()
    try:
        cursor = conn.cursor()

        # Verifica os tipos atuais
        cursor.execute("SELECT id, nome, preco, typeof(preco) FROM itens")
        print("\nAntes da correção:")
        for row in cursor.fetchall():
            print(row)

        # Executa a correção
        cursor.execute("UPDATE itens SET preco = CAST(preco AS REAL)")
        conn.commit()

        # Verifica após correção
        cursor.execute("SELECT id, nome, preco, typeof(preco) FROM itens")
        print("\nDepois da correção:")
        for row in cursor.fetchall():
            print(row)

        print("\n✅ Preços convertidos para numéricos com sucesso!")
    except Exception as e:
        print(f"❌ Erro: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    corrigir_precos()
    input("Pressione Enter para sair...")