"""Módulo de exportação para múltiplos formatos."""

from pathlib import Path
from typing import Optional, List
from enum import Enum

from .summarize import MeetingSummary


class ExportFormat(Enum):
    """Formatos de exportação suportados."""
    MARKDOWN = "md"
    PDF = "pdf"
    DOCX = "docx"
    HTML = "html"


class Exporter:
    """Gerencia exportação de resumos para diferentes formatos."""

    def __init__(self, output_dir: Optional[Path] = None):
        """Inicializa o exportador.

        Args:
            output_dir: Diretório para salvar os arquivos exportados.
        """
        from .utils import ensure_directory

        self.output_dir = output_dir or Path.cwd() / "exports"
        ensure_directory(self.output_dir)

    def export(self, summary: MeetingSummary, output_format: ExportFormat) -> Path:
        """Exporta o resumo para o formato especificado.

        Args:
            summary: Resumo da reunião.
            output_format: Formato de saída.

        Returns:
            Caminho para o arquivo exportado.
        """
        from .utils import sanitize_filename

        safe_title = sanitize_filename(summary.title)
        filename = f"{safe_title}.{output_format.value}"
        output_path = self.output_dir / filename

        if output_format == ExportFormat.MARKDOWN:
            self._export_markdown(summary, output_path)
        elif output_format == ExportFormat.PDF:
            self._export_pdf(summary, output_path)
        elif output_format == ExportFormat.DOCX:
            self._export_docx(summary, output_path)
        elif output_format == ExportFormat.HTML:
            self._export_html(summary, output_path)

        return output_path

    def _export_markdown(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para Markdown."""
        output_path.write_text(summary.to_markdown(), encoding="utf-8")

    def _export_pdf(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para PDF usando WeasyPrint."""
        # TODO: Implementar com weasyprint
        html_content = self._markdown_to_html(summary.to_markdown())
        # from weasyprint import HTML
        # HTML(string=html_content).write_pdf(str(output_path))

        # Placeholder
        output_path.write_text(f"[PDF export placeholder for {summary.title}]")

    def _export_docx(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para DOCX usando python-docx."""
        # TODO: Implementar com python-docx
        # from docx import Document
        # doc = Document()
        # doc.add_heading(summary.title, 0)
        # ...

        # Placeholder
        output_path.write_text(f"[DOCX export placeholder for {summary.title}]")

    def _export_html(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para HTML."""
        html_content = self._markdown_to_html(summary.to_markdown())
        output_path.write_text(html_content, encoding="utf-8")

    def _markdown_to_html(self, markdown_text: str) -> str:
        """Converte Markdown básico para HTML."""
        # Conversão simplificada - substituir por markdown-it-py quando possível
        html = markdown_text.replace("\n\n", "</p><p>")
        html = html.replace("# ", "<h1>")
        html = html.replace("## ", "<h2>")
        html = html.replace("**", "<strong>")
        html = html.replace("`", "<code>")
        html = f"<html><body><pre>{html}</pre></body></html>"
        return html

    def export_multiple(self, summary: MeetingSummary, formats: List[ExportFormat]) -> List[Path]:
        """Exporta para múltiplos formatos."""
        return [self.export(summary, fmt) for fmt in formats]