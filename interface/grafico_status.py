import tkinter as tk

from interface.componentes import retangulo_arredondado
from utils.constantes import (
    FONTE, COR_FUNDO, COR_SUPERFICIE, COR_BORDA, COR_TEXTO, COR_TEXTO_SECUNDARIO,
    COR_GRAFICO_EIXO, COR_GRAFICO_PADRAO,
    CORES_GRAFICO_STATUS, CORES_GRAFICO_TIPO, MSG_GRAFICO_VAZIO,
)

# Cores das barras (definidas no tema, em utils/constantes.py)
CORES_STATUS = CORES_GRAFICO_STATUS
CORES_TIPO = CORES_GRAFICO_TIPO
COR_EIXO = COR_GRAFICO_EIXO
COR_PADRAO_BARRA = COR_GRAFICO_PADRAO
MSG_SEM_TAREFAS = MSG_GRAFICO_VAZIO


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

        self.canvas = tk.Canvas(self, bg=COR_SUPERFICIE, highlightthickness=1,
                                highlightbackground=COR_BORDA,
                                highlightcolor=COR_BORDA)
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
                          fill=COR_TEXTO_SECUNDARIO, font=(FONTE, 12),
                          justify="center")
            return

        margem_x = 40
        topo = 60        # espaço para o "Total" e o número acima da barra mais alta
        base = altura - 50   # espaço para o nome da categoria embaixo

        c.create_text(margem_x, 22, text=f"Total: {total} tarefa(s)",
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
                cor = self.cores.get(categoria, COR_PADRAO_BARRA)
                x1 = centro - largura_barra / 2
                x2 = centro + largura_barra / 2
                raio = min(12, largura_barra / 2, altura_barra / 2)
                # Barra com o topo arredondado: retângulo arredondado +
                # retângulo reto cobrindo os cantos de baixo
                retangulo_arredondado(c, x1, y_topo, x2, base, raio,
                                      fill=cor, outline=cor)
                c.create_rectangle(x1, base - raio, x2, base,
                                   fill=cor, outline=cor)

            # Quantidade acima da barra (aparece "0" também)
            c.create_text(centro, y_topo - 12, text=str(valor),
                          fill=COR_TEXTO, font=(FONTE, 11, "bold"))

            # Nome da categoria + percentual embaixo
            percentual = round(valor * 100 / total)
            c.create_text(centro, base + 16, text=categoria,
                          fill=COR_TEXTO, font=(FONTE, 10))
            c.create_text(centro, base + 34, text=f"{percentual}%",
                          fill=COR_TEXTO_SECUNDARIO, font=(FONTE, 9))