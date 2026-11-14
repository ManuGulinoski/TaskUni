import os


# ============================================================
# CONFIGURAÇÕES GERAIS DO PROJETO
# ============================================================

# Arquivo de dados
PASTA_PROJETO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAMINHO_DADOS = os.path.join(PASTA_PROJETO, "dados", "dados.json")

# Datas
FORMATO_DATA_JSON = "%Y-%m-%d"
FORMATO_DATA_TELA = "%d/%m/%Y"


# ============================================================
# DISCIPLINAS
# ============================================================

# Limites de caracteres
MAX_NOME_DISCIPLINA = 50


# ============================================================
# TAREFAS
# ============================================================

# Limites de caracteres
MAX_NOME_TAREFA = 50
MAX_DESCRICAO_TAREFA = 100

# Tipos de tarefa
TIPO_PROVA = "Prova"
TIPO_TRABALHO = "Trabalho"
TIPO_EXERCICIO = "Exercício"

TIPOS = [
    TIPO_PROVA,
    TIPO_TRABALHO,
    TIPO_EXERCICIO
]

# Status das tarefas
STATUS_A_FAZER = "A fazer"
STATUS_EM_ANDAMENTO = "Em andamento"
STATUS_CONCLUIDA = "Concluída"
STATUS_ATRASADA = "Atrasada"

STATUS_SELECIONAVEIS = [
    STATUS_A_FAZER,
    STATUS_EM_ANDAMENTO,
    STATUS_CONCLUIDA
]

STATUS_TODOS = STATUS_SELECIONAVEIS + [STATUS_ATRASADA]

# Prioridades (calculadas pelo prazo)
PRIORIDADE_URGENTE = "Urgente"  # 0 dias
PRIORIDADE_ALTA = "Alta"        # 1 a 3 dias
PRIORIDADE_MEDIA = "Média"      # 4 a 7 dias
PRIORIDADE_BAIXA = "Baixa"      # 8 dias ou mais

PRIORIDADES = [
    PRIORIDADE_URGENTE,
    PRIORIDADE_ALTA,
    PRIORIDADE_MEDIA,
    PRIORIDADE_BAIXA
]

# Filtros de prazo
PRAZO_HOJE = "Hoje"
PRAZO_ESTA_SEMANA = "Esta semana"
PRAZO_SEMANA_QUE_VEM = "Semana que vem"

FILTROS_PRAZO = [
    PRAZO_HOJE,
    PRAZO_ESTA_SEMANA,
    PRAZO_SEMANA_QUE_VEM
]

# Opções gerais dos filtros
OPCAO_TODOS = "Todos"
OPCAO_TODAS = "Todas"

# Cores das tarefas (faixa lateral do card) - tons pastel
# Os NOMES ficam salvos no JSON; só os tons mudaram.
CORES_TAREFA = {
    "Branco": "#FFFFFF",
    "Azul": "#8EC1F0",
    "Verde": "#9FD8A8",
    "Amarelo": "#FFD77A",
    "Vermelho": "#FF9A9A",
    "Roxo": "#B9A3EE",
    "Laranja": "#FFB38A"
}


# ============================================================
# INTERFACE GRÁFICA - TEMA "FOFO" (tons pastel)
# Todas as cores e fontes das telas ficam AQUI.
# Para mudar o visual do app inteiro, basta mexer nesta seção.
# ============================================================

# Janela principal
TAMANHO_JANELA = "1100x700"
TAMANHO_MINIMO = (1100, 700)
TITULO_APP = "Gerenciador de Tarefas Acadêmicas"

# ---------- Fontes ----------
FONTE = "Segoe UI"
FONTE_TITULO = (FONTE, 20, "bold")
FONTE_SUBTITULO = (FONTE, 11)
FONTE_TEXTO = (FONTE, 10)
FONTE_LABEL = (FONTE, 10, "bold")
FONTE_BOTAO = (FONTE, 10, "bold")
FONTE_PILULA = (FONTE, 9, "bold")

# ---------- Cores gerais ----------
COR_FUNDO = "#FFF8F3"            # creme bem clarinho
COR_SUPERFICIE = "#FFFFFF"       # cards, modais, gráficos
COR_BORDA = "#EFE6F5"            # bordas suaves
COR_OVERLAY = "#E9E0F2"          # fundo atrás dos modais

COR_TEXTO = "#4A4058"            # roxo-acinzentado escuro (mais suave que preto)
COR_TEXTO_SECUNDARIO = "#766A8A"
COR_TEXTO_LABEL = "#5B4A7A"
COR_TEXTO_MENSAGEM = "#766A8A"

# Botão principal (lilás)
COR_PRIMARIA = "#7C5CC4"
COR_PRIMARIA_HOVER = "#6A4BB3"
COR_TEXTO_PRIMARIA = "#FFFFFF"

# Botão suave (lilás clarinho, ex.: Filtrar, Ver detalhes)
COR_SUAVE = "#EFE7FA"
COR_SUAVE_HOVER = "#E3D7F6"
COR_TEXTO_SUAVE = "#6346B0"

# Botão secundário (ex.: Cancelar, Início, Limpar)
COR_SECUNDARIA = "#F4F0F8"
COR_SECUNDARIA_HOVER = "#E9E2F1"
COR_TEXTO_SECUNDARIA = "#5B4A7A"

# Botão de perigo (ex.: Excluir)
COR_PERIGO = "#C2414B"
COR_PERIGO_HOVER = "#A8333D"
COR_TEXTO_PERIGO = "#FFFFFF"

# Nomes usados pela equipe nos botões (apontam para o tema)
COR_BOTAO_PRINCIPAL = COR_PRIMARIA
COR_BOTAO_HOVER = COR_PRIMARIA_HOVER
COR_TEXTO_BOTAO = COR_TEXTO_PRIMARIA

# Campos de formulário
COR_CAMPO = "#FAF7FD"
COR_CAMPO_BORDA = "#E3D8F0"
COR_CAMPO_FOCO = COR_PRIMARIA
COR_PLACEHOLDER = "#9C92AC"

# ---------- Menu lateral ----------
COR_MENU_LATERAL = COR_SUPERFICIE     # menu branquinho
COR_MENU_TEXTO = "#6E6283"
COR_MENU_TEXTO_ATIVO = COR_TEXTO_SUAVE
COR_MENU_ATIVO = COR_SUAVE            # item selecionado (pílula lilás)
COR_MENU_HOVER = COR_SECUNDARIA
COR_MENU_LOGO = COR_PRIMARIA
LARGURA_MENU = 200

# ---------- Cards de números (Home) ----------
# título -> (cor do número, cor da bolinha de destaque)
CORES_BIG_NUMBER = {
    "Total de tarefas": ("#6346B0", "#C3B1F0"),
    "Concluídas": ("#1F6B52", "#9ED9BF"),
    "Pendentes": ("#1F5F8B", "#A7C7E7"),
    "Atrasadas": ("#B3261E", "#FF9E9E"),
}

# ---------- Cards de tarefas ----------
COR_CARD = COR_SUPERFICIE
COR_NEUTRA = "#E9E2F1"           # faixa quando a cor é "Branco"
COR_ATRASADA = "#B3261E"
COR_CONCLUIDA = "#1F6B52"
CORES_PADRAO = ("Branco", "Padrão")

# Pílulas de status: status -> (fundo, texto)
CORES_PILULA_STATUS = {
    "A fazer": ("#DCEBFA", "#1F5F8B"),       # azul bebê
    "Em andamento": ("#FFEBD2", "#8A5300"),  # pêssego
    "Concluída": ("#D7F3E7", "#1F6B52"),     # menta
    "Atrasada": ("#FFE1E1", "#B3261E"),      # rosa-coral
}
COR_PILULA_PADRAO = ("#F3EDFA", "#4A4058")   # prioridade e status desconhecido

# Ícones dos cards (editar, excluir, concluir)
COR_ICONE_EDITAR = "#7C5CC4"
COR_ICONE_EXCLUIR = "#E0707A"
COR_ICONE_CONCLUIR = "#3FA586"

# ---------- Gráficos (barras pastel) ----------
CORES_GRAFICO_STATUS = {
    "A fazer": "#A7C7E7",
    "Em andamento": "#FFCF99",
    "Concluída": "#9ED9BF",
    "Atrasada": "#FF9E9E",
}
CORES_GRAFICO_TIPO = {
    "Prova": "#C3B1F0",
    "Trabalho": "#FFB5C8",
    "Exercício": "#A8E0E0",
}
COR_GRAFICO_EIXO = "#E3D8F0"
COR_GRAFICO_PADRAO = "#D6CCE4"

# ---------- Notificações (toasts): tipo -> (fundo, texto, borda) ----------
COR_TOAST_FUNDO = "#FFFFFF"
COR_TOAST_TEXTO = "#000000"

CORES_TOAST_BARRA = {
    "sucesso": "#2E9E5B",
    "erro": "#D64545",
}

# ---------- Mensagens simpáticas ----------
MSG_SEM_TAREFAS = "Nenhuma tarefa por aqui ainda ✿\nClique em “+ Criar tarefa” para começar!"
MSG_SEM_RESULTADO = "Nenhuma tarefa com esses filtros ♡\nTente mudar ou limpar os filtros."
MSG_GRAFICO_VAZIO = "Ainda não há tarefas para mostrar ✿\nCadastre uma tarefa e volte aqui!"

# ============================================================
# API E FRASES
# ============================================================

FRASE_RESERVA = (
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Robert Collier"
)

URL_ZENQUOTES = "https://zenquotes.io/api/random"