"""
Componentes visuais reutilizáveis do tema (só Tkinter, sem bibliotecas extras).

- retangulo_arredondado: desenha um retângulo com cantos arredondados num Canvas
- BotaoArredondado: botão em formato de "pílula", com hover
- Pilula: etiqueta colorida arredondada (status, prioridade)
- exibir_toast: notificação no canto da tela
- aplicar_estilo_ttk: deixa Combobox, Notebook e Scrollbar com as cores do tema
"""
import tkinter as tk
from tkinter import ttk
from tkinter import font as tkfont

from utils.constantes import (
    FONTE, FONTE_BOTAO, FONTE_PILULA, FONTE_TEXTO,
    COR_FUNDO, COR_SUPERFICIE, COR_BORDA, COR_TEXTO, COR_TEXTO_SECUNDARIO,
    COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_TEXTO_PRIMARIA,
    COR_SUAVE, COR_SUAVE_HOVER, COR_TEXTO_SUAVE,
    COR_SECUNDARIA, COR_SECUNDARIA_HOVER, COR_TEXTO_SECUNDARIA,
    COR_PERIGO, COR_PERIGO_HOVER, COR_TEXTO_PERIGO,
    COR_MENU_LATERAL, COR_MENU_HOVER, COR_MENU_TEXTO,
    COR_MENU_ATIVO, COR_MENU_TEXTO_ATIVO,
    COR_CAMPO, COR_CAMPO_BORDA, COR_CAMPO_FOCO, COR_PILULA_PADRAO, CORES_TOAST,
)

# tipo do botão -> (fundo, fundo no hover, texto)
ESTILOS_BOTAO = {
    "primario": (COR_PRIMARIA, COR_PRIMARIA_HOVER, COR_TEXTO_PRIMARIA),
    "suave": (COR_SUAVE, COR_SUAVE_HOVER, COR_TEXTO_SUAVE),
    "secundario": (COR_SECUNDARIA, COR_SECUNDARIA_HOVER, COR_TEXTO_SECUNDARIA),
    "perigo": (COR_PERIGO, COR_PERIGO_HOVER, COR_TEXTO_PERIGO),
    # Itens do menu lateral
    "menu": (COR_MENU_LATERAL, COR_MENU_HOVER, COR_MENU_TEXTO),
    "menu_ativo": (COR_MENU_ATIVO, COR_MENU_ATIVO, COR_MENU_TEXTO_ATIVO),
}


def retangulo_arredondado(canvas, x1, y1, x2, y2, raio, fill, outline=None):
    """
    Desenha um retângulo com cantos arredondados num Canvas:
    4 arcos nos cantos + 2 retângulos no meio. Com raio = metade da
    altura, vira uma "pílula".
    """
    raio = max(0, min(raio, (x2 - x1) / 2, (y2 - y1) / 2))
    d = 2 * raio
    cor = fill

    if raio > 0:
        cantos = [
            (x1, y1, x1 + d, y1 + d, 90),     # superior esquerdo
            (x2 - d, y1, x2, y1 + d, 0),      # superior direito
            (x1, y2 - d, x1 + d, y2, 180),    # inferior esquerdo
            (x2 - d, y2 - d, x2, y2, 270),    # inferior direito
        ]
        for ax1, ay1, ax2, ay2, inicio in cantos:
            canvas.create_arc(ax1, ay1, ax2, ay2, start=inicio, extent=90,
                              style="pieslice", fill=cor, outline=cor)

    canvas.create_rectangle(x1 + raio, y1, x2 - raio, y2, fill=cor, outline=cor)
    canvas.create_rectangle(x1, y1 + raio, x2, y2 - raio, fill=cor, outline=cor)


def _cor_do_pai(parent):
    """Cor de fundo do widget pai, para o canto do botão "sumir" no fundo."""
    try:
        return parent.cget("bg")
    except tk.TclError:
        return COR_FUNDO


class BotaoArredondado(tk.Canvas):
    """
    Botão com cantos arredondados e hover.

    Uso:
        BotaoArredondado(frame, "Adicionar", self.salvar).pack()
        BotaoArredondado(frame, "Cancelar", self.fechar, tipo="secundario")

    tipo: "primario" (lilás), "suave" (lilás clarinho), "secundario"
          (cinza-lilás), "perigo" (vermelho), "menu" / "menu_ativo"
    alinhar: "center" ou "left" (texto encostado à esquerda, usado no menu)
    raio: arredondamento dos cantos (padrão: metade da altura = pílula)
    Funciona com pack/grid normalmente, inclusive com fill="x" / sticky="ew".
    """

    def __init__(self, parent, texto, comando, tipo="primario",
                 largura=None, altura=38, fonte=FONTE_BOTAO, padx=20,
                 alinhar="center", raio=None):
        self.fonte = tkfont.Font(font=fonte)
        if largura is None:
            largura = self.fonte.measure(texto) + 2 * padx

        super().__init__(parent, width=largura, height=altura,
                         bg=_cor_do_pai(parent), highlightthickness=0,
                         bd=0, cursor="hand2")

        self.texto = texto
        self.comando = comando
        self.padx = padx
        self.alinhar = alinhar
        self.raio = raio
        self.cor_fundo, self.cor_hover, self.cor_texto = ESTILOS_BOTAO[tipo]
        self._cor_atual = self.cor_fundo

        self.bind("<Configure>", lambda e: self._desenhar())
        self.bind("<Enter>", lambda e: self._mudar_cor(self.cor_hover))
        self.bind("<Leave>", lambda e: self._mudar_cor(self.cor_fundo))
        self.bind("<ButtonRelease-1>", self._clicar)

        self._desenhar()

    def _desenhar(self):
        self.delete("all")
        largura = self.winfo_width() if self.winfo_width() > 1 else int(self["width"])
        altura = self.winfo_height() if self.winfo_height() > 1 else int(self["height"])

        raio = altura / 2 if self.raio is None else self.raio
        retangulo_arredondado(self, 1, 1, largura - 1, altura - 1, raio,
                              fill=self._cor_atual, outline=self._cor_atual)

        if self.alinhar == "left":
            self.create_text(self.padx, altura / 2, text=self.texto, anchor="w",
                             fill=self.cor_texto, font=self.fonte)
        else:
            self.create_text(largura / 2, altura / 2, text=self.texto,
                             fill=self.cor_texto, font=self.fonte)

    def definir_tipo(self, tipo, fonte=None):
        """Troca o estilo do botão (ex.: item do menu ativo/inativo)."""
        self.cor_fundo, self.cor_hover, self.cor_texto = ESTILOS_BOTAO[tipo]
        if fonte is not None:
            self.fonte = tkfont.Font(font=fonte)
        self._cor_atual = self.cor_fundo
        self._desenhar()

    def _mudar_cor(self, cor):
        self._cor_atual = cor
        self._desenhar()

    def _clicar(self, evento):
        # Só dispara se o mouse ainda estiver em cima do botão ao soltar
        if 0 <= evento.x <= self.winfo_width() and 0 <= evento.y <= self.winfo_height():
            if self.comando:
                self.comando()


class Pilula(tk.Canvas):
    """Etiqueta arredondada, ex.: Pilula(frame, "Atrasada", "#FFE1E1", "#B3261E")."""

    def __init__(self, parent, texto, cor_fundo=None, cor_texto=None,
                 fonte=FONTE_PILULA, padx=10, altura=22):
        cor_fundo = cor_fundo or COR_PILULA_PADRAO[0]
        cor_texto = cor_texto or COR_PILULA_PADRAO[1]
        fonte = tkfont.Font(font=fonte)
        largura = fonte.measure(texto) + 2 * padx

        super().__init__(parent, width=largura, height=altura,
                         bg=_cor_do_pai(parent), highlightthickness=0, bd=0)

        retangulo_arredondado(self, 0, 0, largura, altura, altura / 2,
                              fill=cor_fundo, outline=cor_fundo)
        self.create_text(largura / 2, altura / 2, text=texto,
                         fill=cor_texto, font=fonte)


def exibir_toast(parent, mensagem, tipo="sucesso", duracao=3000):
    """Notificação no canto superior direito. tipo: "sucesso" ou "erro"."""
    cor_fundo, cor_texto, cor_borda = CORES_TOAST.get(tipo, CORES_TOAST["erro"])
    icone = "✓" if tipo == "sucesso" else "!"

    toast = tk.Frame(parent, bg=cor_fundo, highlightthickness=1,
                     highlightbackground=cor_borda)
    toast.place(relx=1.0, x=-20, y=20, anchor="ne")

    tk.Label(toast, text=f"{icone}  {mensagem}", bg=cor_fundo, fg=cor_texto,
             font=(FONTE, 10, "bold"), wraplength=300,
             justify="left").pack(padx=18, pady=12)

    toast.lift()
    parent.after(duracao, toast.destroy)
    return toast


def criar_campo(parent, fonte=(FONTE, 11)):
    """Entry no estilo do tema: fundo lilás clarinho e borda que acende no foco."""
    return tk.Entry(parent, font=fonte, fg=COR_TEXTO, bg=COR_CAMPO,
                    relief="flat", bd=0, insertbackground=COR_TEXTO,
                    highlightthickness=1, highlightbackground=COR_CAMPO_BORDA,
                    highlightcolor=COR_CAMPO_FOCO)


def aplicar_estilo_ttk(janela):
    """
    Aplica as cores do tema nos widgets ttk (Combobox, Notebook, Scrollbar).
    Chamar UMA vez, logo depois de criar a janela principal.
    """
    estilo = ttk.Style(janela)
    estilo.theme_use("clam")   # o tema "clam" aceita cores personalizadas

    # Combobox
    estilo.configure("TCombobox", fieldbackground=COR_CAMPO, background=COR_SUAVE,
                     foreground=COR_TEXTO, arrowcolor=COR_TEXTO_SUAVE,
                     bordercolor=COR_CAMPO_BORDA, lightcolor=COR_CAMPO,
                     darkcolor=COR_CAMPO, padding=4)
    estilo.map("TCombobox",
               fieldbackground=[("readonly", COR_CAMPO)],
               selectbackground=[("readonly", COR_CAMPO)],
               selectforeground=[("readonly", COR_TEXTO)],
               bordercolor=[("focus", COR_PRIMARIA)],
               background=[("active", COR_SUAVE_HOVER)])
    # Lista que abre do Combobox
    janela.option_add("*TCombobox*Listbox.background", COR_SUPERFICIE)
    janela.option_add("*TCombobox*Listbox.foreground", COR_TEXTO)
    janela.option_add("*TCombobox*Listbox.selectBackground", COR_SUAVE)
    janela.option_add("*TCombobox*Listbox.selectForeground", COR_TEXTO_SUAVE)
    janela.option_add("*TCombobox*Listbox.font", FONTE_TEXTO)

    # Abas (tela de gráficos)
    estilo.configure("TNotebook", background=COR_FUNDO, borderwidth=1,
                     bordercolor=COR_BORDA, lightcolor=COR_SUPERFICIE,
                     darkcolor=COR_BORDA, tabmargins=(0, 0, 0, 0))
    estilo.configure("TNotebook.Tab", background=COR_SECUNDARIA,
                     foreground=COR_TEXTO_SECUNDARIO, padding=(16, 6),
                     font=FONTE_BOTAO, borderwidth=0,
                     lightcolor=COR_SECUNDARIA, darkcolor=COR_BORDA,
                     bordercolor=COR_BORDA)
    estilo.map("TNotebook.Tab",
               background=[("selected", COR_SUPERFICIE), ("active", COR_SUAVE)],
               foreground=[("selected", COR_TEXTO_SUAVE)],
               lightcolor=[("selected", COR_SUPERFICIE)])

    # Barra de rolagem
    estilo.configure("Vertical.TScrollbar", background=COR_SUAVE,
                     troughcolor=COR_FUNDO, bordercolor=COR_FUNDO,
                     arrowcolor=COR_TEXTO_SUAVE, lightcolor=COR_SUAVE,
                     darkcolor=COR_SUAVE)
    estilo.map("Vertical.TScrollbar", background=[("active", COR_SUAVE_HOVER)])
