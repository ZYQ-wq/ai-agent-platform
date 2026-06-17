from app.core.database import SessionLocal
from app.models.knowledge import KnowledgeBase
from app.services.document_parser import parse_file
from app.services.text_splitter import split_text


def process_knowledge_file(user_id: int, file_path: str, file_name: str):

    db = SessionLocal()

    try:
        # 1. 解析文件
        text = parse_file(file_path)

        if not text:
            raise Exception("文件解析失败")

        # 2. 切片
        chunks = split_text(text)

        # 3. 存知识库主记录
        kb = KnowledgeBase(
            user_id=user_id,
            name=file_name,
            file_path=file_path,
            chunk_count=len(chunks)
        )

        db.add(kb)
        db.commit()
        db.refresh(kb)

        # 4. 存 chunk（下一步你会建表）
        # 暂时先打印
        for i, chunk in enumerate(chunks):
            print(f"[chunk {i}]: {chunk[:50]}")

        return kb

    finally:
        db.close()