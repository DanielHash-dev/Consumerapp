import winreg
import os
import datetime
import getpass
import psutil

HISTORICO = "historico.txt"


# ---------------- HISTÓRICO ----------------
def registrar_historico(nome, impacto):
    data = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    usuario = getpass.getuser()
    linha = f"[{data}] Usuário: {usuario} | DESATIVADO | {nome} | Impacto: {impacto}\n"
    with open(HISTORICO, "a", encoding="utf-8") as f:
        f.write(linha)


def ler_historico():
    if not os.path.exists(HISTORICO):
        return "Nenhuma ação registrada."
    with open(HISTORICO, "r", encoding="utf-8") as f:
        return f.read()


# ---------------- IMPACTO ----------------
def classificar_impacto(nome):
    nome = nome.lower()
    if any(p in nome for p in ["onedrive", "steam", "discord"]):
        return "Alto"
    if any(p in nome for p in ["update", "launcher"]):
        return "Médio"
    return "Baixo"


# ---------------- OBTER PROGRAMAS ----------------
def obter_programas(chave, origem):
    programas = []
    i = 0
    try:
        while True:
            nome, caminho, _ = winreg.EnumValue(chave, i)
            impacto = classificar_impacto(nome)
            programas.append({
                "nome": nome,
                "caminho": caminho,
                "origem": origem,
                "impacto": impacto
            })
            i += 1
    except OSError:
        pass
    return programas


# ---------------- CPU E RAM ----------------
def adicionar_consumo(programas):
    """
    Adiciona 'cpu' (%) e 'ram' (MB) para cada programa se estiver rodando.
    """
    # Cria um dicionário de processos ativos
    processos = {p.name().lower(): p for p in psutil.process_iter(['name', 'cpu_percent', 'memory_info'])}

    for prog in programas:
        nome_prog = prog['nome'].lower()
        cpu = 0.0
        ram = 0.0
        for p_name, p_obj in processos.items():
            if nome_prog in p_name:
                cpu = p_obj.info['cpu_percent']
                ram = round(p_obj.info['memory_info'].rss / (1024 * 1024), 1)  # MB
                break
        prog['cpu'] = cpu
        prog['ram'] = ram
    return programas


def obter_programas_usuario():
    chave = winreg.OpenKey(
        winreg.HKEY_CURRENT_USER,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    )
    programas = obter_programas(chave, "Usuário")
    return adicionar_consumo(programas)


def obter_programas_sistema():
    chave = winreg.OpenKey(
        winreg.HKEY_LOCAL_MACHINE,
        r"Software\Microsoft\Windows\CurrentVersion\Run"
    )
    programas = obter_programas(chave, "Sistema")
    return adicionar_consumo(programas)


# ---------------- DESATIVAR ----------------
def desativar_programa(programa):
    try:
        raiz = winreg.HKEY_CURRENT_USER if programa["origem"] == "Usuário" else winreg.HKEY_LOCAL_MACHINE
        chave = winreg.OpenKey(
            raiz,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0,
            winreg.KEY_SET_VALUE
        )
        winreg.DeleteValue(chave, programa["nome"])
        registrar_historico(programa["nome"], programa["impacto"])
        return True
    except PermissionError:
        return False


# ---------------- FUNÇÃO UNIFICADA PARA UI ----------------
def obter_programas_startup():
    return obter_programas_usuario() + obter_programas_sistema()
