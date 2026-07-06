from telegram import Bot
from config import TOKEN, CHANNEL_ID


async def publish(post):
    bot = Bot(token=TOKEN)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=post
    )