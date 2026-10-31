"""
Constantes usadas em todo o projeto.

Responsável: Pessoa 2
REGRA: ninguém digita "Prova", "A fazer" etc. direto no código.
Sempre importe daqui:  from utils.constantes import TIPOS, STATUS ...
"""

import os

# ---------- Arquivo de dados ----------
# Caminho absoluto, montado a partir da pasta do projeto. Assim funciona
# mesmo se alguém rodar o main.py pelo botão "Run" do VS Code de outra pasta.
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS = os.path.join(PASTA_PROJETO, "dados", "dados.json")

# ---------- Limites de caracteres ----------
MAX_NOME_DISCIPLINA = 50
MAX_NOME_TAREFA = 50
MAX_DESCRICAO_TAREFA = 100

# ---------- Tipos de tarefa ----------
TIPO_PROVA = "Prova"
TIPO_TRABALHO = "Trabalho"
TIPO_EXERCICIO = "Exercício"
TIPOS = [TIPO_PROVA, TIPO_TRABALHO, TIPO_EXERCICIO]

# ---------- Status ----------
# Os 3 primeiros o usuário escolhe. "Atrasada" é calculado automaticamente
# e NUNCA é salvo no JSON.
STATUS_A_FAZER = "A fazer"
STATUS_EM_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluída"
STATUS_ATRASADA = "Atrasada"

STATUS_SELECIONAVEIS = [STATUS_A_FAZER, STATUS_EM_ANDAMENTO, STATUS_CONCLUIDA]
STATUS_TODOS = STATUS_SELECIONAVEIS + [STATUS_ATRASADA]

# ---------- Prioridade (calculada pelo prazo) ----------
PRIORIDADE_URGENTE = "Urgente"   # 0 dias (entrega hoje)
PRIORIDADE_ALTA = "Alta"         # 1 a 3 dias
PRIORIDADE_MEDIA = "Média"       # 4 a 7 dias
PRIORIDADE_BAIXA = "Baixa"       # 8 dias ou mais
PRIORIDADES = [PRIORIDADE_URGENTE, PRIORIDADE_ALTA, PRIORIDADE_MEDIA, PRIORIDADE_BAIXA]

# ---------- Filtro de prazo ----------
PRAZO_HOJE = "Hoje"
PRAZO_ESTA_SEMANA = "Esta semana"
PRAZO_SEMANA_QUE_VEM = "Semana que vem"
FILTROS_PRAZO = [PRAZO_HOJE, PRAZO_ESTA_SEMANA, PRAZO_SEMANA_QUE_VEM]

# Opção "sem filtro" usada nos Combobox de filtro
OPCAO_TODOS = "Todos"

# ---------- Datas ----------
FORMATO_DATA_JSON = "%Y-%m-%d"   # como a data é salva no JSON
FORMATO_DATA_TELA = "%d/%m/%Y"   # como a data aparece para o usuário

# ---------- Cores da tarefa (campo opcional) ----------
CORES_TAREFA = {
    "Nenhuma": None,
    "Azul": "#378ADD",
    "Verde": "#639922",
    "Amarelo": "#EF9F27",
    "Vermelho": "#E24B4A",
    "Roxo": "#7F77DD",
}

# ---------- Visual da interface ----------
COR_MENU_LATERAL = "#1F2937"
COR_MENU_TEXTO = "#FFFFFF"
COR_FUNDO = "#F3F4F6"
LARGURA_MENU = 180
TAMANHO_JANELA = "1100x700"
TITULO_APP = "Gerenciador de Tarefas Acadêmicas"

# ---------- API ----------
URL_ZENQUOTES = "https://zenquotes.io/api/random"
FRASE_RESERVA = ("O sucesso é a soma de pequenos esforços repetidos dia após dia.",
                 "Robert Collier")
