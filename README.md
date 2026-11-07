# TaskUni

Gerenciador de tarefas acadêmicas com interface gráfica desktop, feito em Python com Tkinter. Com ele você cadastra suas disciplinas, organiza provas, trabalhos e exercícios por prazo e acompanha o que está pendente, em andamento ou atrasado.

**Autores:** Ana Clara · Eduarda Tavares · Emanuele Gulinoski · Rebeca dos Santos

## Funcionalidades

- **Disciplinas**: cadastro de disciplinas com validação de nome vazio e de duplicidade (sem diferenciar maiúsculas/minúsculas).
- **Tarefas**: criação e edição com nome, tipo, disciplina, prazo, descrição, status e cor.
- **Tipos de tarefa**: Prova, Trabalho e Exercício.
- **Status**: A fazer, Em andamento, Concluída e Atrasada. Tarefas com prazo vencido e não concluídas são marcadas automaticamente como *Atrasada*.
- **Prioridade automática**, calculada pelos dias restantes até o prazo:

  | Prioridade | Prazo                     |
  |------------|---------------------------|
  | Urgente    | hoje ou já vencido        |
  | Alta       | de 1 a 3 dias             |
  | Média      | de 4 a 7 dias             |
  | Baixa      | 8 dias ou mais            |

- **Filtros**: por disciplina, tipo, status e prioridade, com botões *Filtrar* e *Limpar*. O serviço também suporta filtro por prazo (Hoje, Esta semana, Semana que vem).
- **Cards coloridos**: cada tarefa aparece em um card com faixa de cor personalizável (Branco, Azul, Verde, Amarelo, Vermelho, Roxo, Laranja), ordenados por prazo, com ícones de editar, excluir e concluir.
- **Notificações (toasts)** de sucesso e erro nos formulários.
- **Persistência local** em arquivo JSON, sem necessidade de banco de dados.

## Tecnologias

- Python 3.10+ (o projeto foi desenvolvido com Python 3.14)
- Tkinter / ttk (biblioteca padrão)
- [ctkfontawesome](https://pypi.org/project/ctkfontawesome/) para os ícones dos cards

## Como executar

1. Clone o repositório e entre na pasta:

   ```bash
   git clone <url-do-repositorio>
   cd TaskUni
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

   > No Linux, o Tkinter pode precisar ser instalado à parte (por exemplo, `sudo apt install python3-tk`).

3. Inicie o aplicativo:

   ```bash
   python main.py
   ```

## Como usar

1. Na tela inicial, clique em **+ Nova** e escolha **Disciplina** para cadastrar suas matérias.
2. Clique em **+ Nova → Tarefa** (ou em **+ Criar tarefa** na tela de tarefas) para registrar uma atividade.
3. Clique em **Ver tarefas** para acompanhar a lista, filtrar e editar tarefas pelo ícone de lápis.

O prazo deve ser informado no formato `DD/MM/AAAA` e não pode ser uma data passada. Limites de tamanho: nome da disciplina e da tarefa com até 50 caracteres, descrição com até 100.

## Estrutura do projeto

```
TaskUni/
├── main.py                  # Janela principal e navegação entre telas
├── requirements.txt         # Dependências do projeto
├── dados/
│   └── dados.json           # Armazenamento local (disciplinas e tarefas)
├── models/
│   ├── disciplina.py        # Classe Disciplina
│   └── tarefa.py            # Classe Tarefa (status, prazo e prioridade)
├── repositorio/
│   └── armazenamento.py     # Leitura e gravação do JSON
├── services/
│   ├── disciplina_service.py  # Regras de cadastro de disciplinas
│   ├── tarefa_service.py      # Validações, cadastro, edição e atraso
│   └── filtro_service.py      # Filtros de tarefas
├── interface/
│   ├── tela_tarefas.py      # Tela de listagem com filtros
│   ├── card_tarefa.py       # Card visual de cada tarefa
│   ├── modal_tarefa.py      # Formulário de criar/editar tarefa
│   └── modal_disciplina.py  # Formulário de nova disciplina
├── utils/
│   ├── constantes.py        # Constantes, cores e textos
│   └── icones.py            # Ícones da interface
└── testes/
    └── abrir_tela_tarefas.py    # Abre só a tela de tarefas
```

O código segue uma separação em camadas: **interface** (telas), **services** (regras de negócio), **models** (entidades) e **repositorio** (persistência).

## Formato dos dados

Os dados ficam em `dados/dados.json`:

```json
{
  "disciplinas": [
    { "id": "uuid", "nome": "Matemática" }
  ],
  "tarefas": [
    {
      "id": "uuid",
      "nome": "Lista de exercícios",
      "tipo": "Exercício",
      "prazo": "2026-12-18",
      "disciplina_id": "uuid",
      "status": "A fazer",
      "descricao": "",
      "cor": "Azul"
    }
  ]
}
```