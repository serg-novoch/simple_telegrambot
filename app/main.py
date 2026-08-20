import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from dotenv import load_dotenv
from sqlalchemy import select

from app.database import SessionLocal, init_db
from app.models import MessageModel


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is not set")


dp = Dispatcher()


@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Привет! Я учебный DevOps-бот."
    )


@dp.message(Command("history"))
async def messages_handler(message: Message):
    db = SessionLocal()

    try:
        result = db.execute(
            select(MessageModel)
            .order_by(MessageModel.created_at)
        )

        messages = result.scalars().all()

        if not messages:
            await message.answer("Сообщений пока нет.")
            return

        response = []

        for msg in messages:
            response.append(
                f"{msg.id}. "
                f"[{msg.created_at:%Y-%m-%d %H:%M:%S}] "
                f"{msg.message}"
            )

        await message.answer("\n".join(response))

    finally:
        db.close()

@dp.message()
async def message_handler(message: Message):
    if message.text is None:
        await message.answer("Я пока умею сохранять только текстовые сообщения.")
        return

    db = SessionLocal()

    try:
        db_message = MessageModel(
            telegram_user_id=message.from_user.id,
            username=message.from_user.username,
            message=message.text,
        )

        db.add(db_message)
        db.commit()

        await message.answer("Сообщение сохранено.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


async def main():
    init_db()

    bot = Bot(token=BOT_TOKEN)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
