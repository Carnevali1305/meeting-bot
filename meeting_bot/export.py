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
        try:
            from weasyprint import CSS, HTML
        except ImportError:
            output_path.write_text(f"[PDF export placeholder for {summary.title}]")
            return

        html_content = self._markdown_to_html(summary.to_markdown())
        css = CSS(string="""
            @page { size: A4; margin: 2cm; }
            body { font-family: sans-serif; line-height: 1.5; color: #333; }
            h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: .4em; }
            h2 { color: #34495e; margin-top: 1.4em; }
        """)
        HTML(string=html_content).write_pdf(str(output_path), stylesheets=[css])

    def _export_docx(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para DOCX usando python-docx."""
        try:
            from docx import Document
        except ImportError:
            output_path.write_text(f"[DOCX export placeholder for {summary.title}]")
            return

        doc = Document()
        doc.add_heading(summary.title, level=0)
        doc.add_paragraph(f"Data: {summary.datetime}")
        doc.add_paragraph(f"Duração: {summary.duration}")

        doc.add_heading("Tópicos Tratados", level=1)
        for topic in summary.topics:
            doc.add_paragraph(topic, style="List Bullet")

        doc.add_heading("Decisões Importantes", level=1)
        for decision in summary.decisions:
            doc.add_paragraph(decision, style="List Bullet")

        doc.add_heading("Ações Definidas", level=1)
        for action in summary.actions:
            owner = action.get("owner", "não especificado")
            task = action.get("task", "tarefa não definida")
            deadline = action.get("deadline", "em prazo")
            doc.add_paragraph(f"{owner} — {task} (até {deadline})", style="List Bullet")

        next_steps = getattr(summary, "next_steps", [])
        if next_steps:
            doc.add_heading("Próximos Passos", level=1)
            for step in next_steps:
                doc.add_paragraph(step, style="List Bullet")

        doc.add_paragraph("Gerado automaticamente pelo meeting-bot")
        doc.save(str(output_path))

    def _export_html(self, summary: MeetingSummary, output_path: Path) -> None:
        """Exporta para HTML."""
        html_content = self._markdown_to_html(summary.to_markdown())
        output_path.write_text(html_content, encoding="utf-8")

    def _markdown_to_html(self, markdown_text: str) -> str:
        """Converte Markdown básico para HTML com tags fechadas."""
        import html as html_mod
        import re

        def inline(text: str) -> str:
            text = html_mod.escape(text)
            text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
            text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
            return text

        lines = []
        in_list = False
        for line in markdown_text.split("\n"):
            if line.startswith("- "):
                if not in_list:
                    lines.append("<ul>")
                    in_list = True
                lines.append(f"<li>{inline(line[2:])}</li>")
                continue
            if in_list:
                lines.append("</ul>")
                in_list = False
            if line.startswith("## "):
                lines.append(f"<h2>{inline(line[3:])}</h2>")
            elif line.startswith("# "):
                lines.append(f"<h1>{inline(line[2:])}</h1>")
            elif line.startswith("---"):
                lines.append("<hr>")
            elif line.strip():
                lines.append(f"<p>{inline(line)}</p>")
        if in_list:
            lines.append("</ul>")

        body = "\n".join(lines)
        return f'<html><head><meta charset="utf-8"></head><body>{body}</body></html>'

    def export_multiple(self, summary: MeetingSummary, formats: List[ExportFormat]) -> List[Path]:
        """Exporta para múltiplos formatos."""
        return [self.export(summary, fmt) for fmt in formats]