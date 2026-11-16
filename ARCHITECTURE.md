# Documentação de Arquitetura - meeting-bot

## Visão Geral

`meeting-bot` é um **CLI Python** para captura, transcrição e geração automática de resumos de reuniões. O projeto segue uma arquitetura modular e baseada em comandos.

## 📁 Estrutura do Projeto

```
meeting-bot/
├── meeting_bot/           # Código principal do pacote
│   ├── __init__.py        # Inicialização do pacote
│   ├── cli.py             # Interface de linha de comando (220+ linhas)
│   ├── capture.py         # Captura de áudio com PyAudio
│   ├── transcribe.py      # Transcrição com faster-whisper
│   ├── summarize.py       # Resumo com IA (Anthropic/OpenAI)
│   ├── export.py          # Exportação multi-formato (md, pdf, docx, html)
│   ├── index.py           # Sistema de índice/gerenciamento de reuniões
│   ├── config.py          # Gerenciamento de configurações
│   └── utils.py           # Utilitários compartilhados
├── bin/
│   └── meeting-bot        # Entry point executável
├── tests/                 # Testes unitários
├── templates/             # Templates de resumo
├── examples/              # Exemplos gerados
├── README.md              # Documentação principal
├── PLAN.md                # Planejamento de implementação
└── CLAUDE.md              # Instruções para Claude Code
```

## 🏗️ Arquitetura de Componentes

### 1. **Interface CLI (`cli.py`)**
- **Framework:** Click (>=8.0.0)
- **Comandos principais:**
  - `start <topic>` - Iniciar gravação
  - `stop` - Parar gravação
  - `list` - Listar reuniões
  - `search <query>` - Buscar reuniões
  - `summary` - Gerar resumo da última reunião
  - `export --format <fmt>` - Exportar para PDF/DOCX/MD/HTML
  - `doctor` - Verificar dependências

### 2. **Captura de Áudio (`capture.py`)**
- **Tecnologia:** PyAudio + sounddevice
- **Recursos:**
  - Gravação em tempo real
  - Suporte a scrcpy para áudio de celular
  - Salva como WAV (formato não comprimido)

### 3. **Transcrição (`transcribe.py`)**
- **Modelo:** faster-whisper (>=1.0.0)
- **Hardware:** GPU/CPU com suporte CUDA opcional
- **Formato de saída:** Texto limpo com timestamps

### 4. **Geração de Resumo (`summarize.py`)**
- **Providers suportados:**
  - Anthropic (Claude)
  - OpenAI (GPT)
- **Modelo padrão:** `claude-3-5-haiku` (custo eficiente)
- **Fallback:** Resumo placeholder quando API key não configurada

### 5. **Exportação (`export.py`)**
- **Formatos:**
  - Markdown (`.md`)
  - PDF (`.pdf`) via WeasyPrint
  - DOCX (`.docx`) via python-docx
  - HTML (`.html`)

### 6. **Índice (`index.py`)**
- **Armazenamento:** YAML (`index.yaml`) em `~/.meeting-bot/`
- **Metadados:** ID, datetime, tópico, duração, tags, ações

### 7. **Configuração (`config.py`)**
- **Arquivo:** `~/.meeting-bot/config.yaml`
- **Variáveis:**
  - `ai_provider` - anthropic/openai
  - `ai_model` - modelo a ser usado
  - `whisper_model` - modelo whisper (small/base/large)
  - `meetings_dir` - diretório de saída

## 🔗 Fluxo de Dados

```mermaid
graph TD
    A[meeting-bot start "tópico"] --> B[AudioCapture.start]
    B --> C[Grava áudio em tempo real]
    C --> D[meeting-bot stop]
    D --> E[AudioCapture.stop]
    E --> F[Arquivo WAV salvo]
    F --> G[meeting-bot summary]
    G --> H[Transcriber.transcribe]
    H --> I[Transcript do Whisper]
    I --> J[SummaryGenerator.generate]
    J --> K[Resumo via IA]
    K --> L[Exporter.export]
    L --> M[Arquivo de saída]
    M --> N[IndexManager.add_meeting]
    N --> O[Metadados atualizados]
```

## 📦 Dependências Principais

| Pacote | Versão | Função |
|--------|--------|--------|
| `click` | >=8.0.0 | CLI framework |
| `pyaudio` | >=0.2.14 | Captura áudio |
| `sounddevice` | >=0.4.7 | Áudio alternativo |
| `faster-whisper` | >=1.0.0 | Transcrição |
| `av` | <16 | Processamento de áudio |
| `anthropic` | >=0.3.0 | API Claude |
| `python-docx` | >=0.8.11 | Export DOCX |
| `weasyprint` | >=60.0 | Export PDF |
| `python-dotenv` | >=1.0.0 | Carregar .env |

## ⚙️ Configuração

### Variáveis de Ambiente

```bash
# API Keys (opcionais, mas recomendados)
ANTHROPIC_API_KEY    # Chave da API Claude
OPENAI_API_KEY       # Chave da API OpenAI (fallback)

# Configuração do Whisper
WHISPER_MODEL        # Modelo a ser usado (default: small)

# Diretório de saída
MEETINGS_DIR         # Pasta para salvar reuniões
```

### Arquivo .env

O projeto carrega variáveis de:
1. `~/.meeting-bot/.env` (global)
2. Diretório atual (`.env`)

## 🔒 Segurança

### Credenciais
- ✅ `.env` está no `.gitignore`
- ✅ Chaves API são carregadas de variáveis de ambiente
- ✅ Nenhum segredo hard-coded

### Permissões
- Estado de gravação armazenado em: `~/.meeting-bot/state.json`
- Apenas o usuário tem permissão de leitura/escrita

### Validações
- Verifica se já existe gravação antes de iniciar novo start
- Valida transcrição antes de gerar resumo
- Tratamento de erros robusto

## 🚀 Como Executar

### Desenvolvimento Local
```bash
# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e .[dev]

# Executar CLI
python -m meeting_bot.cli start "tema-da-reuniao"

# Ou usar o script diretamente
./bin/meeting-bot start "tema-da-reuniao"
```

### Comandos Principais
```bash
# Configurar
meeting-bot config init
meeting-bot config set ai_provider anthropic
meeting-bot config set ai_model claude-3-5-haiku

# Verificar dependências
meeting-bot doctor

# Fluxo completo
meeting-bot start "reuniao-projeto"
meeting-bot stop
meeting-bot summary
meeting-bot export --format pdf
```

## 📊 Métricas de Desempenho

### Recomendações do RuFlo Performance:
- **HNSW quantization:** +50% redução de memória
- **WASM SIMD:** +4x de velocidade
- **Request batching:** -30% latência

### Otimizações implementadas:
- Cache de estado em `~/.meeting-bot/state.json`
- Carregamento inteligente de .env
- Transcrição incremental quando possível

## 🧪 Testes

```bash
# Executar todos os testes
pytest -v

# Cobertura
pytest --cov=meeting_bot --cov-report=html
```

## 📝 Notas de Desenvolvimento

- Cada fase é um MVP funcional por si só
- Suporte a scrcpy para áudio do celular é diferencial único
- Exportação múltipla de formatos é essencial para adoção
- Sistema de índice permite escalabilidade para dezenas de reuniões

## 🔗 Integrações

- **Supabase:** Não utilizado (projeto local)
- **Fireflies.ai:** Não integrado
- **Twilio:** Não utilizado
