import sqlite3

def verificar_estrutura():
    conn = sqlite3.connect('database/almoxarifado.db')
    cursor = conn.cursor()

    # Verifica a estrutura da tabela
    cursor.execute("PRAGMA table_info(itens)")
    colunas = cursor.fetchall()

    print("\nEstrutura atual da tabela:")
    for coluna in colunas:
        print(f"{coluna[1]} ({coluna[2]})")

    # Verifica alguns registros
    cursor.execute("SELECT * FROM itens LIMIT 1")
    registro = cursor.fetchone()

    print("\nExemplo de registro:")
    if registro:
        for i, valor in enumerate(registro):
            print(f"Posição {i}: {valor}")

    conn.close()

if __name__ == "__main__":
    verificar_estrutura()
    input("Pressione Enter para sair...")
