from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Movimentacao:
    id: Optional[int] = None
    item_id: int = 0
    tipo: str = ""  # 'entrada' ou 'saída'
    quantidade: int = 0
    data: str = ""
    responsavel: str = ""
    motivo: Optional[str] = None

    def validar(self):
        """Valida os dados da movimentação"""
        if self.tipo not in ('entrada', 'saída'):
            raise ValueError("Tipo deve ser 'entrada' ou 'saída'")
        if self.quantidade <= 0:
            raise ValueError("Quantidade deve ser positiva")
        if not self.responsavel:
            raise ValueError("Responsável é obrigatório")
        try:
            datetime.strptime(self.data, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            raise ValueError("Data em formato inválido")