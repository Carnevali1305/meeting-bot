"""Testes do módulo de captura de áudio."""

from pathlib import Path

from meeting_bot.capture import AudioCapture


def test_audio_capture_creates_output_dir(tmp_path: Path) -> None:
    output_dir = tmp_path / "audio"
    AudioCapture(output_dir=output_dir)
    assert output_dir.exists()


def test_start_creates_wav_file(tmp_path: Path) -> None:
    capture = AudioCapture(output_dir=tmp_path)
    file_path = capture.start("reuniao-teste")

    assert file_path.exists()
    assert file_path.suffix == ".wav"
    assert "reuniao-teste" in file_path.name


def test_stop_returns_current_file(tmp_path: Path) -> None:
    capture = AudioCapture(output_dir=tmp_path)
    started = capture.start("reuniao-teste")
    stopped = capture.stop()

    assert stopped == started


def test_stop_without_start_returns_none(tmp_path: Path) -> None:
    capture = AudioCapture(output_dir=tmp_path)
    assert capture.stop() is None
