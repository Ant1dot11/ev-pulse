from telegram import Update
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    ContextTypes,
)

from config import TOKEN
from publisher import publish


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    if query.data == "publish":

        text = query.message.caption or query.message.text

        photo = None

        if query.message.photo:
            photo = query.message.photo[-1].file_id

        await publish(text, photo)

        await query.edit_message_reply_markup(None)

        await query.message.reply_text("✅ Опубліковано в канал.")

    elif query.data == "reject":

        await query.edit_message_reply_markup(None)

        await query.message.reply_text("❌ Пост відхилено.")

    elif query.data == "regen":

        await query.edit_message_reply_markup(None)

        await query.message.reply_text("🔄 Перегенерація поки що в розробці.")


app = Application.builder().token(TOKEN).build()

app.add_handler(
    CallbackQueryHandler(buttons)
)

print("✅ Admin Bot запущено")

app.run_polling()