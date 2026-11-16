"""Módulo de transcrição usando Whisper."""

from pathlib import Path
from typing import Callable, Dict, Any, Optional

# Cache de modelos carregados
_MODEL_CACHE: Optional[object] = None


class Transcriber:
    """Gerencia a transcrição de áudio usando Whisper."""

    def __init__(
        self,
        model_name: str = "small",
        device: str = "auto",
        model_factory: Optional[Callable[[], Any]] = None,
    ):
        """Inicializa o transcritor.

        Args:
            model_name: Nome do modelo Whisper (tiny, base, small, medium, large).
            device: Dispositivo para processing (auto, cpu, cuda).
            model_factory: Fábrica opcional para injetar modelo fake em testes.
        """
        from .utils import ensure_directory

        self.model_name = model_name
        self.device = device
        self._model_factory = model_factory
        self._model: Optional[Any] = None

    def transcribe(self, audio_path: Path) -> str:
        """Transcreve um arquivo de áudio.

        Args:
            audio_path: Caminho para o arquivo de áudio.

        Returns:
            Texto transcrito.
        """
        try:
            model = self.load_model()
            if model is None:
                return f"[Transcrição simulada para {audio_path.name}]"

            segments, _ = model.transcribe(str(audio_path))
            return "\n".join([seg.text for seg in segments])

        except ImportError:
            # faster-whisper não instalado
            return f"[Transcrição simulada para {audio_path.name}]"
        except Exception as e:
            # Fallback para outros erros
            return f"[Transcrição simulada para {audio_path.name}]"

    def transcribe_with_details(self, audio_path: Path) -> Dict[str, Any]:
        """Transcreve com detalhes adicionais.

        Args:
            audio_path: Caminho para o arquivo de áudio.

        Returns:
            Dicionário com texto, língua e timestamps.
        """
        try:
            model = self.load_model()
            if model is None:
                return {
                    "text": f"[Transcrição simulada para {audio_path.name}]",
                    "language": "pt",
                    "segments": [],
                }

            segments, info = model.transcribe(str(audio_path))
            segments_list = [
                {
                    "text": seg.text,
                    "start": seg.start,
                    "end": seg.end,
                }
                for seg in segments
            ]

            return {
                "text": "\n".join([seg.text for seg in segments]),
                "language": info.language,
                "segments": segments_list,
            }

        except ImportError:
            return {
                "text": f"[Transcrição simulada para {audio_path.name}]",
                "language": "pt",
                "segments": [],
            }
        except Exception:
            return {
                "text": f"[Transcrição simulada para {audio_path.name}]",
                "language": "pt",
                "segments": [],
            }

    def load_model(self) -> Optional[Any]:
        """Carrega o modelo Whisper (lazy loading).

        Returns:
            Modelo Whisper carregado, ou None se não disponível.
        """
        global _MODEL_CACHE

        if self._model is not None:
            return self._model

        # Usar fábrica injetada (para testes)
        if self._model_factory is not None:
            self._model = self._model_factory()
            return self._model

        # Carregar modelo real
        try:
            from faster_whisper import WhisperModel

            _MODEL_CACHE = WhisperModel(
                self.model_name,
                device=self.device,
            )
            self._model = _MODEL_CACHE
            return self._model

        except ImportError:
            return None
        except Exception:
            return None

    def validate_transcript(self, transcript: str) -> bool:
        """Valida se o transcript é adequado para processamento.

        Args:
            transcript: Texto a validar.

        Returns:
            True se o transcript tem mais de 50 caracteres.
        """
        return len(transcript.strip()) > 50


def get_whisper_model(model_name: str = "small", device: str = "auto") -> Optional[Any]:
    """Obtém um modelo Whisper compartilhado.

    Args:
        model_name: Nome do modelo Whisper.
        device: Dispositivo para processing.

    Returns:
        Modelo Whisper carregado, ou None se não disponível.
    """
    global _MODEL_CACHE

    if _MODEL_CACHE is not None:
        return _MODEL_CACHE

    try:
        from faster_whisper import WhisperModel

        _MODEL_CACHE = WhisperModel(model_name, device=device)
        return _MODEL_CACHE
    except ImportError:
        return None
    except Exception:
        return None
