"""Testes do módulo de transcrição."""

from pathlib import Path

from meeting_bot.transcribe import Transcriber


def test_transcribe_returns_string(tmp_path: Path) -> None:
    """transcribe retorna string com o nome do arquivo."""
    transcriber = Transcriber()
    audio_file = tmp_path / "test.wav"
    audio_file.touch()

    result = transcriber.transcribe(audio_file)

    assert isinstance(result, str)
    assert "test.wav" in result


def test_transcribe_with_details_returns_dict(tmp_path: Path) -> None:
    """transcribe_with_details retorna estrutura correta."""
    transcriber = Transcriber()
    audio_file = tmp_path / "test.wav"
    audio_file.touch()

    result = transcriber.transcribe_with_details(audio_file)

    assert isinstance(result, dict)
    assert "text" in result
    assert "language" in result
    assert "segments" in result


def test_transcribe_uses_model_name_from_constructor(tmp_path: Path) -> None:
    """O nome do modelo é armazenado corretamente."""
    transcriber = Transcriber(model_name="large")

    assert transcriber.model_name == "large"


def test_transcribe_uses_device_from_constructor(tmp_path: Path) -> None:
    """O dispositivo é armazenado corretamente."""
    transcriber = Transcriber(device="cpu")

    assert transcriber.device == "cpu"


def test_validate_transcript_rejects_short_text(tmp_path: Path) -> None:
    """Validação rejeita textos muito curtos."""
    transcriber = Transcriber()

    assert transcriber.validate_transcript("curto") is False
    assert transcriber.validate_transcript("x" * 100) is True
