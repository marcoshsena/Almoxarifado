from datetime import datetime
import os

def input_int(mensagem: str, min_val: int = None, max_val: int = None) -> int:
    """Garante que o usuário digite um inteiro válido"""
    while True:
        try:
            valor = int(input(mensagem))
            if min_val is not None and valor < min_val:
                print(f"Valor mínimo permitido: {min_val}")
                continue
            if max_val is not None and valor > max_val:
                print(f"Valor máximo permitido: {max_val}")
                continue
            return valor
        except ValueError:
            print("Por favor, digite um número inteiro válido.")

def input_float(mensagem: str, min_val: float = None) -> float:
    """Garante que o usuário digite um float válido"""
    while True:
        try:
            valor = float(input(mensagem))
            if min_val is not None and valor < min_val:
                print(f"Valor mínimo permitido: {min_val}")
                continue
            return valor
        except ValueError:
            print("Por favor, digite um número válido.")

def formatar_data(data_str: str, formato_origem: str, formato_destino: str) -> str:
    """Converte entre formatos de data"""
    try:
        data = datetime.strptime(data_str, formato_origem)
        return data.strftime(formato_destino)
    except ValueError:
        return data_str  # Retorna original se falhar

def limpar_tela():
    """Limpa a tela do console de forma cross-platform"""
    os.system('cls' if os.name == 'nt' else 'clear')

def validar_data(data_str: str, formato: str = "%d/%m/%Y") -> bool:
    """Valida se uma string está no formato de data correto"""
    try:
        datetime.strptime(data_str, formato)
        return True
    except ValueError:
        return False

def converter_data_para_banco(data_str: str, formato_origem: str = "%d/%m/%Y") -> str:
    """Converte data do formato DD/MM/AAAA para AAAA-MM-DD"""
    try:
        return datetime.strptime(data_str, formato_origem).strftime("%Y-%m-%d")
    except ValueError:
        return data_str  # Retorna original se falhar

def converter_data_para_exibir(data_str: str, formato_banco: str = "%Y-%m-%d %H:%M:%S") -> str:
    """Converte data do banco para formato legível"""
    try:
        return datetime.strptime(data_str, formato_banco).strftime("%d/%m/%Y %H:%M")
    except ValueError:
        return data_str  # Retorna original se falhar