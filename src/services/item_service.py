from typing import List, Tuple, Optional
from src.models.item import Item
from src.repositories.item_repository import ItemRepository
from src.utils.logger import logger

class ItemService:
    def __init__(self):
        self.repository = ItemRepository()

    def cadastrar(self, item: Item) -> Tuple[bool, str]:
        """Cadastra um novo item com validações"""
        try:
            item.validar()

            # Verifica se item já existe
            if self._item_existe(item.nome):
                return False, "Item já cadastrado com este nome"

            return self.repository.salvar(item)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Erro ao cadastrar item: {e}")
            return False, "Erro interno ao cadastrar item"

    def listar_todos(self) -> List[Item]:
        """Retorna todos os itens ordenados por nome"""
        try:
            return self.repository.listar_todos()
        except Exception as e:
            logger.error(f"Erro ao listar itens: {e}")
            return []

    def buscar_por_nome(self, nome: str) -> List[Item]:
        """Busca itens por similaridade no nome"""
        try:
            if not nome.strip():
                return self.listar_todos()

            return self.repository.buscar_por_nome(nome.strip())
        except Exception as e:
            logger.error(f"Erro ao buscar itens: {e}")
            return []

    def buscar_por_id(self, item_id: int) -> Optional[Item]:
        """Obtém um item pelo ID"""
        try:
            return self.repository.buscar_por_id(item_id)
        except Exception as e:
            logger.error(f"Erro ao buscar item: {e}")
            return None

    def atualizar(self, item: Item) -> Tuple[bool, str]:
        """Atualiza um item existente"""
        try:
            item.validar()

            # Verifica se item existe
            if not self.repository.buscar_por_id(item.id):
                return False, "Item não encontrado"

            return self.repository.salvar(item)

        except ValueError as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Erro ao atualizar item: {e}")
            return False, "Erro interno ao atualizar item"

    def remover(self, item_id: int) -> Tuple[bool, str]:
        """Remove um item do sistema"""
        try:
            # Verifica se item existe
            if not self.repository.buscar_por_id(item_id):
                return False, "Item não encontrado"

            return self.repository.remover(item_id)

        except Exception as e:
            logger.error(f"Erro ao remover item: {e}")
            return False, "Erro interno ao remover item"

    def _item_existe(self, nome: str) -> bool:
        """Verifica se item com mesmo nome já existe"""
        try:
            itens = self.repository.buscar_por_nome(nome)
            return any(item.nome.lower() == nome.lower() for item in itens)
        except Exception:
            return False