import logging
from pathlib import Path

def configurar_logger():
    """Configura o sistema de logging global"""
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(logs_dir / "almoxarifado.log"),
            logging.StreamHandler()
        ]
    )

# Configura o logger ao importar o módulo
configurar_logger()

# Cria o logger global
logger = logging.getLogger(__name__)