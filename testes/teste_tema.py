"""
Testes da US do tema visual: confere se as cores do tema têm contraste
suficiente para leitura (critério de aceite "bom contraste").

Usa a fórmula de contraste das diretrizes de acessibilidade (WCAG):
4.5 é o mínimo recomendado para texto normal.

Rodar (da pasta do projeto):  python -m unittest testes.teste_tema -v
"""
import unittest

from utils import constantes as c

CONTRASTE_MINIMO = 4.5


def _luminancia(cor):
    cor = cor.lstrip("#")
    canais = [int(cor[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    canais = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4
              for v in canais]
    r, g, b = canais
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contraste(cor1, cor2):
    """Razão de contraste entre duas cores (1 a 21)."""
    clara, escura = sorted([_luminancia(cor1), _luminancia(cor2)], reverse=True)
    return (clara + 0.05) / (escura + 0.05)


class TesteContrasteTema(unittest.TestCase):

    def assertLegivel(self, texto, fundo, nome):
        valor = contraste(texto, fundo)
        self.assertGreaterEqual(
            valor, CONTRASTE_MINIMO,
            f"{nome}: contraste {valor:.2f} abaixo de {CONTRASTE_MINIMO}"
        )

    def test_textos_no_fundo_e_nos_cards(self):
        for fundo in (c.COR_FUNDO, c.COR_SUPERFICIE):
            self.assertLegivel(c.COR_TEXTO, fundo, "texto")
            self.assertLegivel(c.COR_TEXTO_SECUNDARIO, fundo, "texto secundário")
            self.assertLegivel(c.COR_TEXTO_LABEL, fundo, "label")

    def test_texto_nos_campos(self):
        self.assertLegivel(c.COR_TEXTO, c.COR_CAMPO, "texto do campo")

    def test_botoes(self):
        self.assertLegivel(c.COR_TEXTO_PRIMARIA, c.COR_PRIMARIA, "botão primário")
        self.assertLegivel(c.COR_TEXTO_PRIMARIA, c.COR_PRIMARIA_HOVER, "botão primário (hover)")
        self.assertLegivel(c.COR_TEXTO_SUAVE, c.COR_SUAVE, "botão suave")
        self.assertLegivel(c.COR_TEXTO_SUAVE, c.COR_SUAVE_HOVER, "botão suave (hover)")
        self.assertLegivel(c.COR_TEXTO_SECUNDARIA, c.COR_SECUNDARIA, "botão secundário")
        self.assertLegivel(c.COR_TEXTO_SECUNDARIA, c.COR_SECUNDARIA_HOVER, "botão secundário (hover)")

    def test_botao_de_excluir(self):
        self.assertLegivel(c.COR_TEXTO_PERIGO, c.COR_PERIGO, "botão excluir")
        self.assertLegivel(c.COR_TEXTO_PERIGO, c.COR_PERIGO_HOVER, "botão excluir (hover)")

    def test_menu_lateral(self):
        self.assertLegivel(c.COR_MENU_TEXTO, c.COR_MENU_LATERAL, "item do menu")
        self.assertLegivel(c.COR_MENU_TEXTO, c.COR_MENU_HOVER, "item do menu (hover)")
        self.assertLegivel(c.COR_MENU_TEXTO_ATIVO, c.COR_MENU_ATIVO, "item do menu ativo")

    def test_numeros_da_home(self):
        for titulo, (cor_numero, _destaque) in c.CORES_BIG_NUMBER.items():
            self.assertLegivel(cor_numero, c.COR_SUPERFICIE, f"número {titulo}")

    def test_pilulas_de_status(self):
        for status in c.STATUS_TODOS:
            fundo, texto = c.CORES_PILULA_STATUS[status]
            self.assertLegivel(texto, fundo, f"pílula {status}")
        fundo, texto = c.COR_PILULA_PADRAO
        self.assertLegivel(texto, fundo, "pílula padrão")

    def test_toasts(self):
        for tipo, (fundo, texto, _borda) in c.CORES_TOAST.items():
            self.assertLegivel(texto, fundo, f"toast {tipo}")

    def test_todo_status_tem_pilula_e_cor_no_grafico(self):
        for status in c.STATUS_TODOS:
            self.assertIn(status, c.CORES_PILULA_STATUS)
            self.assertIn(status, c.CORES_GRAFICO_STATUS)

    def test_todo_tipo_tem_cor_no_grafico(self):
        for tipo in c.TIPOS:
            self.assertIn(tipo, c.CORES_GRAFICO_TIPO)


if __name__ == "__main__":
    unittest.main()
