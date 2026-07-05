from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)
from config import TOKEN


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Вітаю!\n\n"
        "Я Pulse AI — помічник проєкту EV Pulse Україна. ⚡️\n\n"
        "Поки що я навчаюся, але зовсім скоро зможу:\n"
        "🚗 знаходити новини про електромобілі;\n"
        "📰 готувати короткі огляди;\n"
        "🇺🇦 перекладати їх українською;\n"
        "📢 допомагати з публікаціями.\n\n"
        "Дякую, що ви з нами! 💙💛"
    )

    await update.message.reply_text(text)


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

print("⚡️ Pulse AI запущений...")

app.run_polling()