# CLAUDE.md - meeting-bot

## Visão Geral do Projeto

`meeting-bot` é um CLI Python para captura, transcrição e geração automática de resumos de reuniões, com exportação múltipla de formatos e sistema de índices inteligente.

## Estrutura de Pastas

```
meeting-bot/
├── meeting_bot/           # Código principal do pacote
│   ├── __init__.py
│   ├── capture.py         # Captura de áudio
│   ├── transcribe.py      # Transcrição com Whisper
│   ├── summarize.py       # Resumo com IA
│   ├── export.py          # Exportação múltipla formatos
│   ├── index.py           # Sistema de índice/gerenciamento
│   ├── config.py          # Configurações do usuário
│   └── cli.py             # Interface de linha de comando
├── bin/
│   └── meeting-bot        # Entry point executável
├── tests/                 # Testes
├── templates/             # Templates de resumo
├── examples/              # Exemplos gerados
├── README.md
├── requirements.txt
├── pyproject.toml
└── PLAN.md                # Planejamento de implementação
```

## Como Executar

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

### Configuração Inicial
```bash
# Configurar usuário e preferências
meeting-bot config init

# Configurar AI provider
meeting-bot config set ai_provider anthropic
meeting-bot config set ai_model claude-3-5-haiku
```

## Comandos Principais

```bash
meeting-bot start "tema-da-reuniao"     # Iniciar gravação
meeting-bot stop                      # Parar gravação
meeting-bot list [--date] [--tag]   # Listar reuniões
meeting-bot search "palavra-chave"    # Buscar reuniões
meeting-bot summary                 # Gerar resumo da última
meeting-bot export --format pdf     # Exportar (md/pdf/docx/html)
```

## Fluxo de Trabalho Típico

1. **Antes da reunião:**
   ```bash
   meeting-bot config init  # Configurar uma vez
   ```

2. **Durante a reunião:**
   - Em outra aba/terminal:
   ```bash
   meeting-bot start "projeto-alpha-sprint-3"
   ```

3. **Após a reunião:**
   ```bash
   meeting-bot stop
   meeting-bot summary
   meeting-bot export --format md
   ```

## Dependências Principais

| Pacote | Uso | Instalação |
|--------|-----|------------|
| click | CLI | `pip install click` |
| pyaudio | Captura áudio | `pip install pyaudio` |
| faster-whisper | Transcrição | `pip install faster-whisper` |
| anthropic | API Claude | `pip install anthropic` |
| python-docx | DOCX export | `pip install python-docx` |
| weasyprint | PDF export | `pip install weasyprint` |

## Estrutura de Dados

### index.yaml
Arquivo principal que mantém índice de todas as reuniões:
```yaml
meetings:
  - id: 20251115-1430
    datetime: "2025-11-15T14:30:00"
    topic: "Reunião Projeto Alpha"
    file: "archive/2025-11/..."
    duration: "62m"
    attendees: ["@joao", "@maria"]
    tags: ["projeto-alpha", "sprint"]
    actions_count: 4
```

## Integração com scrcpy

O meeting-bot suporta captura de áudio do celular via scrcpy:
```bash
meeting-bot start "reuniao-celular" --phone-audio
```

Requisito: scrcpy instalado e dispositivo conectado via USB/Wi-Fi.

## Variáveis de Ambiente

```bash
ANTHROPIC_API_KEY    # Chave da API Claude
OPENAI_API_KEY       # Chave da API OpenAI (fallback)
WHISPER_MODEL        # Modelo a ser usado (default: small)
```

## Notas de Desenvolvimento

- Cada fase é um MVP funcional por si só
- O suporte a scrcpy para áudio do celular é diferencial único
- Exportação múltipla de formatos é essencial para adoção
- Sistema de índice permite escalabilidade para dezenas de reuniões