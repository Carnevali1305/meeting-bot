"""Utilitários comuns para meeting-bot."""

from pathlib import Path
from datetime import datetime
from typing import Optional, List


def format_duration(seconds: float) -> str:
    """Formata duração em segundos para formato legível.

    Args:
        seconds: Duração em segundos.

    Returns:
        String formatada (ex: "1h 30m", "45m", "5m").
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)

    if hours > 0:
        return f"{hours}h {minutes}m"
    else:
        return f"{minutes}m"


def get_timestamp() -> str:
    """Retorna timestamp formatado.

    Returns:
        Timestamp no formato YYYYMMDD-HHMMSS.
    """
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def sanitize_filename(text: str, max_length: int = 50) -> str:
    """Sanitiza texto para uso em nome de arquivo.

    Args:
        text: Texto a ser sanitizado.
        max_length: Comprimento máximo do nome.

    Returns:
        Nome de arquivo seguro.
    """
    # Remove caracteres inválidos
    safe_chars = "".join(c for c in text if c.isalnum() or c in " -_")
    # Reduz espaços múltiplos a um único espaço
    safe_chars = " ".join(safe_chars.split())
    # Limita tamanho
    if len(safe_chars) > max_length:
        safe_chars = safe_chars[:max_length - 3] + "..."
    return safe_chars.replace(" ", "_")


def find_wav_files(directory: Path, pattern: str = "*.wav") -> List[Path]:
    """Encontra arquivos WAV em diretório.

    Args:
        directory: Diretório a pesquisar.
        pattern: Padrão de glob para arquivos.

    Returns:
        Lista de caminhos para arquivos WAV.
    """
    if not directory.exists():
        return []
    return sorted(directory.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)


def ensure_directory(path: Path) -> None:
    """Garante que um diretório existe.

    Args:
        path: Caminho do diretório.
    """
    path.mkdir(parents=True, exist_ok=True)