from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Item:
    id: Optional[int] = None
    nome: str = ""
    marca: Optional[str] = None
    quantidade: int = 0
    saldo_inicial: int = 0
    unidade: Optional[str] = None
    preco: float = 0.0
    tipo: str = ""
    descricao: Optional[str] = None
    data_validade: Optional[str] = None

    def validar(self):
        """Valida todos os campos do item"""
        if not self.nome or len(self.nome) > 100:
            raise ValueError("Nome deve ter entre 1 e 100 caracteres")
        if self.quantidade < 0:
            raise ValueError("Quantidade não pode ser negativa")
        if self.preco < 0:
            raise ValueError("Preço não pode ser negativo")
        if self.data_validade:
            try:
                datetime.strptime(self.data_validade, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Data deve estar no formato AAAA-MM-DD")