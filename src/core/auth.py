from getpass import getpass
import hashlib

class Autenticador:
    @staticmethod
    def login():
        """Autenticação simples do usuário"""
        print("=== LOGIN ===")
        usuario = input("Usuário: ")
        senha = input("Senha: ")

        # Credenciais temporárias - substitua por um sistema real
        if usuario == "admin" and senha == "admin123":
            return True
        print("Credenciais inválidas!")
        return False