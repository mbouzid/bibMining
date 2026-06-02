from pathlib import Path
import requests
from typing import Tuple
import bibtexparser


GROBID_DEFAULT_URL: str = "http://localhost:8070"

class GrobidClient:
    def __init__(self, url: str = GROBID_DEFAULT_URL):
        self.url = url.rstrip("/")

    def process_header(self, pdf_path: str | Path) -> str:
        endpoint = f"{self.url}/api/processHeaderDocument"

        pdf_path = Path(pdf_path)
        with open(pdf_path, "rb") as pdf_file:

            response = requests.post(
                endpoint,
                files={"input": pdf_file},
                timeout=300,
            )

        response.raise_for_status()

        return response.text

    def process_pdf(self, pdf_path: str | Path) -> str:

        pdf_path = Path(pdf_path)

        endpoint = f"{self.url}/api/processFulltextDocument" # processFulltextDocument

        with open(pdf_path, "rb") as pdf_file:

            response = requests.post(
                endpoint,
                files={"input": pdf_file},
                timeout=300,
            )

        response.raise_for_status()

        return response.text

    def process_and_save(self, pdf_path: str | Path, output_path: str | Path) -> Path:

        pdf_path = Path(pdf_path)
        output_path = Path(output_path)

        tei_xml = self.process_pdf(pdf_path)
        
        output_path.write_text(tei_xml, encoding="utf-8")

        return output_path