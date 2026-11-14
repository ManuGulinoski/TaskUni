from ctkfontawesome import icon_to_image

from utils.constantes import (
    COR_ICONE_EDITAR,
    COR_ICONE_EXCLUIR,
    COR_ICONE_CONCLUIR,
    COR_PRIMARIA
)

_icones = None
_icones_menu = None
_icones_cards = {}
_icones_frase = None


def criar_icones():

    global _icones

    if _icones is None:
        _icones = {
            "editar": icon_to_image(
                "pen",
                fill=COR_ICONE_EDITAR,
                scale_to_width=16
            ),

            "excluir": icon_to_image(
                "trash",
                fill=COR_ICONE_EXCLUIR,
                scale_to_width=16
            ),

            "concluir": icon_to_image(
                "check",
                fill=COR_ICONE_CONCLUIR,
                scale_to_width=16
            )
        }

    return _icones


def criar_icones_menu():
    """Ícones para menus nativos do Tkinter."""

    global _icones_menu

    if _icones_menu is None:
        _icones_menu = {
            "tarefa": icon_to_image(
                "list-check",
                fill="#000000",
                scale_to_width=16
            ),

            "disciplina": icon_to_image(
                "layer-group",
                fill="#000000",
                scale_to_width=16
            ),
        }

    return _icones_menu


def obter_icone_card(nome, cor):
    """Ícone colorido para os cards da Home, com cache.

    Os cards são recriados a cada atualização da Home, então o cache
    evita gerar o mesmo ícone de novo toda vez (e mantém a referência
    da imagem viva, senão ela some da tela).
    """

    chave = (nome, cor)

    if chave not in _icones_cards:
        _icones_cards[chave] = icon_to_image(
            nome,
            fill=cor,
            scale_to_width=16
        )

    return _icones_cards[chave]


def criar_icones_frase():
    """Ícones do card de frase motivacional."""

    global _icones_frase

    if _icones_frase is None:
        _icones_frase = {
            "recarregar": icon_to_image(
                "arrows-rotate",
                fill=COR_PRIMARIA,
                scale_to_width=16
            ),
        }

    return _icones_frase


ICONES_TOAST = {
    "sucesso": "check",
    "erro": "exclamation",
}

_icones_toast = {}


def obter_icone_toast(tipo, cor):
    """Ícone do toast (check no sucesso, exclamação no erro), com cache."""

    chave = (tipo, cor)

    if chave not in _icones_toast:
        _icones_toast[chave] = icon_to_image(
            ICONES_TOAST.get(tipo, ICONES_TOAST["erro"]),
            fill=cor,
            scale_to_width=16
        )

    return _icones_toast[chave]