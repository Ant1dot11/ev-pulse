from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Bot

from config import TOKEN, ADMIN_ID
from database import create_pending_post

bot = Bot(token=TOKEN)


async def send_for_review(result):

    pending_id = create_pending_post(
        link=result["link"],
        title=result["title"],
        source=result["source"],
        score=result["score"],
        image=result.get("image", ""),
        article=result.get("article", ""),
        post=result["post"],
    )

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Опублікувати", callback_data=f"review_publish:{pending_id}")],
        [InlineKeyboardButton("🔄 Перегенерувати", callback_data=f"review_regen:{pending_id}")],
        [InlineKeyboardButton("❌ Відхилити", callback_data=f"review_reject:{pending_id}")],
    ])

    text = result["post"]

    if result["image"]:

        await bot.send_photo(
            chat_id=ADMIN_ID,
            photo=result["image"],
            caption=text[:1024],
            reply_markup=keyboard
        )

        if len(text) > 1024:
            await bot.send_message(ADMIN_ID, text[1024:])

    else:

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=text,
            reply_markup=keyboard
        )