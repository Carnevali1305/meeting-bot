"""Módulo de gerenciamento de índice de reuniões."""

import yaml
from pathlib import Path
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict, field
from datetime import datetime


@dataclass
class MeetingEntry:
    """Entrada de reunião no índice."""

    id: str
    datetime: str
    topic: str
    file: str
    duration: str
    attendees: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
    actions_count: int = 0
    last_modified: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MeetingEntry":
        """Cria a partir de dicionário."""
        return cls(**data)


class IndexManager:
    """Gerencia o índice de reuniões."""

    def __init__(self, index_path: Optional[Path] = None):
        """Inicializa o gerenciador de índice.

        Args:
            index_path: Caminho para o arquivo de índice.
        """
        from .utils import ensure_directory

        self.index_path = index_path or Path.home() / ".meeting-bot" / "index.yaml"
        ensure_directory(self.index_path.parent)
        self._index: Dict[str, Any] = {"meetings": [], "stats": {}}

    def load(self) -> Dict[str, Any]:
        """Carrega o índice do arquivo."""
        if self.index_path.exists():
            with open(self.index_path, "r", encoding="utf-8") as f:
                self._index = yaml.safe_load(f) or {"meetings": [], "stats": {}}
        return self._index

    def save(self) -> None:
        """Salva o índice no arquivo."""
        with open(self.index_path, "w", encoding="utf-8") as f:
            yaml.dump(self._index, f, allow_unicode=True, default_flow_style=False)

    def add_meeting(self, entry: MeetingEntry) -> None:
        """Adiciona uma reunião ao índice."""
        self.load()
        self._index["meetings"].append(entry.to_dict())
        self._update_stats()
        self.save()

    def get_meetings(self, date_filter: Optional[str] = None,
                     tag_filter: Optional[str] = None) -> List[MeetingEntry]:
        """Obtém reuniões filtradas."""
        self.load()
        meetings = [MeetingEntry.from_dict(m) for m in self._index["meetings"]]

        if date_filter:
            meetings = [m for m in meetings if date_filter in m.datetime]
        if tag_filter:
            meetings = [m for m in meetings if tag_filter in m.tags]

        return sorted(meetings, key=lambda m: m.datetime, reverse=True)

    def search(self, query: str) -> List[MeetingEntry]:
        """Pesquisa reuniões por termo."""
        self.load()
        meetings = [MeetingEntry.from_dict(m) for m in self._index["meetings"]]

        query_lower = query.lower()
        results = [
            m for m in meetings
            if query_lower in m.topic.lower()
            or query_lower in " ".join(m.attendees).lower()
            or any(query_lower in tag.lower() for tag in m.tags)
        ]

        return sorted(results, key=lambda m: m.datetime, reverse=True)

    def _update_stats(self) -> None:
        """Atualiza estatísticas do índice."""
        meetings = self._index.get("meetings", [])
        self._index["stats"] = {
            "total_meetings": len(meetings),
            "last_sync": datetime.now().isoformat(),
        }

    def clear(self) -> None:
        """Limpa o índice."""
        self._index = {"meetings": [], "stats": {}}
        self.save()