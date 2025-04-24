import sqlite3
from pathlib import Path
from datetime import datetime
import logging
from typing import Optional

class DatabaseManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.__init__()
        return cls._instance

    def __init__(self):
        self.db_path = Path("database/almoxarifado.db")
        self.backup_dir = Path("database/backups")
        self.backup_dir.mkdir(exist_ok=True, parents=True)
        self.__inicializar_banco()

    def __inicializar_banco(self):
        """Cria estrutura inicial do banco"""
        with self.criar_conexao() as conn:
            cursor = conn.cursor()

            # Tabela Itens
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS itens (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                marca TEXT,
                quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                saldo_inicial INTEGER NOT NULL DEFAULT 0,
                unidade TEXT,
                preco REAL NOT NULL CHECK(preco >= 0),
                tipo TEXT NOT NULL,
                descricao TEXT,
                data_validade TEXT,
                criado_em TEXT DEFAULT CURRENT_TIMESTAMP
            )""")

            # Tabela Movimentações
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS movimentacoes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER NOT NULL,
                tipo TEXT NOT NULL CHECK(tipo IN ('entrada', 'saída')),
                quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                data TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                responsavel TEXT NOT NULL,
                motivo TEXT,
                FOREIGN KEY(item_id) REFERENCES itens(id) ON DELETE CASCADE
            )""")

            conn.commit()

    def criar_conexao(self) -> sqlite3.Connection:
        """Cria conexão segura com o banco"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.execute("PRAGMA foreign_keys = ON")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Erro ao conectar ao banco: {e}")
            raise

    def fazer_backup(self) -> bool:
        """Realiza backup completo do banco"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.backup_dir / f"backup_{timestamp}.db"

        try:
            with self.criar_conexao() as src, sqlite3.connect(backup_path) as dst:
                src.backup(dst)
            logging.info(f"Backup criado em {backup_path}")
            return True
        except Exception as e:
            logging.error(f"Falha no backup: {e}")
            return False

# Singleton global
db_manager = DatabaseManager()