from ctkfontawesome import icon_to_image

from utils.constantes import (
    COR_ICONE_EDITAR,
    COR_ICONE_EXCLUIR,
    COR_ICONE_CONCLUIR
)

_icones = None

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