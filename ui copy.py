import tkinter as tk
from tkinter import ttk, messagebox
from Consumo import (
    obter_programas_usuario,
    obter_programas_sistema,
    desativar_programa,
    ler_historico
)
import psutil

TEMA_ESCURO = {
    "bg": "#1e1e2e",
    "panel": "#2a2a3d",
    "text": "#ffffff",
    "accent": "#4f8cff",
    "danger": "#d9534f"
}

TEMA_CLARO = {
    "bg": "#f5f5f5",
    "panel": "#ffffff",
    "text": "#000000",
    "accent": "#0078d7",
    "danger": "#c9302c"
}


class StartupDetectorUI:
    def __init__(self, root):
        self.root = root
        self.root.withdraw()
        self.root.title("Gerenciador de Inicialização do Windows")
        self.centralizar_janela(700, 610)

        self.tema_atual = TEMA_ESCURO
        self.total_desativados = 0
        self.tempo_estimado = 0

        self.configurar_estilo()
        self.criar_interface()

        self.root.attributes("-alpha", 0.0)
        self.root.deiconify()
        self.fade_in()

    # ---------------- CENTRALIZAR ----------------
    def centralizar_janela(self, largura=700, altura=610):
        largura_tela = self.root.winfo_screenwidth()
        altura_tela = self.root.winfo_screenheight()
        x = (largura_tela // 2) - (largura // 2)
        y = (altura_tela // 2) - (altura // 2)
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")

    # ---------------- ESTILO ----------------
    def configurar_estilo(self):
        self.style = ttk.Style()
        self.style.theme_use("default")

        self.root.configure(bg=self.tema_atual["bg"])

        self.style.configure("TFrame", background=self.tema_atual["bg"])
        self.style.configure("TLabel", background=self.tema_atual["bg"], foreground=self.tema_atual["text"])
        self.style.configure("TButton", background=self.tema_atual["accent"], foreground="#ffffff")
        self.style.configure("TNotebook", background=self.tema_atual["bg"])
        self.style.configure(
            "TNotebook.Tab",
            background=self.tema_atual["panel"],
            foreground=self.tema_atual["text"],
            padding=(12, 6),
            font=("Segoe UI", 11, "bold")
        )
        self.style.map(
            "TNotebook.Tab",
            background=[("selected", self.tema_atual["accent"])],
            foreground=[("selected", "#ffffff")]
        )

        # Estilos de saúde
        self.style.configure("SaudeBoa.TLabel", foreground="#4CAF50", background=self.tema_atual["bg"])
        self.style.configure("SaudeModerada.TLabel", foreground="#FFB300", background=self.tema_atual["bg"])
        self.style.configure("SaudeCritica.TLabel", foreground="#D32F2F", background=self.tema_atual["bg"])

    # ---------------- INTERFACE ----------------
    def criar_interface(self):
        for w in self.root.winfo_children():
            w.destroy()

        # ===== TOPO =====
        topo = ttk.Frame(self.root)
        topo.pack(fill="x", padx=12, pady=6)

        ttk.Label(topo, text="Gerenciador", font=("Segoe UI", 16, "bold"), foreground=self.tema_atual["accent"]).pack(side="left")

        self.label_status = ttk.Label(topo, text="🚀 Nenhuma otimização", foreground=self.tema_atual["accent"])
        self.label_status.pack(side="left", padx=20)

        ttk.Button(topo, text="🌗 Tema", command=self.alternar_tema).pack(side="right")

        self.label_saude = ttk.Label(topo, text="🟢 Saúde: Boa", font=("Segoe UI", 11, "bold"), style="SaudeBoa.TLabel")
        self.label_saude.pack(side="right", padx=20)

        # ===== NOTEBOOK =====
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        self.aba_usuario = ttk.Frame(notebook)
        self.aba_sistema = ttk.Frame(notebook)
        self.aba_historico = ttk.Frame(notebook)
        self.aba_recursos = ttk.Frame(notebook)

        notebook.add(self.aba_usuario, text="👤 Usuário")
        notebook.add(self.aba_sistema, text="💻 Sistema")
        notebook.add(self.aba_historico, text="📃 Histórico")
        notebook.add(self.aba_recursos, text="⚡ Recursos")

        self.criar_aba_programas(self.aba_usuario, obter_programas_usuario)
        self.criar_aba_programas(self.aba_sistema, obter_programas_sistema)
        self.criar_aba_historico()
        self.criar_aba_recursos(self.aba_recursos)

        # ===== RODAPÉ =====
        rodape = ttk.Frame(self.root)
        rodape.pack(side="bottom", fill="x")
        ttk.Label(
            rodape,
            text="Desenvolvido por Daniel Marques • Projeto acadêmico — Python + Tkinter",
            font=("Segoe UI", 9),
            anchor="center"
        ).pack(pady=4)

    # ---------------- ABA PROGRAMAS ----------------
    def criar_aba_programas(self, aba, funcao):
        filtros = ttk.Frame(aba)
        filtros.pack(fill="x", padx=10, pady=(8, 0))

        self.var_alto = tk.BooleanVar()
        ttk.Checkbutton(filtros, text="Mostrar apenas impacto alto", variable=self.var_alto).pack(side="left")

        frame = ttk.Frame(aba)
        frame.pack(fill="both", expand=True, padx=10, pady=(5, 0))

        lista = tk.Listbox(frame, bg=self.tema_atual["panel"], fg=self.tema_atual["text"],
                           selectbackground=self.tema_atual["accent"], highlightthickness=0,
                           font=("Segoe UI", 10))
        lista.pack(side="left", fill="both", expand=True)

        detalhes = tk.Text(frame, width=42, bg=self.tema_atual["panel"], fg=self.tema_atual["text"],
                           insertbackground=self.tema_atual["text"], relief="flat", state="disabled",
                           font=("Segoe UI", 10))
        detalhes.pack(side="right", padx=10, fill="both")

        botoes = ttk.Frame(aba)
        botoes.pack(side="bottom", fill="x", padx=10, pady=8)

        # ---------------- FUNÇÕES ----------------
        def carregar():
            lista.delete(0, tk.END)
            self.programas = funcao()
            filtrados = [p for p in self.programas if not self.var_alto.get() or p["impacto"] == "Alto"]
            for p in filtrados:
                lista.insert(tk.END, f"{p['nome']} | Impacto: {p['impacto']}")
            self.atualizar_saude(self.programas)

        def mostrar(event=None):
            if not lista.curselection():
                return
            p = self.programas[lista.curselection()[0]]
            detalhes.config(state="normal")
            detalhes.delete("1.0", tk.END)
            detalhes.insert(tk.END, f"Nome:\n{p['nome']}\n\nCaminho:\n{p['caminho']}\n\nImpacto: {p['impacto']}")
            detalhes.config(state="disabled")

        def desativar():
            if not lista.curselection():
                return
            p = self.programas[lista.curselection()[0]]
            if messagebox.askyesno("Confirmar", f"Desativar '{p['nome']}'?\nImpacto: {p['impacto']}"):
                if desativar_programa(p):
                    self.total_desativados += 1
                    self.tempo_estimado += {"Baixo": 1, "Médio": 3, "Alto": 5}[p["impacto"]]
                    self.atualizar_status()
                    carregar()
                else:
                    messagebox.showerror("Erro", "Permissão negada.\nExecute como administrador.")

        def copiar_nome():
            if not lista.curselection():
                return
            p = self.programas[lista.curselection()[0]]
            self.root.clipboard_clear()
            self.root.clipboard_append(p["nome"])
            messagebox.showinfo("Copiado", f"Nome '{p['nome']}' copiado para a área de transferência.")

        def abrir_caminho():
            import os, subprocess
            if not lista.curselection():
                return
            p = self.programas[lista.curselection()[0]]
            caminho = os.path.dirname(p["caminho"])
            if os.path.exists(caminho):
                subprocess.Popen(f'explorer "{caminho}"')
            else:
                messagebox.showerror("Erro", "Caminho não encontrado.")

        # Menu de contexto
        menu_contexto = tk.Menu(self.root, tearoff=0)
        menu_contexto.add_command(label="Desativar", command=desativar)
        menu_contexto.add_command(label="Mostrar detalhes", command=mostrar)
        menu_contexto.add_separator()
        menu_contexto.add_command(label="Copiar nome", command=copiar_nome)
        menu_contexto.add_command(label="Abrir caminho", command=abrir_caminho)

        def abrir_menu(event):
            if lista.curselection():
                menu_contexto.post(event.x_root, event.y_root)

        lista.bind("<Button-3>", abrir_menu)
        lista.bind("<<ListboxSelect>>", mostrar)

        ttk.Button(botoes, text="Atualizar", command=carregar).pack(side="left", padx=5)
        ttk.Button(botoes, text="Desativar", command=desativar).pack(side="left", padx=5)

        carregar()

    # ---------------- ABA HISTÓRICO ----------------
    def criar_aba_historico(self):
        texto = tk.Text(self.aba_historico, bg=self.tema_atual["panel"], fg=self.tema_atual["text"],
                        insertbackground=self.tema_atual["text"], relief="flat", font=("Segoe UI", 10))
        texto.pack(fill="both", expand=True, padx=10, pady=10)
        texto.insert(tk.END, ler_historico())
        texto.config(state="disabled")

    # ---------------- ABA RECURSOS ----------------
    def criar_aba_recursos(self, aba):
        frame = ttk.Frame(aba)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        canvas = tk.Canvas(frame, bg=self.tema_atual["panel"])
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")
        canvas.configure(yscrollcommand=scrollbar.set)

        inner_frame = ttk.Frame(canvas)
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        inner_frame.bind("<Configure>", on_frame_configure)

        self.recursos_widgets = []

        total_ram = psutil.virtual_memory().total / (1024*1024)

        def atualizar_recursos():
            for w in self.recursos_widgets:
                w.destroy()
            self.recursos_widgets.clear()

            programas = obter_programas_usuario() + obter_programas_sistema()

            for prog in programas:
                prog_frame = ttk.Frame(inner_frame, relief="ridge", padding=5)
                prog_frame.pack(fill="x", pady=3)
                self.recursos_widgets.append(prog_frame)

                ttk.Label(prog_frame, text=prog["nome"], font=("Segoe UI", 10, "bold")).pack(anchor="w")

                cpu_bar = ttk.Progressbar(prog_frame, maximum=100, value=prog.get("cpu", 0))
                cpu_bar.pack(fill="x", pady=2)
                ttk.Label(prog_frame, text=f"CPU: {prog.get('cpu', 0)}%").pack(anchor="w")

                ram_percent = round((prog.get("ram", 0) / total_ram) * 100, 1)
                ram_bar = ttk.Progressbar(prog_frame, maximum=100, value=ram_percent)
                ram_bar.pack(fill="x", pady=2)
                ttk.Label(prog_frame, text=f"RAM: {prog.get('ram', 0)} MB ({ram_percent}%)").pack(anchor="w")

            self.root.after(3000, atualizar_recursos)

        atualizar_recursos()

    # ---------------- STATUS ----------------
    def atualizar_status(self):
        self.label_status.config(
            text=f"🚀 {self.total_desativados} programas desativados | ⏱ ~{self.tempo_estimado}s economizados"
        )

    def atualizar_saude(self, programas):
        altos = sum(1 for p in programas if p["impacto"] == "Alto")
        if altos <= 1:
            self.label_saude.config(text="🤩 Saúde: Boa", style="SaudeBoa.TLabel")
        elif altos <= 3:
            self.label_saude.config(text="🙂 Saúde: Moderada", style="SaudeModerada.TLabel")
        else:
            self.label_saude.config(text="😭 Saúde: Crítica", style="SaudeCritica.TLabel")

    # ---------------- TOGGLE TEMA ----------------
    def alternar_tema(self):
        self.tema_atual = TEMA_CLARO if self.tema_atual == TEMA_ESCURO else TEMA_ESCURO
        self.configurar_estilo()
        self.criar_interface()

    # ---------------- FADE ----------------
    def fade_in(self, passo=0.01, intervalo=10):
        alpha = float(self.root.attributes("-alpha"))
        if alpha < 1.0:
            alpha = min(alpha + passo, 1.0)
            self.root.attributes("-alpha", alpha)
            self.root.after(intervalo, lambda: self.fade_in(passo, intervalo))

    def fade_out(self, callback=None, passo=0.02, intervalo=10):
        alpha = float(self.root.attributes("-alpha"))
        if alpha > 0:
            alpha = max(alpha - passo, 0)
            self.root.attributes("-alpha", alpha)
            self.root.after(intervalo, lambda: self.fade_out(callback, passo, intervalo))
        else:
            if callback:
                callback()
            else:
                self.root.destroy()
