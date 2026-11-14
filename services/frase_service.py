import requests

from utils.constantes import FRASE_RESERVA, URL_ZENQUOTES


def buscar_frase():
    try:
        resposta = requests.get(
            URL_ZENQUOTES,
            timeout=5
        )

        resposta.raise_for_status()

        dados = resposta.json()

        if not isinstance(dados, list) or not dados:
            return FRASE_RESERVA

        frase = dados[0].get("q")
        autor = dados[0].get("a")

        if not frase or not autor:
            return FRASE_RESERVA

        # Mensagem de limite de requisições da API, não é uma frase de verdade
        if autor == "zenquotes.io":
            return FRASE_RESERVA

        return frase, autor

    except (requests.RequestException, ValueError, TypeError, KeyError, AttributeError):
        return FRASE_RESERVA