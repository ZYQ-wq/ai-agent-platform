import os

from PyPDF2 import PdfReader
from docx import Document


# =========================
# PDF解析
# =========================
def parse_pdf(file_path: str) -> str:

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


# =========================
# DOCX解析
# =========================
def parse_docx(file_path: str) -> str:

    doc = Document(file_path)

    return "\n".join(
        para.text
        for para in doc.paragraphs
        if para.text.strip()
    )


# =========================
# TXT解析
# =========================
def parse_txt(file_path: str) -> str:

    with open(
        file_path,
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()


# =========================
# 文本清洗
# =========================
def clean_text(text: str) -> str:

    if not text:
        return ""

    # 去掉多余空格
    text = text.replace("\r", "")

    lines = []

    for line in text.split("\n"):

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


# =========================
# Chunk切分
# =========================
def split_text(
    text: str,
    chunk_size: int = 800,
    overlap: int = 150
) -> list[str]:

    chunks = []

    start = 0

    text_length = len(text)

    while start < text_length:

        end = start + chunk_size

        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)

        start += chunk_size - overlap

    return chunks


# =========================
# 文件统一入口
# =========================
def parse_file(file_path: str) -> list[str]:

    ext = os.path.splitext(file_path)[-1].lower()

    if ext == ".pdf":

        text = parse_pdf(file_path)

    elif ext == ".docx":

        text = parse_docx(file_path)

    elif ext == ".txt":

        text = parse_txt(file_path)

    else:

        raise Exception(
            f"不支持的文件类型: {ext}"
        )

    text = clean_text(text)

    chunks = split_text(
        text=text,
        chunk_size=800,
        overlap=150
    )

    return chunks