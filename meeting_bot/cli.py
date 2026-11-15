"""Interface de linha de comando para meeting-bot."""

import click


@click.group()
@click.version_option()
def cli() -> None:
    """meeting-bot - CLI para captura, transcrição e geração de resumos de reuniões."""
    pass


@cli.command()
@click.argument("topic")
def start(topic: str) -> None:
    """Iniciar gravação de áudio com TEMA da reunião."""
    click.echo(f"Gravação iniciada: {topic}")
    # TODO: Implementar captura de áudio


@cli.command()
def stop() -> None:
    """Parar gravação de áudio."""
    click.echo("Gravação parada")
    # TODO: Implementar parada da captura


@cli.command(name="list")
@click.option("--date", help="Filtrar por data (YYYY-MM-DD)")
@click.option("--tag", help="Filtrar por tag")
def list_meetings(date: str | None, tag: str | None) -> None:
    """Listar reuniões gravadas."""
    click.echo(f"Listando reuniões (date={date}, tag={tag})")
    # TODO: Implementar listagem


@cli.command()
@click.argument("query")
def search(query: str) -> None:
    """Buscar reuniões por TERM.

    Exemplo: meeting-bot search "projeto-alpha"
    """
    click.echo(f"Procurando por: {query}")
    # TODO: Implementar busca


@cli.command()
def summary() -> None:
    """Gerar resumo da última reunião."""
    click.echo("Gerando resumo...")
    # TODO: Implementar geração de resumo


@cli.command()
@click.option("--format", "output_format", default="md",
              type=click.Choice(["md", "pdf", "docx", "html"]),
              help="Formato de saída")
def export(output_format: str) -> None:
    """Exportar resumo para formato FORMAT."""
    click.echo(f"Exportando para {output_format}...")
    # TODO: Implementar exportação


@cli.command()
def config() -> None:
    """Configurações do usuário."""
    click.echo("Comandos de configuração")
    # TODO: Implementar configuração


def main() -> None:
    """Entry point para o CLI."""
    cli()


if __name__ == "__main__":
    cli()