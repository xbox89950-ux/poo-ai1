"""PDF reading utility"""
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

class PDFReader:
    @staticmethod
    def read_pdf(path: str, pages: Optional[int] = None) -> str:
        try:
            import PyPDF2
            with open(path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                total = len(reader.pages)
                read_pages = pages if pages else min(5, total)
                text = []
                for i in range(min(read_pages, total)):
                    page = reader.pages[i]
                    text.append(page.extract_text())
                return f"PDF ({total} pages) - First {read_pages} pages:\n" + "\n".join(text)
        except ImportError:
            return "PyPDF2 not installed. Run: pip install PyPDF2"
        except Exception as e:
            return f"PDF error: {e}"

    @staticmethod
    def summarize_pdf(path: str) -> str:
        content = PDFReader.read_pdf(path, pages=3)
        if content.startswith("PDF"):
            lines = content.split("\n")[1:]
            return "Summary (first 3 pages):\n" + "\n".join(lines[:50])
        return content
