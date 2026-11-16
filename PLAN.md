# Planejamento de Implementação - meeting-bot

## Visão Geral

Criar um CLI Python para captura, transcrição e geração automática de resumos de reuniões, com exportação múltipla de formatos e sistema de índices inteligente.

## Estrutura de Arquivos

```
meeting-bot/
├── .claude/
│   └── CLAUDE.md              # Instruções para desenvolvimento
├── meeting_bot/
│   ├── __init__.py
│   ├── capture.py             # Captura de áudio
│   ├── transcribe.py          # Transcrição com Whisper
│   ├── summarize.py           # Resumo com IA
│   ├── export.py              # Exportação múltipla formatos
│   ├── index.py               # Sistema de índice/gerenciamento
│   ├── config.py              # Configurações do usuário
│   └── cli.py                 # Interface de linha de comando
├── bin/
│   └── meeting-bot            # Entry point executável
├── tests/
│   ├── test_capture.py
│   ├── test_summarize.py
│   └── test_export.py
├── templates/
│   └── default.md             # Template padrão de resumo
├── examples/
│   └── sample_summaries/      # Exemplos gerados
├── README.md
├── requirements.txt
├── pyproject.toml
└── PLAN.md                    # Este arquivo
```

## Fase 1: Estrutura Base e CLI (2-3 horas)

### Objetivos
- [ ] Criar estrutura de diretórios
- [ ] Configurar projeto Python (pyproject.toml, venv)
- [ ] Implementar CLI básica com argparse/click
- [ ] Criar entry point em `bin/meeting-bot`

### Comandos CLI básico
```bash
meeting-bot start "tema-da-reuniao"
meeting-bot stop
meeting-bot list [--date] [--tag]
meeting-bot search "palavra-chave"
meeting-bot summary
meeting-bot export --format [md|pdf|docx|html]
```

## Fase 2: Captura de Áudio (4-6 horas)

### Objetivos
- [ ] Detectar backend de áudio (FFmpeg, PyAudio, sounddevice)
- [ ] Implementar captura local do sistema
- [ ] Implementar captura de microfone externo
- [ ] Suporte a captura via scrcpy (áudio do celular)
- [ ] Gerenciamento de arquivos WAV

### Tecnologias
- `pyaudio` ou `sounddevice` para microfone
- `ffmpeg-python` para captura do sistema
- `scrcpy` integrado para captura de áudio do celular

## Fase 3: Transcrição com Whisper (3-4 horas)

### Objetivos
- [ ] Integração com Whisper local (offline)
- [ ] Suporte a Whisper API (online)
- [ ] Cache de transcrições
- [ ] Detecção automática de língua

### Modelos suportados
- `tiny` - Rápido, ~75MB
- `base` - Equilibrado
- `small` - Qualidade bom
- `medium` - Muito bom
- `large` - Máxima qualidade

## Fase 4: Resumo Inteligente com IA (4-5 horas)

### Objetivos
- [ ] Integração com Claude API (Anthropic)
- [ ] Fallback para OpenAI GPT
- [ ] Análise de ações/decisões
- [ ] Extração de responsáveis e prazos
- [ ] Formatação markdown estruturado

### Prompt padrão para resumo
```
Você é um assistente especializado em transcrever e resumir reuniões.
Formate a saída com:
1. Título da reunião e data
2. Tópicos principais (5-7 itens)
3. Decisões importantes (em tabela)
4. Ações definidas (com responsáveis)
5. Próximos passos

Siga rigorosamente estrutura markdown.
```

## Fase 5: Sistema de Exportação Múltipla (4-5 horas)

### Formatos suportados
- [ ] Markdown (.md) - nativo e principal
- [ ] PDF - usando weasyprint
- [ ] DOCX - usando python-docx
- [ ] HTML - visualização web
- [ ] YAML - para processamento automático
- [ ] TaskPaper - integração com ferramentas de tarefas
- [ ] ICS - exportação para calendário

### Templates configuráveis
- [ ] Template padrão (relatório)
- [ ] Template formal ( corporativo)
- [ ] Template minimalista (rapido)
- [ ] Template de apresentação (slide)

## Fase 6: Sistema de Índice e Busca (3-4 horas)

### Índice principal
```yaml
# index.yaml
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

### Comandos avançados
```bash
meeting-bot list --date 2025-11-15
meeting-bot list --tag sprint
meeting-bot search "projeto-alpha"
meeting-bot export-index --format json
```

## Fase 7: Integrações e Configurações (2-3 horas)

### Integrações
- [ ] Google Calendar (exportação de eventos)
- [ ] Slack (notificações automáticas)
- [ ] Telegram (resumos por mensagem)
- [ ] Notion (publicação automática)

### Configurações
```bash
# ~/.meeting-bot/config.yaml
language: pt-BR
timezone: America/Sao_Paulo
default_output_format: md
whisper_model: small
ai_provider: anthropic  # ou openai
ai_model: claude-3-5-haiku
```

## Fase 8: Tests e Documentação (2-3 horas)

### Testes
- [ ] Testes de captura de áudio
- [ ] Testes de transcrição
- [ ] Testes de exportação
- [ ] CI/CD básico com GitHub Actions

### Documentação
- [ ] README.md completo
- [ ] Exemplos de uso
- [ ] Guia de instalação
- [ ] API Reference

## Dependências Principais (requirements.txt)

```
click>=8.0.0                # CLI
pyaudio>=0.2.14             # Captura áudio
sounddevice>=0.4.7          # Alternativa áudio
ffmpeg-python>=0.2.0        # FFmpeg wrapper
faster-whisper>=1.0.0       # Whisper (ou open-whisper)
anthropic>=0.3.0            # API Claude
python-docx>=0.8.11         # DOCX export
weasyprint>=60.0            # PDF export
pyyaml>=6.0                 # YAML handling
```

## Cronograma Estimado

| Fase | Horas | Prioridade |
|------|-------|------------|
| Estrutura Base | 2-3h | ⭐⭐⭐⭐⭐ |
| Captura de Áudio | 4-6h | ⭐⭐⭐⭐⭐ |
| Transcrição | 3-4h | ⭐⭐⭐⭐⭐ |
| Resumo IA | 4-5h | ⭐⭐⭐⭐ |
| Exportação | 4-5h | ⭐⭐⭐⭐ |
| Índice/Busca | 3-4h | ⭐⭐⭐ |
| Integrações | 2-3h | ⭐⭐⭐ |
| Tests/Docs | 2-3h | ⭐⭐ |

**Total estimado:** 24-33 horas

## Próximos Passos Imediatos

1. Criar estrutura de pastas
2. Configurar ambiente virtual Python
3. Implementar CLI básica
4. Criar script de captura de áudio
5. Testar integração com Whisper

## Notas Importantes

- O projeto pode ser incremental - funcionalidades podem ser adicionadas conforme necessidade
- Cada fase é um MVP funcional por si só
- O suporte a scrcpy para áudio do celular é único e forte diferencial
- Exportação múltipla de formatos é essencial para adoção
- Sistema de índice permite escalabilidade para dezenas de reuniões

## Referências

- scrcpy: https://github.com/Genymobile/scrcpy
- Whisper: https://github.com/openai/whisper
- Claude API: https://docs.anthropic.com
- Python Click: https://click.palletsprojects.com