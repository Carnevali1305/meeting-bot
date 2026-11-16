"""Testes do módulo de configuração."""

from pathlib import Path

from meeting_bot.config import Config, ConfigManager, AIProvider, WhisperModel


def test_config_has_defaults() -> None:
    """Config tem valores padrão corretos."""
    config = Config()
    assert config.language == "pt-BR"
    assert config.timezone == "America/Sao_Paulo"
    assert config.default_output_format == "md"
    assert config.whisper_model == "small"
    assert config.ai_provider == "anthropic"
    assert config.ai_model == "claude-3-5-haiku"


def test_config_manager_loads_defaults(tmp_path: Path) -> None:
    """ConfigManager carrega configurações padrão."""
    config_path = tmp_path / "config.yaml"
    manager = ConfigManager(config_path=config_path)

    config = manager.get()

    assert isinstance(config, Config)
    assert config.language == "pt-BR"


def test_config_manager_save_and_load(tmp_path: Path) -> None:
    """ConfigManager salva e carrega corretamente."""
    config_path = tmp_path / "config.yaml"
    manager = ConfigManager(config_path=config_path)

    # Salvar configuração
    manager.set("language", "en-US")

    # Carregar novamente
    manager2 = ConfigManager(config_path=config_path)
    config = manager2.get()

    assert config.language == "en-US"


def test_config_to_dict_and_from_dict() -> None:
    """Config pode ser convertido para e de dicionário."""
    original = Config(language="en-US", ai_provider="openai")
    data = original.to_dict()

    restored = Config.from_dict(data)

    assert restored.language == "en-US"
    assert restored.ai_provider == "openai"


def test_config_init_creates_defaults(tmp_path: Path) -> None:
    """init() cria configurações padrão."""
    config_path = tmp_path / "config.yaml"
    manager = ConfigManager(config_path=config_path)

    manager.init()

    config = manager.get()
    assert config.language == "pt-BR"
    assert config_path.exists()
