from sqlalchemy import select

from app.database import SessionLocal
from app.models import MessageModel


def save_message(
    telegram_user_id: int,
    username: str | None,
    message: str,
):
    db = SessionLocal()

    try:
        db_message = MessageModel(
            telegram_user_id=telegram_user_id,
            username=username,
            message=message,
        )

        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return db_message

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


def get_messages():
    db = SessionLocal()

    try:
        result = db.execute(
            select(MessageModel)
            .order_by(MessageModel.created_at)
        )

        return result.scalars().all()

    finally:
        db.close()
