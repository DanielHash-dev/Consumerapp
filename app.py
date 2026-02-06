from tkinter import Tk
import tkinter as tk
from ui import StartupDetectorUI
from tkinter import messagebox
import ctypes
import os
import sys
from tkinter import messagebox, Tk


def verifica_admin():
    """Retorna True se o app está sendo executado como administrador"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


# Verifica se é admin antes de iniciar o app
if not verifica_admin():
    root = Tk()
    root.withdraw()  # Esconde a janela principal temporariamente

    resposta = messagebox.askyesno(
        "Permissão de Administrador",
        "Este aplicativo precisa ser executado como administrador para desativar programas.\n"
        "Deseja reiniciar como administrador?"
    )

    if resposta:
        # Reinicia o app como administrador
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, os.path.abspath(__file__), None, 1
        )
        sys.exit()  # Sai do processo atual, o novo será admin
    # Se o usuário responder "não", apenas continua normalmente
    root.destroy()  # Fecha a janela temporária

# Importa aqui porque precisa do Tkinter

if __name__ == "__main__":
    root = Tk()
    app = StartupDetectorUI(root)  # Sua interface principal
    root.mainloop()
