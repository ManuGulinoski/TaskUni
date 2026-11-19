from models.disciplina import Disciplina
from repositorio import armazenamento
from utils.constantes import MAX_NOME_DISCIPLINA


def verifica_tam_disciplina(nome):
    if len(nome) > MAX_NOME_DISCIPLINA:
        return False
    else:
        return True


def _validar_nome_disciplina(nome, disciplinas, ignorar_id=None):
    """Regras comuns ao cadastro e à edição de disciplina."""
    nome = nome.strip()

    if not nome:
        raise ValueError("O campo 'Nome da disciplina' deve ser preenchido!")

    if not verifica_tam_disciplina(nome):
        raise ValueError(
            f"O nome da disciplina deve ter no máximo "
            f"{MAX_NOME_DISCIPLINA} caracteres."
        )

    for disciplina in disciplinas:
        if disciplina.id == ignorar_id:
            continue
        if disciplina.nome.lower() == nome.lower():
            raise ValueError("Essa disciplina já está cadastrada!")

    return nome


def listar_disciplinas():
    """Retorna as disciplinas em ordem alfabética."""
    disciplinas, _ = armazenamento.carregar()
    return sorted(disciplinas, key=lambda d: d.nome.lower())


def cadastrar_disciplina(nome):
    disciplinas, tarefas = armazenamento.carregar()

    nome = _validar_nome_disciplina(nome, disciplinas)

    nova_disciplina = Disciplina(nome)
    disciplinas.append(nova_disciplina)
    armazenamento.salvar(disciplinas, tarefas)
    return nova_disciplina


# US05 - Editar disciplina
def editar_disciplina(disciplina_id, novo_nome):
    """
    Troca o nome da disciplina. As tarefas guardam o ID da disciplina,
    então continuam ligadas a ela sem precisar mudar nada.
    """
    disciplinas, tarefas = armazenamento.carregar()

    disciplina = next(
        (d for d in disciplinas if d.id == disciplina_id),
        None
    )

    if disciplina is None:
        raise ValueError("Escolha a disciplina que deseja editar.")

    disciplina.nome = _validar_nome_disciplina(
        novo_nome, disciplinas, ignorar_id=disciplina_id
    )

    armazenamento.salvar(disciplinas, tarefas)
    return disciplina