"""Módulo de captura de áudio."""

import shutil
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Callable, List, Optional

# Tempo (em segundos) aguardado por `wait()` antes de forçar `kill()`.
_STOP_WAIT_TIMEOUT = 5


class AudioCapture:
    """Gerencia a captura de áudio das reuniões."""

    def __init__(
        self,
        output_dir: Optional[Path] = None,
        popen_factory: Optional[Callable[..., "subprocess.Popen"]] = None,
    ):
        """Inicializa o capturador de áudio.

        Args:
            output_dir: Diretório para salvar os arquivos de áudio.
            popen_factory: Fábrica usada para criar o processo de captura
                (compatível com a assinatura de `subprocess.Popen`). Permite
                injetar um processo falso em testes, evitando spawnar o
                ffmpeg real. Por padrão usa `subprocess.Popen`.
        """
        from .utils import ensure_directory

        self.output_dir = output_dir or Path(tempfile.gettempdir()) / "meetings"
        ensure_directory(self.output_dir)
        self._popen_factory = popen_factory or subprocess.Popen
        self._recording_process: Optional["subprocess.Popen[bytes]"] = None
        self._current_file: Optional[Path] = None
        self._start_time: Optional[float] = None
        self._duration_seconds: float = 0.0

    def start(self, topic: str) -> Path:
        """Inicia a gravação de áudio.

        Cria um arquivo `.wav` e, se o binário `ffmpeg` estiver disponível no PATH,
        lança-o em segundo plano gravando o áudio padrão do sistema (PulseAudio/ALSA),
        sobrescrevendo o placeholder. Se o `ffmpeg` não estiver disponível,
        degrade graciosamente mantendo o arquivo `.wav` vazio (placeholder).

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
        self._duration_seconds = 0.0

        # Garante que o arquivo exista imediatamente (placeholder)
        self._current_file.touch()

        ffmpeg_path = shutil.which("ffmpeg")
        if ffmpeg_path:
            command: List[str] = [
                ffmpeg_path,
                "-y",
                "-f", "pulse",
                "-i", "default",
                str(self._current_file),
            ]
            self._recording_process = self._popen_factory(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            self._recording_process = None

        self._start_time = time.monotonic()

        return self._current_file

    def stop(self) -> Optional[Path]:
        """Para a gravação de áudio.

        Encerra o processo do ffmpeg (quando houver) de forma limpa,
        chamando `terminate()` e aguardando `wait()` com tempo limitado
        antes de forçar `kill()`.

        Returns:
            Caminho para o arquivo gravado, ou None se não houver gravação ativa.
        """
        if self._current_file is None:
            return None

        if self._start_time is not None:
            self._duration_seconds = time.monotonic() - self._start_time
            self._start_time = None

        if self._recording_process is not None:
            self._recording_process.terminate()
            try:
                self._recording_process.wait(timeout=_STOP_WAIT_TIMEOUT)
            except subprocess.TimeoutExpired:
                self._recording_process.kill()
                self._recording_process.wait()
            self._recording_process = None

        return self._current_file

    def get_duration(self) -> str:
        """Retorna a duração atual da gravação.

        Enquanto a gravação está ativa, calcula o tempo decorrido desde
        `start()`. Após `stop()`, retorna a duração total registrada.
        """
        from .utils import format_duration

        if self._start_time is not None:
            elapsed = time.monotonic() - self._start_time
            return format_duration(elapsed)

        if self._duration_seconds:
            return format_duration(self._duration_seconds)

        return "0m"

    @property
    def is_recording(self) -> bool:
        """Verifica se há gravação ativa."""
        return self._recording_process is not None and self._recording_process.poll() is None

    @property
    def current_file(self) -> Optional[Path]:
        """Retorna o caminho do arquivo atual."""
        return self._current_file


def capture_system_audio(output_path: Path, duration: Optional[int] = None) -> bool:
    """Captura áudio do sistema usando FFmpeg.

    Args:
        output_path: Caminho para salvar o áudio.
        duration: Duração opcional em segundos. Se None, grava indefinidamente.

    Returns:
        True se a captura foi iniciada com sucesso.
    """
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        return False

    try:
        cmd = [
            ffmpeg_path,
            "-y",
            "-f", "pulse",
            "-i", "default",
            "-acodec", "pcm_s16le",
            "-ar", "44100",
            "-ac", "1",
        ]
        if duration:
            cmd.extend(["-t", str(duration)])

        cmd.append(str(output_path))

        subprocess.run(
            cmd,
            capture_output=True,
            check=True,
            timeout=duration + 10 if duration else 30,
        )
        return True
    except Exception:
        return False
