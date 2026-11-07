
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

# Cores das tarefas
CORES_TAREFA = {
    "Branco": "#FFFFFF",
    "Azul": "#378ADD",
    "Verde": "#639922",
    "Amarelo": "#EF9F27",
    "Vermelho": "#E24B4A",
    "Roxo": "#7F77DD",
    "Laranja": "#E06C26"
}


# ============================================================
# INTERFACE GRÁFICA
# ============================================================

# Menu lateral
COR_MENU_LATERAL = "#1F2937"
COR_MENU_TEXTO = "#FFFFFF"
LARGURA_MENU = 180

# Cores gerais
COR_FUNDO = "#F3F4F6"

# Janela principal
TAMANHO_JANELA = "1100x700"
TITULO_APP = "Gerenciador de Tarefas Acadêmicas"

# ---------- Cards de tarefas ----------

FONTE = "Segoe UI"

COR_CARD = "white"
COR_BORDA = "#E5E7EB"

COR_TEXTO = "#111827"
COR_TEXTO_SECUNDARIO = "#6B7280"

COR_NEUTRA = "#D1D5DB"
COR_ATRASADA = "#DC2626"
COR_CONCLUIDA = "#16A34A"

CORES_PADRAO = ("Branco", "Padrão")

# ---------- Tela de tarefas ----------
COR_TEXTO_LABEL = "#374151"
COR_TEXTO_MENSAGEM = "#6B7280"

MSG_SEM_TAREFAS = "Nenhuma tarefa cadastrada."
MSG_SEM_RESULTADO = "Nenhuma tarefa encontrada para os filtros selecionados."

# ============================================================
# API E FRASES
# ============================================================

FRASE_RESERVA = (
    "O sucesso é a soma de pequenos esforços repetidos dia após dia.",
    "Robert Collier"
)