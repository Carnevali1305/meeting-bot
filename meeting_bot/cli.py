"""Interface de linha de comando para meeting-bot."""

import json
import os
from pathlib import Path
from typing import Optional

import click

from .capture import AudioCapture
from .transcribe import Transcriber
from .summarize import SummaryGenerator, MeetingSummary
from .export import Exporter, ExportFormat
from .index import IndexManager, MeetingEntry
from .config import ConfigManager


def _load_env() -> None:
    """Carrega variáveis de .env (global em ~/.meeting-bot/.env, depois o do diretório atual).

    Variáveis já definidas no ambiente têm precedência (override=False).
    Sem python-dotenv instalado, segue silenciosamente só com o ambiente.
    """
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    load_dotenv(Path.home() / ".meeting-bot" / ".env", override=False)
    load_dotenv(override=False)  # .env do diretório atual (ou acima)


_load_env()

# Estado da gravação atual
_STATE_FILE = Path.home() / ".meeting-bot" / "state.json"


def _get_state() -> dict:
    """Obtém o estado atual da gravação."""
    if _STATE_FILE.exists():
        try:
            return json.loads(_STATE_FILE.read_text())
        except (json.JSONDecodeError, IOError):
            pass
    return {"recording": None}


def _save_state(state: dict) -> None:
    """Salva o estado atual."""
    _STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    _STATE_FILE.write_text(json.dumps(state, default=str))


def _get_config() -> "Config":
    """Obtém a configuração atual."""
    manager = ConfigManager()
    return manager.get()


@click.group()
@click.version_option()
def cli() -> None:
    """meeting-bot - CLI para captura, transcrição e geração de resumos de reuniões."""
    pass


@cli.command()
@click.argument("topic")
@click.option("--phone-audio", is_flag=True, help="Usar captura de áudio do celular via scrcpy")
def start(topic: str, phone_audio: bool) -> None:
    """Iniciar gravação de áudio com TEMA da reunião.

    Exemplo: meeting-bot start "projeto-alpha-sprint-3"
    """
    state = _get_state()

    if state.get("recording"):
        click.echo(
            click.style(
                "⚠️  Já existe uma gravação em andamento!",
                fg="yellow"
            ),
            err=True
        )
        return

    config = _get_config()
    output_dir = config.meetings_dir or Path.home() / ".meeting-bot" / "meetings"

    capture = AudioCapture(output_dir=output_dir)
    audio_path = capture.start(topic)

    state = {
        "recording": {
            "topic": topic,
            "start_time": str(Path.cwd()),
            "audio_path": str(audio_path),
            "duration": "0m",
        }
    }
    _save_state(state)

    click.echo(click.style(f"✅ Gravação iniciada: {topic}", fg="green"))
    click.echo(f"📁 Arquivo: {audio_path}")
    click.echo(f"⏱️  Duração: {capture.get_duration()}")


@cli.command()
def stop() -> None:
    """Parar gravação de áudio."""
    state = _get_state()

    if not state.get("recording"):
        click.echo(click.style("⚠️  Nenhuma gravação em andamento.", fg="yellow"), err=True)
        return

    config = _get_config()
    output_dir = config.meetings_dir or Path.home() / ".meeting-bot" / "meetings"

    capture = AudioCapture(output_dir=output_dir)
    audio_path = capture.stop()

    state["recording"] = None
    _save_state(state)

    if audio_path:
        duration = capture.get_duration()
        click.echo(click.style(f"✅ Gravação parada com sucesso!", fg="green"))
        click.echo(f"📁 Arquivo: {audio_path}")
        click.echo(f"⏱️  Duração: {duration}")
    else:
        click.echo("❌ Nenhum arquivo foi gravado.")


@cli.command(name="list")
@click.option("--date", help="Filtrar por data (YYYY-MM-DD)")
@click.option("--tag", help="Filtrar por tag")
def list_meetings(date: Optional[str], tag: Optional[str]) -> None:
    """Listar reuniões gravadas.

    Exemplo: meeting-bot list --date 2025-11-15
    Exemplo: meeting-bot list --tag sprint
    """
    index = IndexManager()
    meetings = index.get_meetings(date_filter=date, tag_filter=tag)

    if not meetings:
        click.echo("📭 Nenhuma reunião encontrada.")
        return

    click.echo(f"📊 Encontradas {len(meetings)} reunião(ões):\n")

    for i, meeting in enumerate(meetings, 1):
        status = "✅" if meeting.actions_count > 0 else "📝"
        click.echo(f"{i}. {status} [{meeting.id}] {meeting.topic}")
        click.echo(f"   📅 {meeting.datetime} | ⏱️  {meeting.duration} | 🎯 {meeting.actions_count} ações")
        if meeting.tags:
            tags_str = ", ".join(meeting.tags)
            click.echo(f"   🏷️  Tags: {tags_str}")


@cli.command()
@click.argument("query")
def search(query: str) -> None:
    """Buscar reuniões por TERM.

    Exemplo: meeting-bot search "projeto-alpha"
    """
    index = IndexManager()
    results = index.search(query)

    if not results:
        click.echo(f"🔍 Nenhum resultado encontrado para '{query}'")
        return

    click.echo(f"🔍 Encontrados {len(results)} resultado(s) para '{query}':\n")

    for meeting in results:
        click.echo(f"• {meeting.topic} ({meeting.datetime})")


@cli.command()
@click.option("--format", "output_format", default="md",
              type=click.Choice(["md", "pdf", "docx", "html"]),
              help="Formato de saída do resumo")
def summary(output_format: str) -> None:
    """Gerar resumo da última reunião gravada."""
    state = _get_state()

    if state.get("recording"):
        click.echo(
            click.style(
                "⚠️  Ainda há uma gravação em andamento. Pare a gravação primeiro.",
                fg="yellow",
                err=True
            ),
            err=True
        )
        return

    config = _get_config()
    index = IndexManager()

    meetings = index.get_meetings()
    if not meetings:
        click.echo("📭 Nenhuma reunião gravada. Use 'meeting-bot start <tema>' primeiro.")
        return

    last_meeting = meetings[0]

    # Transcrever áudio
    audio_path_str = last_meeting.file or state.get("recording", {}).get("audio_path")
    audio_path = Path(audio_path_str) if audio_path_str else None

    if audio_path and audio_path.exists():
        transcriber = Transcriber(model_name=config.whisper_model)
        transcript = transcriber.transcribe(audio_path)
    else:
        # Placeholder de transcrição para testes
        transcript = f"Transcrição simulada para {last_meeting.topic}. Este é um texto de exemplo."

    if not transcriber.validate_transcript(transcript):
        click.echo("⚠️  Transcrição muito curta para gerar resumo.")
        return

    # Gerar resumo com IA
    generator = SummaryGenerator(provider=config.ai_provider, model=config.ai_model)

    try:
        api_key = os.getenv("ANTHROPIC_API_KEY") or os.getenv("OPENAI_API_KEY")
        if api_key:
            summary_obj = generator.generate(transcript, last_meeting.topic, last_meeting.duration)
        else:
            click.echo("⚠️  Sem chave de API. Generando resumo placeholder...")
            summary_obj = MeetingSummary(
                title=last_meeting.topic,
                datetime=last_meeting.datetime,
                duration=last_meeting.duration,
                topics=[last_meeting.topic],
                decisions=["Reunião resumida"],
                actions=[],
                next_steps=[],
                raw_transcript=transcript[:500] + "..." if len(transcript) > 500 else transcript,
            )
    except Exception as e:
        click.echo(f"❌ Erro ao gerar resumo: {e}")
        return

    # Exportar
    exporter = Exporter()
    output_path = exporter.export(summary_obj, ExportFormat(output_format))

    # Atualizar índice
    index.add_meeting(MeetingEntry(
        id=last_meeting.id,
        datetime=last_meeting.datetime,
        topic=last_meeting.topic,
        file=str(output_path),
        duration=summary_obj.duration,
        attendees=[],
        tags=last_meeting.tags,
        actions_count=len(summary_obj.actions),
        last_modified=str(Path.cwd()),
    ))

    click.echo(click.style(f"✅ Resumo gerado: {output_path}", fg="green"))
    click.echo(f"📝 Temas: {len(summary_obj.topics)} itens")
    click.echo(f"🎯 Ações: {len(summary_obj.actions)} itens")


@cli.command()
@click.option("--format", "output_format", default="md",
              type=click.Choice(["md", "pdf", "docx", "html"]),
              help="Formato de saída")
@click.argument("topic", required=False)
def export(output_format: str, topic: Optional[str]) -> None:
    """Exportar resumo para formato FORMAT.

    Exemplo: meeting-bot export --format pdf "tema-da-reuniao"
    """
    index = IndexManager()

    if topic:
        meetings = index.search(topic)
        if not meetings:
            click.echo(f"❌ Reunião '{topic}' não encontrada.")
            return
        meeting = meetings[0]
        summary_obj = MeetingSummary(
            title=meeting.topic,
            datetime=meeting.datetime,
            duration=meeting.duration,
            topics=[],
            decisions=[],
            actions=[],
            next_steps=[],
            raw_transcript="",
        )
    else:
        meetings = index.get_meetings()
        if not meetings:
            click.echo("📭 Nenhuma reunião para exportar.")
            return
        last_meeting = meetings[0]
        summary_obj = MeetingSummary(
            title=last_meeting.topic,
            datetime=last_meeting.datetime,
            duration=last_meeting.duration,
            topics=[],
            decisions=[],
            actions=[],
            next_steps=[],
            raw_transcript="",
        )

    exporter = Exporter()
    output_path = exporter.export(summary_obj, ExportFormat(output_format))

    click.echo(click.style(f"✅ Exportado: {output_path}", fg="green"))


@cli.group()
def config() -> None:
    """Comandos de configuração do meeting-bot."""
    pass


@config.command("init")
def config_init() -> None:
    """Inicializar configurações padrão."""
    manager = ConfigManager()
    manager.init()
    click.echo(click.style("✅ Configurações inicializadas com sucesso!", fg="green"))
    click.echo(f"📁 Arquivo: {manager.config_path}")


@config.command("get")
@click.argument("key", required=False)
def config_get(key: Optional[str]) -> None:
    """Obter configuração.

    Exemplo: meeting-bot config get ai_provider
    """
    manager = ConfigManager()
    cfg = manager.get()

    if key:
        value = getattr(cfg, key, None)
        if value is None:
            click.echo(f"❌ Chave '{key}' não encontrada.")
        else:
            click.echo(f"{key}: {value}")
    else:
        click.echo("⚙️  Configurações atuais:")
        for key, value in cfg.to_dict().items():
            click.echo(f"  {key}: {value}")


@config.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Definir uma configuração.

    Exemplo: meeting-bot config set ai_provider anthropic
    Exemplo: meeting-bot config set whisper_model small
    """
    manager = ConfigManager()
    manager.set(key, value)
    click.echo(click.style(f"✅ {key} = {value}", fg="green"))


@cli.command()
def doctor() -> None:
    """Verificar se as dependências estão instaladas corretamente."""
    click.echo("🔍 Verificando dependências...\n")

    checks = [
        ("click", "CLI framework"),
        ("pyaudio", "Captura de áudio"),
        ("sounddevice", "Áudio alternativo"),
        ("faster_whisper", "Transcrição Whisper"),
        ("anthropic", "API Claude"),
        ("docx", "Exportação DOCX"),
        ("weasyprint", "Exportação PDF"),
        ("yaml", "YAML"),
    ]

    for module, description in checks:
        try:
            __import__(module)
            click.echo(f"✅ {module:20} - {description}")
        except ImportError:
            click.echo(f"❌ {module:20} - {description} (não instalado)")

    import shutil
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        click.echo(f"✅ {'ffmpeg':20} - {ffmpeg_path}")
    else:
        click.echo(f"⚠️  {'ffmpeg':20} - não encontrado (captura limitada)")

    click.echo("\n📄 Arquivos .env:")
    for env_path in [Path.home() / ".meeting-bot" / ".env", Path.cwd() / ".env"]:
        status = "✅ encontrado" if env_path.exists() else "⚠️  não existe"
        click.echo(f"{status}: {env_path}")

    click.echo("\n🔑 Chaves de API:")
    for key in ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]:
        if os.getenv(key):
            click.echo(f"✅ {key} configurada")
        else:
            click.echo(f"⚠️  {key} não configurada")


def main() -> None:
    """Entry point para o CLI."""
    cli()


if __name__ == "__main__":
    cli()