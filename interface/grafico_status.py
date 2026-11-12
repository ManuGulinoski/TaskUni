import tkinter as tk

from utils.constantes import (
    COR_FUNDO,
    STATUS_A_FAZER, STATUS_EM_ANDAMENTO, STATUS_CONCLUIDA, STATUS_ATRASADA,
    TIPO_PROVA, TIPO_TRABALHO, TIPO_EXERCICIO,
)

FONTE = "Segoe UI"
COR_TEXTO = "#111827"
COR_TEXTO_SECUNDARIO = "#6B7280"
COR_EIXO = "#D1D5DB"
COR_PADRAO_BARRA = "#9CA3AF"

CORES_STATUS = {
    STATUS_A_FAZER: "#378ADD",       # azul
    STATUS_EM_ANDAMENTO: "#EF9F27",  # amarelo
    STATUS_CONCLUIDA: "#16A34A",     # verde
    STATUS_ATRASADA: "#DC2626",      # vermelho
}

CORES_TIPO = {
    TIPO_PROVA: "#7F77DD",       # roxo
    TIPO_TRABALHO: "#E06C26",    # laranja
    TIPO_EXERCICIO: "#0D9488",   # verde-azulado
}

MSG_SEM_TAREFAS = "Nenhuma tarefa cadastrada para exibir no gráfico."


class GraficoBarras(tk.Frame):
    """
    Gráfico de barras com a quantidade de tarefas por categoria
    (status, tipo...). Desenhado num tk.Canvas (não precisa instalar nada).

    Uso:
        grafico = GraficoBarras(parent, cores=CORES_STATUS)
        grafico.atualizar({"A fazer": 3, "Em andamento": 1, ...})

    cores: dicionário categoria -> cor da barra (padrão: cores dos status)
    """

    def __init__(self, parent, cores=None):
        super().__init__(parent, bg=COR_FUNDO)
        self.contagem = {}
        self.cores = cores if cores is not None else CORES_STATUS

        self.canvas = tk.Canvas(self, bg="white", highlightthickness=1,
                                highlightbackground="#E5E7EB")
        self.canvas.pack(fill="both", expand=True)

        # Redesenha quando a janela muda de tamanho
        self.canvas.bind("<Configure>", lambda e: self._desenhar())

    def atualizar(self, contagem):
        """Recebe o dicionário de contar_por_status / contar_por_tipo e redesenha."""
        self.contagem = dict(contagem)
        self._desenhar()

    def _desenhar(self):
        c = self.canvas
        c.delete("all")

        largura = c.winfo_width()
        altura = c.winfo_height()
        if largura < 50 or altura < 50:   # ainda não foi exibido na tela
            return

        total = sum(self.contagem.values())

        # Lista vazia: mostra mensagem no lugar das barras
        if total == 0:
            c.create_text(largura / 2, altura / 2, text=MSG_SEM_TAREFAS,
                          fill=COR_TEXTO_SECUNDARIO, font=(FONTE, 12))
            return

        margem_x = 40
        topo = 60        # espaço para o "Total" e o número acima da barra mais alta
        base = altura - 50   # espaço para o nome da categoria embaixo

        c.create_text(margem_x, 18, text=f"Total: {total} tarefa(s)",
                      anchor="w", fill=COR_TEXTO, font=(FONTE, 11, "bold"))
        c.create_line(margem_x, base, largura - margem_x, base, fill=COR_EIXO, width=2)

        maior = max(self.contagem.values())
        qtd = len(self.contagem)
        espaco = (largura - 2 * margem_x) / qtd
        largura_barra = min(espaco * 0.6, 120)

        for i, (categoria, valor) in enumerate(self.contagem.items()):
            centro = margem_x + espaco * i + espaco / 2
            altura_barra = (base - topo) * valor / maior
            y_topo = base - altura_barra

            if valor > 0:
                c.create_rectangle(centro - largura_barra / 2, y_topo,
                                   centro + largura_barra / 2, base,
                                   fill=self.cores.get(categoria, COR_PADRAO_BARRA),
                                   outline="")

            # Quantidade acima da barra (aparece "0" também)
            c.create_text(centro, y_topo - 12, text=str(valor),
                          fill=COR_TEXTO, font=(FONTE, 11, "bold"))

            # Nome da categoria + percentual embaixo
            percentual = round(valor * 100 / total)
            c.create_text(centro, base + 16, text=categoria,
                          fill=COR_TEXTO, font=(FONTE, 10))
            c.create_text(centro, base + 34, text=f"{percentual}%",
                          fill=COR_TEXTO_SECUNDARIO, font=(FONTE, 9))