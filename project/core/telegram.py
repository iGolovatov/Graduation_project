import asyncio
from django.conf import settings
from telegram import Bot
from logging import getLogger

logger = getLogger(__name__)


def send_telegram_message(message_text):
    bot_token = settings.TELEGRAM_BOT_TOKEN
    chat_id = settings.TELEGRAM_CHAT_ID

    if not bot_token or not chat_id:
        logger.error('Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не настроен')
        return

    async def _send_message():
        bot = Bot(token=bot_token)
        async with bot:
            await bot.send_message(
                chat_id=chat_id,
                text=message_text,
                parse_mode='Markdown'
            )

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(_send_message())
    finally:
        loop.close()
