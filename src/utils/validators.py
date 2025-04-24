from datetime import datetime

class Validador:
    @staticmethod
    def validar_data(data_str: str, formato: str = '%d/%m/%Y') -> bool:
        try:
            datetime.strptime(data_str, formato)
            return True
        except ValueError:
            return False

    @staticmethod
    def validar_quantidade(quantidade: int) -> bool:
        return quantidade > 0

    @staticmethod
    def validar_preco(preco: float) -> bool:
        return preco >= 0