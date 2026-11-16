"""Testes do módulo de índice."""

from pathlib import Path

from meeting_bot.index import IndexManager, MeetingEntry


def test_meeting_entry_to_dict(tmp_path: Path) -> None:
    """MeetingEntry pode ser convertido para dicionário."""
    entry = MeetingEntry(
        id="20251115-1430",
        datetime="2025-11-15T14:30:00",
        topic="Reunião Teste",
        file="meetings/test.wav",
        duration="30m",
        attendees=["@joao", "@maria"],
        tags=["projeto-alpha", "sprint"],
        actions_count=3,
    )

    data = entry.to_dict()

    assert data["id"] == "20251115-1430"
    assert data["topic"] == "Reunião Teste"
    assert data["attendees"] == ["@joao", "@maria"]


def test_meeting_entry_from_dict(tmp_path: Path) -> None:
    """MeetingEntry pode ser criado a partir de dicionário."""
    data = {
        "id": "20251115-1430",
        "datetime": "2025-11-15T14:30:00",
        "topic": "Reunião Teste",
        "file": "meetings/test.wav",
        "duration": "30m",
        "attendees": [],
        "tags": [],
        "actions_count": 0,
        "last_modified": "",
    }

    entry = MeetingEntry.from_dict(data)

    assert entry.id == "20251115-1430"
    assert entry.topic == "Reunião Teste"


def test_index_manager_add_meeting(tmp_path: Path) -> None:
    """IndexManager adiciona reuniões corretamente."""
    index_path = tmp_path / "index.yaml"
    manager = IndexManager(index_path=index_path)

    entry = MeetingEntry(
        id="20251115-1430",
        datetime="2025-11-15T14:30:00",
        topic="Reunião Teste",
        file="meetings/test.wav",
        duration="30m",
        attendees=[],
        tags=[],
        actions_count=0,
    )

    manager.add_meeting(entry)

    meetings = manager.get_meetings()
    assert len(meetings) == 1
    assert meetings[0].topic == "Reunião Teste"


def test_index_manager_search(tmp_path: Path) -> None:
    """IndexManager busca por termo."""
    index_path = tmp_path / "index.yaml"
    manager = IndexManager(index_path=index_path)

    # Adicionar reuniões
    manager.add_meeting(MeetingEntry(
        id="20251115-1430",
        datetime="2025-11-15T14:30:00",
        topic="Projeto Alpha",
        file="meetings/test.wav",
        duration="30m",
        attendees=[],
        tags=["alpha"],
        actions_count=0,
    ))
    manager.add_meeting(MeetingEntry(
        id="20251115-1500",
        datetime="2025-11-15T15:00:00",
        topic="Projeto Beta",
        file="meetings/test2.wav",
        duration="45m",
        attendees=[],
        tags=["beta"],
        actions_count=0,
    ))

    # Buscar
    results = manager.search("Alpha")

    assert len(results) == 1
    assert results[0].topic == "Projeto Alpha"


def test_index_manager_filter_by_date(tmp_path: Path) -> None:
    """IndexManager filtra por data."""
    index_path = tmp_path / "index.yaml"
    manager = IndexManager(index_path=index_path)

    manager.add_meeting(MeetingEntry(
        id="20251115-1430",
        datetime="2025-11-15T14:30:00",
        topic="Reunião 1",
        file="meetings/test.wav",
        duration="30m",
        attendees=[],
        tags=[],
        actions_count=0,
    ))

    meetings = manager.get_meetings(date_filter="2025-11-15")

    assert len(meetings) == 1
    assert "2025-11-15" in meetings[0].datetime


def test_index_manager_filter_by_tag(tmp_path: Path) -> None:
    """IndexManager filtra por tag."""
    index_path = tmp_path / "index.yaml"
    manager = IndexManager(index_path=index_path)

    manager.add_meeting(MeetingEntry(
        id="20251115-1430",
        datetime="2025-11-15T14:30:00",
        topic="Reunião Teste",
        file="meetings/test.wav",
        duration="30m",
        attendees=[],
        tags=["sprint", "projeto-alpha"],
        actions_count=0,
    ))

    meetings = manager.get_meetings(tag_filter="sprint")

    assert len(meetings) == 1
    assert "sprint" in meetings[0].tags
