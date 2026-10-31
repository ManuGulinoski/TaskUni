"""
Leitura e gravação do arquivo JSON.

Responsável: Pessoa 2
Este é o ÚNICO arquivo do projeto que abre o dados.json.
Telas nunca chamam este arquivo diretamente: só os serviços.

Formato do JSON:
{
  "disciplinas": [{"id": "...", "nome": "Cálculo"}],
  "tarefas": [{"id": "...", "nome": "Lista 3", "tipo": "Exercício",
               "prazo": "2026-11-05", "disciplina_id": "...",
               "status": "A fazer", "descricao": "", "cor": null}]
}
"""
import json
import os

from models.disciplina import Disciplina
from models.tarefa import Tarefa
from utils.constantes import CAMINHO_DADOS


def carregar():
    """
    Lê o JSON e retorna uma tupla (lista_de_disciplinas, lista_de_tarefas),
    já convertidas em objetos Disciplina e Tarefa.

    Se o arquivo não existir ou estiver vazio, retorna ([], []).
    Dica: use os.path.exists, json.load(arquivo) e Disciplina.from_dict / Tarefa.from_dict.
    Abra com encoding="utf-8" por causa dos acentos.
    """
    if not os.path.exists(CAMINHO_DADOS):
        return [], []

    with open(CAMINHO_DADOS, "r", encoding="utf-8") as arquivo:
        conteudo = arquivo.read()

    if conteudo.strip() == "":
        return [], []

    dados = json.loads(conteudo)

    disciplinas = [Disciplina.from_dict(d) for d in dados.get("disciplinas", [])]
    tarefas = [Tarefa.from_dict(t) for t in dados.get("tarefas", [])]
    return disciplinas, tarefas


def salvar(disciplinas, tarefas):
    """
    Recebe as listas de objetos e grava tudo no JSON (sobrescreve o arquivo).
    Dica: json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    Crie a pasta 'dados' se ela não existir (os.makedirs(..., exist_ok=True)).
    """
    os.makedirs(os.path.dirname(CAMINHO_DADOS), exist_ok=True)

    dados = {
        "disciplinas": [d.to_dict() for d in disciplinas],
        "tarefas": [t.to_dict() for t in tarefas],
    }

    with open(CAMINHO_DADOS, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
