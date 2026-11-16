# meeting-bot 🤖

CLI Python para captura, transcrição e geração automática de resumos de reuniões.

## 📋 O que é?

O `meeting-bot` é uma ferramenta de linha de comando que:
- Grava áudio de reuniões diretamente do seu sistema
- Transcreve áudio para texto usando Whisper
- Gera resumos inteligentes com IA
- Exporta em múltiplos formatos (MD, PDF, DOCX, HTML)
- Mantém um índice de todas as reuniões

## 📚 Comandos

| Comando | Descrição |
|---------|-----------|
| `meeting-bot start <tema>` | Iniciar gravação de áudio |
| `meeting-bot stop` | Parar gravação |
| `meeting-bot list` | Listar reuniões |
| `meeting-bot search <termo>` | Buscar reuniões |
| `meeting-bot summary` | Gerar resumo da última reunião |
| `meeting-bot export --format <fmt>` | Exportar para MD/PDF/DOCX/HTML |

## 📖 Documentação

- **[ARCHITECTURE.md](ARCHITECTURE.md)** - Documentação técnica completa da arquitetura, fluxos e componentes
- **[manual.html](manual.html)** - Manual de usuário interativo

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

## 🔐 Variáveis de Ambiente Necessárias

```bash
# API Keys (opcionais, mas recomendados)
ANTHROPIC_API_KEY    # Chave da API Claude
OPENAI_API_KEY       # Chave da API OpenAI (fallback)

# Configuração do Whisper
WHISPER_MODEL        # Modelo a ser usado (default: small)

# Diretório de saída
MEETINGS_DIR         # Pasta para salvar reuniões
```

## 🤝 Contribuindo

Veja o arquivo `PLAN.md` para o roadmap de desenvolvimento.

## 📊 Progresso de Implementação

### ✅ Concluído
- **CLI completa** - Todos os comandos implementados e conectados
- **Módulo de captura** - Estrutura completa com AudioCapture
- **Módulo de transcrição** - Estrutura com Transcriber
- **Módulo de resumo** - Integration com API anthropic/openai, parse JSON
- **Módulo de exportação** - PDF, DOCX, HTML completos com CSS profissional
- **Módulo de índice** - Sistema de busca e gerenciamento
- **Sistema de configuração** - ConfigManager com YAML
- **Testes** - 9 testes passando (capture, summarize, export)

### 🚀 Como Testar Localmente

```bash
# Criar e ativar ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependências
pip install -e .[dev]

# Verificar dependências
meeting-bot doctor

# Executar testes
pytest -v
```

## 🛡️ Segurança

- ✅ `.env` está no `.gitignore`
- ✅ Chaves API são carregadas de variáveis de ambiente
- ✅ Nenhum segredo hard-coded

## 📈 Roadmap

1. ✅ Captura de áudio
2. ✅ Transcrição Whisper
3. ✅ Geração de resumo com IA
4. ✅ Exportação multi-formato
5. ✅ Sistema de índice
6. 🔄 Melhorias de performance (em andamento - RuFlo)
7. ⏳ Dashboard web opcional (planejado)