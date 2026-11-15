# meeting-bot 🤖

CLI Python para captura, transcrição e geração automática de resumos de reuniões.

## 📋 O que é?

O `meeting-bot` é uma ferramenta de linha de comando que:
- Grava áudio de reuniões diretamente do seu sistema
- Transcreve áudio para texto usando Whisper
- Gera resumos inteligentes com IA
- Exporta em múltiplos formatos (MD, PDF, DOCX, HTML)
- Mantém um índice de todas as reuniões

## 🚀 Começando

```bash
# Instalar dependências
pip install -r requirements.txt

# Ou instalar em modo desenvolvimento
pip install -e .[dev]

# Usar
meeting-bot start "projeto-alpha-reuniao"
meeting-bot stop
meeting-bot summary
meeting-bot export --format pdf
```

## 📚 Comandos

| Comando | Descrição |
|---------|-----------|
| `meeting-bot start <tema>` | Iniciar gravação de áudio |
| `meeting-bot stop` | Parar gravação |
| `meeting-bot list` | Listar reuniões |
| `meeting-bot search <termo>` | Buscar reuniões |
| `meeting-bot summary` | Gerar resumo da última reunião |
| `meeting-bot export --format <fmt>` | Exportar para MD/PDF/DOCX/HTML |

## 🎯 Fluxo de Trabalho

1. **Iniciar gravação:** `meeting-bot start "tema-da-reuniao"`
2. **Parar gravação:** `meeting-bot stop`
3. **Gerar resumo:** `meeting-bot summary`
4. **Exportar:** `meeting-bot export --format md`

## 📦 Dependências

- Python 3.10+
- FFmpeg (para captura de áudio)
- Whisper (para transcrição)
- Anthropic/OpenAI (para resumo)

## 🔧 Configuração

```bash
meeting-bot config init
meeting-bot config set ai_provider anthropic
meeting-bot config set whisper_model small
```

## 📁 Estrutura de Arquivos

```
~/.meeting-bot/
├── index.yaml              # Índice de reuniões
├── config.yaml             # Configurações do usuário
└── meetings/               # Reuniões gravadas
    └── archive/
```

## 🤝 Contribuindo

Veja o arquivo `PLAN.md` para o roadmap de desenvolvimento.