from models.disciplina import Disciplina
from repositorio import armazenamento
from utils.constantes import MAX_NOME_DISCIPLINA

def verifica_tam_disciplina(nome):
    if len(nome) > MAX_NOME_DISCIPLINA:
        return False
    else:
        return True

def cadastrar_disciplina(nome):
    nome = nome.strip()

    if not nome:
        raise ValueError("O campo 'Nome da disciplina' deve ser preenchido!")
    
    
    disciplinas, tarefas = armazenamento.carregar()     
    for disciplina in disciplinas:
        if disciplina.nome.lower() == nome.lower():
            raise ValueError("Essa disciplina já está cadastrada!")

    nova_disciplina = Disciplina(nome)
    disciplinas.append(nova_disciplina)
    armazenamento.salvar(disciplinas, tarefas)
    return nova_disciplina