"""Testes do módulo de exportação."""

from pathlib import Path

from meeting_bot.export import ExportFormat, Exporter
from meeting_bot.summarize import MeetingSummary


def _sample_summary() -> MeetingSummary:
    return MeetingSummary(
        title="Reuniao Teste",
        datetime="2025-11-15 10:00:00",
        duration="20m",
        topics=["Tópico 1"],
        decisions=["Decisão 1"],
        actions=[{"owner": "@maria", "task": "Revisar doc", "deadline": "2025-11-18"}],
    )


def test_export_markdown_creates_file(tmp_path: Path) -> None:
    exporter = Exporter(output_dir=tmp_path)
    path = exporter.export(_sample_summary(), ExportFormat.MARKDOWN)

    assert path.exists()
    assert path.suffix == ".md"
    content = path.read_text(encoding="utf-8")
    assert "Reuniao Teste" in content


def test_export_multiple_formats(tmp_path: Path) -> None:
    exporter = Exporter(output_dir=tmp_path)
    paths = exporter.export_multiple(
        _sample_summary(),
        [ExportFormat.MARKDOWN, ExportFormat.HTML, ExportFormat.PDF, ExportFormat.DOCX],
    )

    assert len(paths) == 4
    for path in paths:
        assert path.exists()
