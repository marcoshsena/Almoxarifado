import logging

from src.core.auth import Autenticador
from src.cli.menu_principal import MenuPrincipal
from src.services import ItemService


def executar_tarefas_agendadas():
    """Executa rotinas automáticas do sistema"""
    item_service = ItemService()
    resultados = item_service.processar_vencimentos()

    if resultados:
        logging.info(f"Baixa automática: {len(resultados)} itens processados")
        for r in resultados:
            logging.info(f"{r['item']} - {r['mensagem']}")

if __name__ == "__main__":
    executar_tarefas_agendadas()  # Executa antes do menu principal
    MenuPrincipal.iniciar_sistema()

if __name__ == "__main__":
    MenuPrincipal.iniciar_sistema()