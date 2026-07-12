from telegram import InlineKeyboardButton, InlineKeyboardMarkup

from config import TOKEN, ADMIN_ID

from telegram import Bot

bot = Bot(token=TOKEN)


async def send_for_review(result):

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "✅ Опублікувати",
                callback_data="publish"
            )
        ],
        [
            InlineKeyboardButton(
                "🔄 Перегенерувати",
                callback_data="regen"
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Відхилити",
                callback_data="reject"
            )
        ]
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
            await bot.send_message(
                ADMIN_ID,
                text[1024:]
            )

    else:

        await bot.send_message(
            chat_id=ADMIN_ID,
            text=text,
            reply_markup=keyboard
        )