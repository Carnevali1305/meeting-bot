"""Módulo de geração de resumos com IA."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class MeetingSummary:
    """Representa um resumo de reunião."""

    title: str
    datetime: str
    duration: str
    participants: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)
    actions: List[Dict[str, str]] = field(default_factory=list)
    raw_transcript: str = ""

    def to_markdown(self) -> str:
        """Converte o resumo para Markdown."""
        lines = [
            f"# {self.title}",
            f"",
            f"**Data:** {self.datetime}",
            f"**Duração:** {self.duration}",
            f"",
            f"## 📋 Tópicos Tratados",
            f"",
        ]

        for topic in self.topics:
            lines.append(f"- {topic}")

        lines.extend([
            "",
            "## ✔️ Decisões Importantes",
            "",
        ])

        for decision in self.decisions:
            lines.append(f"- {decision}")

        lines.extend([
            "",
            "## 🎯 Ações Definidas",
            "",
        ])

        for action in self.actions:
            lines.append(f"- **{action['owner']}** - {action['task']} (até {action['deadline']})")

        lines.extend([
            "",
            "---",
            "*Gerado automaticamente pelo meeting-bot*",
        ])

        return "\n".join(lines)


class SummaryGenerator:
    """Gera resumos de reuniões usando IA."""

    def __init__(self, provider: str = "anthropic", model: str = "claude-3-5-haiku"):
        """Inicializa o gerador de resumos.

        Args:
            provider: Provedor de IA (anthropic, openai).
            model: Modelo específico a ser usado.
        """
        from .utils import ensure_directory

        self.provider = provider
        self.model = model
        self._client = None

    def generate(self, transcript: str, topic: str, duration: str = "0m") -> MeetingSummary:
        """Gera um resumo do texto transcrito.

        Args:
            transcript: Texto transcrito da reunião.
            topic: Título da reunião.
            duration: Duração da reunião.

        Returns:
            MeetingSummary com o resumo estruturado.
        """
        # TODO: Implementar chamada real à API de IA

        return MeetingSummary(
            title=topic,
            datetime=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            duration=duration,
            participants=[],
            topics=["Tópico 1", "Tópico 2"],
            decisions=["Decisão 1", "Decisão 2"],
            actions=[
                {"owner": "@usuario", "task": "Tarefa 1", "deadline": "2025-11-20"},
            ],
            raw_transcript=transcript[:500] + "..." if len(transcript) > 500 else transcript,
        )

    def _build_prompt(self, transcript: str) -> str:
        """Constrói o prompt para a API de IA."""
        return f"""
Você é um assistente especializado em transcrever e resumir reuniões.
Formate a saída com:
1. Título da reunião e data
2. Tópicos principais (5-7 itens)
3. Decisões importantes (em tabela)
4. Ações definidas (com responsáveis)
5. Próximos passos

Texto da reunião:
{transcript}
"""

    def _call_api(self, prompt: str) -> Dict[str, Any]:
        """Chama a API do provedor de IA."""
        # TODO: Implementar chamada real
        # Exemplo para Anthropic:
        # response = self._client.messages.create(
        #     model=self.model,
        #     max_tokens=1000,
        #     messages=[{"role": "user", "content": prompt}]
        # )
        # return response.content[0].text
        return {}

    def validate_transcript(self, transcript: str) -> bool:
        """Valida se o transcript é adequado para resumo."""
        return len(transcript.strip()) > 50