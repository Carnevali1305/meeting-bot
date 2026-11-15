"""Testes do módulo de geração de resumos."""

from meeting_bot.summarize import MeetingSummary, SummaryGenerator


def test_generate_returns_meeting_summary() -> None:
    generator = SummaryGenerator()
    summary = generator.generate(
        transcript="texto de teste da reuniao",
        topic="Reuniao Teste",
        duration="15m",
    )

    assert isinstance(summary, MeetingSummary)
    assert summary.title == "Reuniao Teste"
    assert summary.duration == "15m"


def test_to_markdown_includes_title_and_sections() -> None:
    summary = MeetingSummary(
        title="Reuniao Alpha",
        datetime="2025-11-15 10:00:00",
        duration="30m",
        topics=["Tópico 1"],
        decisions=["Decisão 1"],
        actions=[{"owner": "@joao", "task": "Fazer X", "deadline": "2025-11-20"}],
    )
    markdown = summary.to_markdown()

    assert "# Reuniao Alpha" in markdown
    assert "Tópico 1" in markdown
    assert "Decisão 1" in markdown
    assert "@joao" in markdown
    assert "Fazer X" in markdown


def test_validate_transcript_rejects_short_text() -> None:
    generator = SummaryGenerator()
    assert generator.validate_transcript("curto") is False
    assert generator.validate_transcript("x" * 100) is True
