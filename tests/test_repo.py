from app.repository import save_message

def test_save_message():
    message = save_message(
        telegram_user_id=123,
        username="test",
        message="Hello",
    )

    assert message.id is not None
    assert message.message == "Hello"
    assert message.telegram_user_id == 123
