import os

from config import ARTICLES_ROOT
from pathlib import Path
from PyPDF2 import PdfFileMerger


class Creator:
    def __init__(self, latest_dir: Path):
        self._latest_dir: Path = latest_dir

    def maybe_create(self):
        if not self._pdf_exists():
            self._create_pdf()

    def _pdf_exists(self):
        return self._pdf_path().exists()

    def _create_pdf(self):
        pdfs = sorted(self._latest_dir.iterdir(), key=os.path.getctime)
        merger = PdfFileMerger()

        for pdf in pdfs:
            if pdf.suffix == ".pdf":
                merger.append(str(pdf))

        merger.write(str(self._pdf_path()))
        merger.close()

    def _pdf_path(self) -> Path:
        pdf = self._latest_dir.name + ".pdf"
        return ARTICLES_ROOT / self._latest_dir / pdf


def create_latest():
    latest_dir: Path = next(filter(lambda p: p.is_dir(),
                                   sorted(Path(ARTICLES_ROOT).iterdir(), key=os.path.getctime, reverse=True)))
    Creator(latest_dir).maybe_create()
