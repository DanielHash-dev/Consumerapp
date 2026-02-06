# Gerenciador de Inicialização do Windows

Um aplicativo desktop em **Python** para gerenciar programas que iniciam com o Windows, monitorar consumo de CPU e RAM, e desativar aplicativos de forma segura, com registro de histórico. Desenvolvido como projeto acadêmico usando **Tkinter**.

---

## Funcionalidades

* Exibe os programas que iniciam automaticamente no Windows (usuário e sistema).
* Classifica o impacto de cada programa em **Baixo**, **Médio** ou **Alto**.
* Permite **desativar programas de inicialização** com confirmação e registro automático no histórico.
* Aba de **histórico** mostrando todas as desativações realizadas.
* Monitoramento em tempo real de **CPU** e **RAM** consumidos por cada programa.
* Indicador de **saúde do sistema** baseado na quantidade de programas de alto impacto.
* **Tema claro e escuro** alternáveis.
* Interface moderna e responsiva com **Tkinter**.

---

## Requisitos

* **Python 3.8+**
* Pacotes Python:

```bash
pip install psutil
```

* Sistema operacional: **Windows** (por conta do uso de `winreg`).

> ⚠️ Para desativar programas do sistema, o aplicativo **precisa ser executado como administrador**.

---

## Estrutura do Projeto

```
.
├── app.py           # Ponto de entrada do aplicativo
├── ui.py            # Interface gráfica usando Tkinter
├── consumo.py       # Funções de monitoramento, registro e desativação
├── historico.txt    # Arquivo gerado automaticamente para registrar ações
├── README.md        # Este arquivo
```

### Descrição dos arquivos

* **app.py**: Inicia o aplicativo, verifica permissões de administrador e lança a interface.
* **ui.py**: Cria a interface gráfica com abas de usuário, sistema, histórico e recursos, além de fornecer interatividade com os programas.
* **consumo.py**: Contém funções para obter programas de inicialização, medir consumo de CPU/RAM, classificar impacto, desativar programas e registrar histórico.
* **historico.txt**: Armazena todas as desativações de programas realizadas pelo usuário.

---

## Como usar

1. Clone ou baixe o projeto.
2. Instale o pacote necessário:

```bash
pip install psutil
```

3. Execute o aplicativo:

```bash
python app.py
```

4. Caso solicitado, permita que o app seja executado como administrador para desativar programas do sistema.

5. Navegue pelas abas:

* **Usuário**: Programas de inicialização do usuário atual.
* **Sistema**: Programas de inicialização do sistema.
* **Histórico**: Lista de programas desativados e seus impactos.
* **Recursos**: Monitoramento em tempo real de CPU e RAM de cada programa.

6. Use o menu de contexto (clique com o botão direito) para:

* Desativar programas.
* Mostrar detalhes.
* Copiar nome do programa.
* Abrir a pasta do programa.

---

## Telas

* Interface moderna com temas claro/escuro.
* Indicadores visuais de **saúde do sistema**.
* Gráficos de consumo de **CPU e RAM** por programa.

---

## Observações

* O aplicativo não desinstala programas, apenas **remove da inicialização** do Windows.
* Algumas ações podem requerer **permissão de administrador**.
* Histórico de ações é salvo em `historico.txt`.

---

## Autor

**Daniel Hash Marques**
Projeto acadêmico — Python + Tkinter
