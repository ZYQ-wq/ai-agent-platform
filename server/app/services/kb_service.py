from datetime import datetime

from app.core.database import SessionLocal
from app.models.knowledge import Knowledge
from app.models.knowledge_file import KnowledgeFile
from app.models.knowledge_chunks import KnowledgeChunk

from app.core.file_storage import save_file
from app.services.document_parser import parse_file
from sqlalchemy import func
from app.services.embedding_service import get_embedding


# =========================
# 1️⃣ 创建知识库
# =========================
def create_kb_service(user_id: str, name: str, description: str):

    db = SessionLocal()

    try:

        kb = Knowledge(
            user_id=user_id,
            name=name,
            description=description,
            created_at=datetime.utcnow()
        )

        db.add(kb)
        db.commit()
        db.refresh(kb)

        return kb

    finally:
        db.close()


# =========================
# 2️⃣ 上传文件 + 切片（核心升级）
# =========================
def upload_kb_service(file, user_id: str, kb_id: int):

    db = SessionLocal()

    try:

        # 1️⃣ 保存文件
        file_path = save_file(file)

        # 2️⃣ 创建文件记录（KBFile）
        kb_file = KnowledgeFile(
            knowledge_id=kb_id,
            file_name=file.filename,
            file_path=file_path,
            file_type=file.filename.split(".")[-1],
            created_at=datetime.utcnow()
        )

        db.add(kb_file)
        db.commit()
        db.refresh(kb_file)

        # 3️⃣ 解析文件（得到文本）
        chunks = parse_file(file_path)

        # 4️⃣ 写入 chunk
        chunk_objs = []

        for i, text in enumerate(chunks):

            vector = get_embedding(text)

            if not vector:
                raise ValueError(
                    f"第 {i + 1} 个切片向量化失败，请检查 Embedding 配置"
                )

            chunk = KnowledgeChunk(
                knowledge_id=kb_id,
                file_id=kb_file.id,
                content=text,
                chunk_index=i,
                embedding=vector
            )

            db.add(chunk)
            chunk_objs.append({
                "chunk_index": i,
                "content": text
            })

        db.commit()

        return {
            "kb_id": kb_id,
            "file_id": kb_file.id,
            "file_name": file.filename,
            "chunks_count": len(chunk_objs),
            "chunks": chunk_objs
        }

    finally:
        db.close()


# =========================
# 3️⃣ KB列表
# =========================
def list_kb_service(user_id: str):

    db = SessionLocal()

    try:

        return db.query(Knowledge).filter(
            Knowledge.user_id == user_id
        ).all()

    finally:
        db.close()


# =========================
# 4️⃣ KB详情（带文件列表）
# =========================
def get_kb_service(kb_id: int, user_id: str):

    db = SessionLocal()

    try:

        kb = db.query(Knowledge).filter(
            Knowledge.id == kb_id,
            Knowledge.user_id == user_id
        ).first()

        if not kb:
            return None

        files = db.query(KnowledgeFile).filter(
            KnowledgeFile.knowledge_id == kb_id
        ).all()

        file_list = []

        for file in files:

            # 当前文件对应的Chunk数量
            chunk_count = db.query(
                func.count(KnowledgeChunk.id)
            ).filter(
                KnowledgeChunk.file_id == file.id
            ).scalar()

            file_list.append({
                "id": file.id,
                "file_name": file.file_name,
                "file_type": file.file_type,
                "file_path": file.file_path,
                "created_at": file.created_at,

                # 后续接入训练任务时再改
                "pending": 0,
                "trained": chunk_count,
                "total": chunk_count
            })

        return {
            "kb": kb,
            "files": file_list
        }

    finally:
        db.close()

# =========================
# 5️⃣ 更新KB
# =========================
def update_kb_service(kb_id: int, user_id: str, name: str, description: str):

    db = SessionLocal()

    try:

        kb = db.query(Knowledge).filter(
            Knowledge.id == kb_id,
            Knowledge.user_id == user_id
        ).first()

        if not kb:
            return None

        kb.name = name
        kb.description = description

        db.commit()
        db.refresh(kb)

        return kb

    finally:
        db.close()


# =========================
# 6️⃣ 删除KB（级联删除）
# =========================
def delete_kb_service(kb_id: int, user_id: str):

    db = SessionLocal()

    try:

        kb = db.query(Knowledge).filter(
            Knowledge.id == kb_id,
            Knowledge.user_id == user_id
        ).first()

        if not kb:
            return False

        # 删除 chunks
        db.query(KnowledgeChunk).filter(
            KnowledgeChunk.knowledge_id == kb_id
        ).delete()

        # 删除 files
        db.query(KnowledgeFile).filter(
            KnowledgeFile.knowledge_id == kb_id
        ).delete()

        # 删除 kb
        db.delete(kb)

        db.commit()

        return True

    finally:
        db.close()

def delete_kb_file_service(file_id: int):

    db = SessionLocal()

    try:

        file = db.query(KnowledgeFile).filter(
            KnowledgeFile.id == file_id
        ).first()

        if not file:
            return False

        db.query(KnowledgeChunk).filter(
            KnowledgeChunk.file_id == file_id
        ).delete()

        db.delete(file)

        db.commit()

        return True

    finally:
        db.close()