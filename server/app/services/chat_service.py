from sqlalchemy.orm import Session
from app.models.memory import Memory

def save_message(db: Session, user_id: int, role: str, content: str):
    db_message = Memory(user_id=user_id, role=role, content=content)
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

def get_history(db: Session, user_id: int, limit: int = 20):
    return db.query(Memory).filter(Memory.user_id == user_id).order_by(Memory.id.desc()).limit(limit).all()