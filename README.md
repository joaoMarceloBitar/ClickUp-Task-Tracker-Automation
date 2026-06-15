# Desafio Técnico - Automação & IA (Brio Lab)

Este repositório contém a resolução do desafio prático para a vaga de Desenvolvedor(a) de Automação & IA. O projeto simula demandas reais de orquestração de fluxos com n8n e tratamento de dados em backend com Python.

## 📁 Estrutura do Repositório

```text
DESAFIOTECNICO/
├── n8n/
│   ├── workflow.json        # JSON exportado do workflow n8n
│   └── screenshots/         # Prints das execuções e do fluxo montado
├── python/
│   ├── app/
│   │   ├── clickup.py       # Integração/simulação com a API do ClickUp
│   │   ├── database.py      # Conexão e persistência (Supabase/SQLite)
│   │   ├── main.py          # Arquivo principal (validação e fluxo de dados)
│   │   └── schemas.py       # Modelos de dados e validação
│   ├── requirements.txt     # Dependências isoladas do ambiente Python
│   └── venv/                # Ambiente virtual (ignorado no Git)
├── .gitignore               # Configurações de arquivos ocultos
└── README.md                # Documentação do projeto (este arquivo)
```

## 🐍 1. Configurando o Backend (Python)

O código Python utiliza um ambiente virtual (`venv`) para isolar as dependências e garantir que o projeto rode sem conflitos globais de versão na sua máquina.

### 1. Navegação e Inicialização
Abra o seu terminal na raiz do projeto e mude para o diretório onde o código Python e o ambiente virtual estão localizados:
```bash
cd python
```

### 2. Criação do Ambiente Virtual
Caso o ambiente virtual ainda não tenha sido gerado no diretório, crie-o executando o comando correspondente ao seu sistema:
```bash
python -m venv venv
```

### 3. Ativação da Virtual Environment (venv)
Ative o ambiente para garantir que os pacotes sejam instalados e executados de forma isolada:

* **No Windows (CMD/PowerShell):**
  ```bash
  .\venv\Scripts\activate
  ```
* **No Linux/macOS:**
  ```bash
  source venv/bin/activate
  ```
> *(Você saberá que a venv foi ativada com sucesso quando o prefixo `(venv)` aparecer no início da linha de comando do seu terminal).*

### 4. Instalação das Dependências
Com a venv devidamente ativada, instale todas as bibliotecas necessárias para o projeto através do arquivo de requerimentos:
```bash
pip install -r requirements.txt
```

### 5. Configuração de Variáveis de Ambiente
1. Vá até a raiz da pasta `python/` e crie um arquivo local nomeado exatamente como `.env`.
2. Abra o arquivo `.env.example` disponível no projeto, copie a estrutura de chaves de exemplo e cole-a no seu novo `.env`.
3. Preencha as chaves com os seus tokens e credenciais locais de teste do Supabase e do ClickUp.

### 6. Execução do Script
Para rodar a aplicação, realizar as validações de dados e disparar o fluxo integrado, execute o arquivo principal a partir do diretório raiz do Python:
```bash
python app/main.py
```

## ⚙️ Configurando o Workflow (n8n)

Para visualizar, editar e testar a orquestração de fluxo solicitada no **Desafio 1**, você pode importar o arquivo JSON do workflow diretamente para a sua instância do n8n seguindo os passos abaixo:

### 1. Inicialização do Ambiente
Certifique-se de que sua instância local do n8n está ativa. Se estiver rodando via terminal, utilize o comando padrão do seu ambiente:
```bash
n8n start
```

### 2. Importando o Workflow JSON
1. No painel lateral esquerdo do n8n, navegue até **Workflows** e clique em **Add Workflow** (ou abra uma tela de fluxo em branco).
2. No canto superior direito da tela de edição, clique no ícone de três pontinhos (`...`).
3. No menu suspenso, seleciona a opção **Import from File**.
4. Navegue pelas pastas do seu computador e selecione o arquivo correspondente neste repositório:
   ```text
   n8n/workflow.json
   ```

### 3. Configuração de Credenciais Locais
Com o fluxo carregado na sua tela, você precisará associar suas próprias chaves de teste para que os nós consigam se comunicar com as plataformas:

* **Nó do ClickUp:** Dê um duplo clique no nó de trigger/leitura do ClickUp, vá na seção de credenciais e adicione o seu token de teste da API.
* **Nó do Supabase:** Dê um duplo clique no nó do Supabase. 

### 4. Execução do Teste
1. Clique no botão **Save** no canto superior direito para salvar as alterações de credenciais.
2. Certifique-se de que as tabelas necessárias estejam criadas no seu banco de dados.
3. Clique em **Execute Workflow** na barra inferior para colocar o fluxo em modo de escuta ou rodar o payload de teste criado.

## Executando o fluxo n8n
```text
O fluxo consiste em um trigger que gera hashtags para posts já aprovados na task list do ClickUp, armazena os dados em um banco de dados Supabase, e notifica o processo por e-mail.
```

### 🗺️ Como Funciona o Fluxo de Automação (Nó por Nó)

Abaixo está a mapeação e explicação detalhada com base no esquema estrutural exato do arquivo JSON desenvolvido para o projeto:

#### 1. Schedule Trigger
* **O que faz:** Acorda e inicia o fluxo de automação ativamente de forma recorrente.
* **Configuração:** Está definido para rodar a cada **2 minutos** (`minutesInterval: 2`), garantindo uma checagem ágil sem sobrecarregar os servidores.

#### 2. Get many tasks (ClickUp Node)
* **O que faz:** Conecta-se à API do ClickUp utilizando o token seguro e faz uma varredura para buscar uma coleção de tarefas dentro da lista especificada do cliente (`list: "901714433814"`).
* **Dados capturados:** Extrai metadados estruturados de cada card de postagem, incluindo o título do post (`name`) e o corpo do texto de legenda (`description`).

#### 3. Filter Node
* **O que faz:** Filtra a lista de tarefas trazidas pelo ClickUp aplicando uma regra lógica condicional estrita.
* **Condição:** Avalia a expressão `{{ $json.status.status }}`, permitindo que **apenas** os itens cujo status seja textualmente igual a `"aprovado"` avancem no fluxo principal.

#### 4. Message a model (Advanced AI - Google Gemini)
* **O que faz:** Aciona o LLM integrado utilizando o modelo `gemini-2.5-flash` para processar a legenda.
* **Engenharia de Prompt:** O nó envia um prompt sistêmico injetando dinamicamente a legenda coletada (`{{$json.description}}`), instruindo o modelo a agir como especialista em Instagram e retornar exatamente 15 hashtags estratégicas.

#### 5. Merge Node
* **O que faz:** Atua como um consolidador de escopos paralelos no fluxo, operando no modo de combinação por posição (`combineByPosition`).
* **Conexões:** Ele recebe na entrada `Input 1` o payload original do post filtrado do ClickUp e na entrada `Input 0` a resposta isolada de texto da Inteligência Artificial, unificando as duas ramificações.

#### 6. Edit Fields (Set Node)
* **O que faz:** Atua como a camada crucial de tratamento e normalização de dados utilizando sintaxe estruturada bruta (`mode: "raw"`).
* **Mapeamento JSON:** Ele limpa o objeto combinado e gera um JSON enxuto mapeando o nome da tarefa para `titulo`, a legenda para `descricao` e limpando a árvore de nós da resposta do Gemini para extrair puramente as strings de tags:
  ```json
  {
    "titulo": "{{ $json.name }}",
    "descricao": "{{ $json.description }}",
    "hashtags": {{ $json.content.parts[0].text }}
  }

#### 7. Create a row (Supabase Node)
* **O que faz:** Conecta-se à API do Supabase e realiza uma operação de inserção (`Insert`) na tabela de dados alvo configurada (`tableId: "postCliente"`).
* **Mapeamento de Linha:** Alimenta as colunas do banco mapeando `nome` com o título tratado, `legenda` com a descrição original e `tags` com as hashtags geradas pela IA.

#### 8. Send a message (Gmail Node)
* **O que faz:** Dispara uma notificação ativa de e-mail automatizada ao final da execução com sucesso para o endereço comercial configurado.
* **Corpo do E-mail:** Injeta dinamicamente as variáveis de persistência confirmando o encerramento do processo: *"O post agendado: {{ $json.nome }} com as hashtags: {{ $json.tags }} está aprovado!"*.

## 🐍 Execução da API Backend (FastAPI)

A API foi desenvolvida utilizando o framework **FastAPI** para atuar como uma camada intermediária blindada entre o formulário web e as ferramentas externas. Ela intercepta os dados brutos, aplica regras estritas de quarentena e higienização, e distribui as informações limpas simultaneamente para o banco de dados e para a esteira comercial.

---

### 🎛️ Fluxo e Arquitetura de Código

A aplicação foi isolada em módulos coesos dentro do diretório `python/app/` para garantir manutenibilidade e escalabilidade do backend:

* **`main.py` (Orquestrador do Serviço):** Inicializa o servidor FastAPI e expõe as rotas da aplicação. Ele gerencia o ciclo completo do ciclo de requisição-resposta do endpoint principal.
* **`schemas.py` (Camada Quarentena & Limpeza):** Define os contratos de entrada de dados baseados em tipagem forte e esquemas do Pydantic, executando sanitizações nativas regex em tempo de execução.
* **`database.py` (Persistência Centralizada):** Inicializa o cliente oficial SDK do Supabase e encapsula as instruções de mutação e inserção na tabela relacional.
* **`clickup.py` (Sincronizador de CRM):** Consome a API REST nativa do ClickUp via requisições HTTP para converter os leads qualificados em tarefas estruturadas na esteira comercial.

---

### 🗺️ Como Funciona o Processamento (Passo a Passo)

```text
[Requisição HTTP POST] 
       │
       ▼
┌──────────────────────────────┐
│  1. Validação Pydantic       │ ◄── Se falhar: Retorna 422 Unprocessable Entity
└──────────────┬───────────────┘
       │ (Dado Sanitizado)
       ▼
┌──────────────────────────────┐
│  2. Tratamento & Sanitização │ ◄── Limpeza de espaços, Title Case e RegExp
└──────────────┬───────────────┘
       │ (Payload Limpa)
       ▼
┌──────────────┴───────────────┐
│  3. Execução do Endpoint     │
└──────┬────────────────┬──────┘
       │                │
       ▼ (Paralelo)     ▼ (Paralelo)
┌──────────────┐┌──────────────┐
│   Supabase   ││   ClickUp    │
│ (Insert Row) ││ (Create Task)│
└──────────────┘└──────────────┘
```

# Fluxo da Aplicação

## 1. Recepção e Sanitização Estrita (`schemas.py`)

Assim que a payload atinge o endpoint `POST /webhook/diagnostico`, o Pydantic entra em ação como o guardião dos dados.

### nome
- Passa por remoção de espaçamentos duplicados.
- É padronizado para **Title Case** (primeiras letras maiúsculas).

### email
- Validado por expressão regular estrita ao nível de domínio.
- Espaços residuais nas extremidades são removidos através de `.strip()`.

### telefone
- Aplica uma limpeza via Regex removendo todos os caracteres não numéricos (`\D`).
- Valida se o número contém entre **10 e 11 dígitos**, incluindo o DDD.
- Caso a validação falhe, a requisição é rejeitada e um `ValueError` é lançado.
- Se válido, o telefone é formatado para um padrão legível:
  - `(XX) XXXXX-XXXX`
  - `(XX) XXXX-XXXX`

### especialidade e principal_desafio
- São sanitizados contra quebras de linha.
- Espaços duplicados são removidos.
- O texto é formatado em estilo frase utilizando `capitalize()`.

---

## 2. Persistência de Dados (`database.py`)

Com o objeto `DiagnosticoLead` totalmente validado e livre de inconsistências que possam comprometer integrações posteriores, a API aciona a função `salvar_lead()`.

O módulo utiliza o SDK oficial do Supabase para inserir uma nova linha na tabela `diagnosticoCliente`.

A operação é encapsulada em um bloco `try/except`, garantindo que eventuais falhas de comunicação com o banco de dados sejam tratadas adequadamente sem comprometer a estabilidade da aplicação.

---

## 3. Geração de Demanda Comercial (`clickup.py`)

Após a persistência bem-sucedida dos dados no banco, a função `criar_tarefa()` é executada.

Utilizando variáveis de ambiente carregadas a partir do arquivo `.env`, o sistema recupera de forma segura:

- Token de autenticação da API do ClickUp.
- ID da lista de destino.

Em seguida, uma requisição HTTP é enviada para o endpoint:

```http
POST /api/v2/list/{LIST_ID}/task
```

A tarefa é criada dinamicamente contendo:

### Título padronizado

```text
Lead - {nome}
```

### Descrição estruturada

- Nome
- Telefone
- E-mail
- Especialidade
- Principal desafio

Essas informações são organizadas em um formato legível para permitir que a equipe comercial inicie o atendimento imediatamente.

---

## 4. Resposta Unificada

Se todas as etapas forem concluídas com sucesso, a API retorna uma resposta consolidada contendo o resultado das integrações executadas.

### Exemplo de resposta

```json
{
  "status": "sucesso",
  "supabase": {
    "id": 11,
    "nome": "João Duarte"
  },
  "clickup": {
    "id": "86abc123",
    "name": "Lead - João Duarte"
  }
}
```

A resposta é enviada com código HTTP `200 OK`, indicando que o lead foi validado, persistido no banco de dados e transformado em uma tarefa operacional dentro do ClickUp.

```json
{
  "status": "sucesso",
  "supabase": {
    "id": 11,
    "nome": "João Duarte"
  },
  "clickup": {
    "id": "86abc123",
    "name": "Lead - João Duarte"
  }
}
```
### 🛸 Contrato do Endpoint API (Payloads de Exemplo)

#### Requisição Esperada
* **Endpoint:** `POST /webhook/diagnostico`
* **Content-Type:** `application/json`

```json
{
  "nome": "   joão   silva  ",
  "telefone": "53991234567",
  "email": "joao.silva@ufpel.edu.br",
  "especialidade": "advogado criminalista",
  "principal_desafio": "falta de captação de leads qualificados no portal."
}
```

#### Resposta Sanitizada e Processada (JSON Output)
Note como o backend higienizou e formatou todos os campos antes de salvar no Supabase e enviar ao ClickUp:

```json
{
  "status": "sucesso",
  "supabase": {
    "data": [
      {
        "nome": "João Silva",
        "telefone": "(53) 99123-4567",
        "email": "joao.silva@ufpel.edu.br",
        "especialidade": "Advogado criminalista",
        "principal_desafio": "Falta de captação de leads qualificados no portal."
      }
    ]
  },
  "clickup": {
    "id": "862jm7abc",
    "name": "Lead - João Silva",
    "description": "\nNome: João Silva\nTelefone: (53) 99123-4567\nEmail: joao.silva@ufpel.edu.br\nEspecialidade: Advogado criminalista\n\nDesafio:\nFalta de captação de leads qualificados no portal.\n"
  }
}
```
## 🧠 Decisões de Projeto

Abaixo estão fundamentadas todas as escolhas de arquitetura, frameworks e bibliotecas utilizadas no desenvolvimento do backend, visando atender aos critérios de resiliência, governança de dados e manutenibilidade exigidos no ecossistema da Brio Lab.

---

#### 🚀 Por que FastAPI?

* **FastAPI:** A escolha pelo framework foi baseada principalmente em critérios de domínio e popularidade no mercado, visando uma manutenção mais tranquila para outros funcionários que trabalharem no código, além de usufruir dos recursos nativos de autodocumentação, validação e tipagem forte.
---

#### pydantic
* **Justificativa:** Utilizado para construir o contrato de dados (`DiagnosticoLead`) do formulário. Forneceu a infraestrutura necessária para aplicar os decoradores `@field_validator`, permitindo higienizar strings, interceptar payloads malformatados em tempo de execução e aplicar máscaras customizadas aos dados antes que eles atinjam o banco de dados.

#### 🏢 Alinhamento com a Infraestrutura e Cultura da Empresa

A escolha do **Supabase** e do **ClickUp** visa aproximar o projeto do ecossistema real e do dia a dia de trabalho da Brio Lab:

## 🔮 Melhorias Futuras

Com o objetivo de escalabilidade, autonomia e otimização do ecossistema da Brio Lab, foram mapeadas as seguintes propostas de evolução para o fluxo do n8n:

### Para o fluxo n8n

#### 📅 1. Geração de Cronograma Inteligente e Automatizado
* **Como funcionaria:** O fluxo deixaria de apenas processar posts individualmente e passaria a gerar calendários editoriais completos de forma preditiva.
* **Inteligência aplicada:** Cruzando os dados cadastrais do cliente, a IA identificaria datas comemorativas e sazonais altamente relevantes para o nicho dele. O n8n calcularia a distribuição ideal das postagens respeitando estritamente a frequência e a quantidade de posts contratada no plano do cliente, populando a esteira do ClickUp de forma automática no início de cada mês.

#### 🚀 2. Publicação Direta e Automatizada no Instagram (Trigger por Campo)
* **Como funcionaria:** Implementação de um webhook dinâmico ou nó de escuta focado no campo personalizado `"conteúdo"` dentro da tarefa do ClickUp.
* **Automação de ponta a ponta:** Assim que o designer/criativo anexasse a mídia final e preenchesse esse campo na task aprovada, o n8n interceptaria o gatilho imediatamente. O fluxo enviaria o arquivo e a legenda tratada direto para a API da Graph do Instagram (via Facebook Developer), realizando o agendamento ou a publicação imediata na rede social, eliminando totalmente o processo de postagem manual.

### Para a API

#### 📈 1. Rate Limiting (Limitador de Requisições)
* **O problema atual:** Ataques de força bruta ou robôs maliciosos podem inundar a API com milhares de requisições por minuto, estourando a cota de uso das chaves do ClickUp e gerando cobranças indevidas no Supabase.
* **A melhoria:** Integrar a biblioteca **`slowapi`** para aplicar *Rate Limiting* baseado no IP do cliente (ex: no máximo 5 requisições por minuto por usuário). Se o limite for excedido, a API bloqueia o atacante retornando `HTTP 429 Too Many Requests`.

#### 📊 4. Dashboard de Métricas de Leads (Rotas de Analytics)
* **A melhoria:** Criar rotas protegidas adicionais (ex: `GET /analytics/leads`) que realizam queries agregadas no Supabase para expor métricas em tempo real.
* **O benefício:** Permitiria extrair dados estruturados como as especialidades mais comuns que estão preenchendo o diagnóstico, volume de leads por período (dia/semana) e os principais desafios categorizados. Esse endpoint poderia ser consumido futuramente por um dashboard interno em React ou Streamlit para fornecer insights valiosos ao time de growth da empresa.
