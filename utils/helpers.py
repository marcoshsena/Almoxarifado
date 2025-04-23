from datetime import datetime

def validar_data(data_str):
    """Valida datas no formato DD/MM/AAAA."""
    try:
        datetime.strptime(data_str, "%d/%m/%Y")
        return True
    except ValueError:
        return False

def converter_data_para_banco(data_str):
    """Converte DD/MM/AAAA para AAAA-MM-DD (SQLite)."""
    return datetime.strptime(data_str, "%d/%m/%Y").strftime("%Y-%m-%d")

def converter_data_para_exibir(data_str):
    """Converte AAAA-MM-DD (banco) para DD/MM/AAAA."""
    if data_str:
        return datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
    return "N/A"

def formatar_moeda(valor):
    """Formata valores monetários para o padrão R$ 1.234,56"""
    try:
        return f"R$ {float(valor):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except (ValueError, TypeError):
        return "R$ 0,00"

def input_int(mensagem):
    """Garante que o usuário digite um número inteiro."""
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("⚠️ Por favor, digite um número inteiro válido.")

def input_float(mensagem):
    """Garante que o usuário digite um número decimal."""
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("⚠️ Por favor, digite um número válido (ex: 10.50).")