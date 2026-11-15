"""Módulo de configuração do usuário."""

import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, Union
from enum import Enum


class AIProvider(str, Enum):
    """Provedores de IA suportados."""
    ANTHROPIC = "anthropic"
    OPENAI = "openai"


class WhisperModel(str, Enum):
    """Modelos Whisper suportados."""
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass
class Config:
    """Configurações do usuário."""

    language: str = "pt-BR"
    timezone: str = "America/Sao_Paulo"
    default_output_format: str = "md"
    whisper_model: str = "small"
    ai_provider: str = "anthropic"
    ai_model: str = "claude-3-5-haiku"
    audio_device: Optional[str] = None
    meetings_dir: Optional[Path] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário."""
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, Path):
                value = str(value)
            result[key] = value
        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Config":
        """Cria a partir de dicionário."""
        if "meetings_dir" in data and isinstance(data["meetings_dir"], str):
            data["meetings_dir"] = Path(data["meetings_dir"])
        return cls(**data)


class ConfigManager:
    """Gerencia as configurações do usuário."""

    def __init__(self, config_path: Optional[Path] = None):
        """Inicializa o gerenciador de configuração.

        Args:
            config_path: Caminho para o arquivo de configuração.
        """
        from .utils import ensure_directory

        self.config_path = config_path or Path.home() / ".meeting-bot" / "config.yaml"
        ensure_directory(self.config_path.parent)
        self._config: Config = Config()

    def load(self) -> Config:
        """Carrega as configurações."""
        if self.config_path.exists():
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
                self._config = Config.from_dict(data)
        return self._config

    def save(self) -> None:
        """Salva as configurações."""
        with open(self.config_path, "w", encoding="utf-8") as f:
            yaml.dump(self._config.to_dict(), f, allow_unicode=True)

    def get(self) -> Config:
        """Obtém as configurações atuais."""
        return self.load()

    def set(self, key: str, value: Any) -> None:
        """Define uma configuração."""
        self.load()
        current = self._config.to_dict()
        current[key] = value
        if "meetings_dir" in current and isinstance(current["meetings_dir"], str):
            current["meetings_dir"] = Path(current["meetings_dir"])
        self._config = Config.from_dict(current)
        self.save()

    def init(self) -> None:
        """Inicializa configurações padrão."""
        self._config = Config()
        self.save()