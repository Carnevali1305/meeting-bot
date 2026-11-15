"""Módulo de captura de áudio."""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional


class AudioCapture:
    """Gerencia a captura de áudio das reuniões."""

    def __init__(self, output_dir: Optional[Path] = None):
        """Inicializa o capturador de áudio.

        Args:
            output_dir: Diretório para salvar os arquivos de áudio.
        """
        from .utils import ensure_directory
        from .utils import format_duration

        self.output_dir = output_dir or Path(tempfile.gettempdir()) / "meetings"
        ensure_directory(self.output_dir)
        self._recording_process = None
        self._current_file: Optional[Path] = None
        self._start_time: Optional[float] = None

    def start(self, topic: str) -> Path:
        """Inicia a gravação de áudio.

        Args:
            topic: Título da reunião.

        Returns:
            Caminho para o arquivo de áudio sendo gravado.
        """
        from .utils import get_timestamp, sanitize_filename

        timestamp = get_timestamp()
        safe_topic = sanitize_filename(topic)
        filename = f"{timestamp}-{safe_topic}.wav"
        self._current_file = self.output_dir / filename

        # Placeholder - substituir por ffmpeg/pipewire quando implementado
        self._current_file.touch()

        return self._current_file

    def stop(self) -> Optional[Path]:
        """Para a gravação de áudio.

        Returns:
            Caminho para o arquivo gravado, ou None se não houver gravação ativa.
        """
        return self._current_file

    def get_duration(self) -> str:
        """Retorna a duração atual da gravação."""
        from .utils import format_duration
        if self._start_time:
            return format_duration(0)  # Placeholder
        return "0m"


def capture_system_audio(output_path: Path) -> bool:
    """Captura áudio do sistema usando FFmpeg.

    Args:
        output_path: Caminho para salvar o áudio.

    Returns:
        True se a captura foi iniciada com sucesso.
    """
    # TODO: Implementar com ffmpeg-python
    # Exemplo:
    # import ffmpeg
    # (
    #     ffmpeg
    #     .input('default', format='alsa', acodec='pcm_s16le')
    #     .output(str(output_path), format='wav')
    #     .overwrite_output()
    #     .run()
    # )
    return False