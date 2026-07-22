from pypdf import PdfReader
import io


def extract_text(filename: str, file_bytes: bytes) -> str:
    """
    Converts an uploaded file's raw bytes into plain text.
    Dispatches based on file extension — .txt is read directly as text,
    .pdf is parsed page by page and joined together.
    """
    if filename.lower().endswith(".pdf"):
        return _extract_pdf(file_bytes)
    return file_bytes.decode("utf-8")


def _extract_pdf(file_bytes: bytes) -> str:
    reader = PdfReader(io.BytesIO(file_bytes))
    pages = [page.extract_text() or "" for page in reader.pages]
    return "\n\n".join(pages)