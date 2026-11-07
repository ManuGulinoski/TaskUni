from ctkfontawesome import icon_to_image

_icones = None

def criar_icones():

    global _icones

    if _icones is None:
        _icones = {
            "editar": icon_to_image(
                "pen",
                fill="#5b21b6",
                scale_to_width=16
            ),

            "excluir": icon_to_image(
                "trash",
                fill="#dc2626",
                scale_to_width=16
            ),

            "concluir": icon_to_image(
                "check",
                fill="#16a34a",
                scale_to_width=16
            )
        }

    return _icones