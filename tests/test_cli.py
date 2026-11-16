"""Testes de integração do CLI."""

from click.testing import CliRunner

from meeting_bot.cli import cli, _STATE_FILE


def _clear_state() -> None:
    """Remove o arquivo de estado para isolar o teste."""
    if _STATE_FILE.exists():
        _STATE_FILE.unlink()


def test_cli_start_command() -> None:
    """Comando start funciona corretamente."""
    _clear_state()
    runner = CliRunner()
    result = runner.invoke(cli, ["start", "test-meeting"])

    assert result.exit_code == 0
    assert "Gravação iniciada" in result.output

    # Limpa a gravação iniciada para não vazar estado aos próximos testes
    runner.invoke(cli, ["stop"])


def test_cli_stop_without_start() -> None:
    """Comando stop sem start mostra mensagem de erro."""
    runner = CliRunner()
    result = runner.invoke(cli, ["stop"])

    # O stop sem gravação mostra "Nenhum arquivo foi gravado" ou mensagem similar
    assert "Nenhuma gravação" in result.output or "Nenhum arquivo" in result.output


def test_cli_list_empty() -> None:
    """Comando list com índice vazio."""
    runner = CliRunner()
    result = runner.invoke(cli, ["list"])

    assert "Nenhuma reunião encontrada" in result.output


def test_cli_search_not_found() -> None:
    """Comando search sem resultados."""
    runner = CliRunner()
    result = runner.invoke(cli, ["search", "nonexistent"])

    assert "Nenhum resultado encontrado" in result.output


def test_cli_config_init() -> None:
    """Comando config init funciona."""
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "init"])

    assert result.exit_code == 0
    assert "Configurações inicializadas" in result.output


def test_cli_doctor_command() -> None:
    """Comando doctor list dependencies."""
    runner = CliRunner()
    result = runner.invoke(cli, ["doctor"])

    assert result.exit_code == 0
    assert "Verificando dependências" in result.output


def test_cli_config_get_all() -> None:
    """Comando config get sem argumento mostra todas as configs."""
    runner = CliRunner()
    result = runner.invoke(cli, ["config", "get"])

    assert result.exit_code == 0
    assert "Configurações atuais" in result.output or "language:" in result.output


def test_cli_help() -> None:
    """Comando --help funciona."""
    runner = CliRunner()
    result = runner.invoke(cli, ["--help"])

    assert result.exit_code == 0
    assert "meeting-bot" in result.output
