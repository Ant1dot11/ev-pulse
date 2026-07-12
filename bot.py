from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

from config import TOKEN
from parser import get_latest_news
from editor import get_best_news
from article import get_article
from ai import create_post
from publisher import publish
from logger import add_published


# Сесії користувачів
user_sessions = {}


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = (
        "👋 Вітаю!\n\n"
        "Я EV Pulse AI ⚡️\n\n"
        "Команди:\n\n"
        "/news — знайти найкращу новину дня 📰"
    )

    await update.message.reply_text(text)


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    msg = await update.message.reply_text(
        "🔎 Шукаю новини..."
    )

    news_list = get_latest_news(20)

    if not news_list:

        await msg.edit_text(
            "❌ Новини не знайдено."
        )

        return

    await msg.edit_text(
        "🧠 AI аналізує новини..."
    )

    ranking = get_best_news(news_list)

    if not ranking:

        await msg.edit_text(
            "❌ AI не зміг оцінити новини."
        )

        return

    best = ranking[0]

    selected = None

    for item in news_list:

        if item["title"] == best["title"]:
            selected = item
            break

    if selected is None:

        await msg.edit_text(
            "❌ Не вдалося знайти новину."
        )

        return

    title = selected["title"]
    link = selected["link"]
    source = selected["source"]

    await msg.edit_text(
        "📖 Завантажую статтю..."
    )

    data = get_article(link)

    article = data["text"]
    image = data["image"]

    if not article:

        await msg.edit_text(
            "❌ Не вдалося отримати статтю."
        )

        return

    await msg.edit_text(
        "🤖 Створюю пост..."
    )

    post = create_post(
        title,
        article,
        source,
    )
    user_sessions[user_id] = {
        "news": news_list,
        "ranking": ranking,
        "current": 0,
        "post": post,
        "link": link,
        "image": image,
    }

    keyboard = [
        [
            InlineKeyboardButton(
                "✅ Опублікувати",
                callback_data="publish",
            )
        ],
        [
            InlineKeyboardButton(
                "⏭️ Наступна",
                callback_data="next",
            )
        ],
        [
            InlineKeyboardButton(
                "❌ Скасувати",
                callback_data="cancel",
            )
        ],
    ]

    await msg.edit_text(
        text=(
            f"🏆 AI Score: {best['score']}/100\n\n"
            f"💬 {best['reason']}\n\n"
            f"{post}"
        ),
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_sessions:

        await query.edit_message_text(
            "❌ Сесію завершено."
        )

        return

    session = user_sessions[user_id]

    if query.data == "publish":

        await publish(
            session["post"],
            session["image"],
        )

        add_published(
            session["link"]
        )

        await query.edit_message_text(
            "✅ Новину успішно опубліковано!"
        )

        del user_sessions[user_id]

        return

    if query.data == "cancel":

        await query.edit_message_text(
            "❌ Скасовано."
        )

        del user_sessions[user_id]

        return
        if query.data == "next":

         session["current"] += 1

        if session["current"] >= len(session["ranking"]):

            await query.edit_message_text(
                "✅ Більше новин немає."
            )

            del user_sessions[user_id]

            return

        best = session["ranking"][session["current"]]

        selected = None

        for item in session["news"]:

            if item["title"] == best["title"]:
                selected = item
                break

        if selected is None:

            await query.edit_message_text(
                "❌ Не вдалося знайти наступну новину."
            )

            return

        title = selected["title"]
        link = selected["link"]
        source = selected["source"]

        await query.edit_message_text(
            "📖 Завантажую наступну статтю..."
        )

        data = get_article(link)

        article = data["text"]
        image = data["image"]

        if not article:

            await query.edit_message_text(
                "❌ Не вдалося отримати статтю."
            )

            return

        post = create_post(
            title,
            article,
            source,
        )

        session["post"] = post
        session["link"] = link
        session["image"] = image

        keyboard = [
            [
                InlineKeyboardButton(
                    "✅ Опублікувати",
                    callback_data="publish",
                )
            ],
            [
                InlineKeyboardButton(
                    "⏭️ Наступна",
                    callback_data="next",
                )
            ],
            [
                InlineKeyboardButton(
                    "❌ Скасувати",
                    callback_data="cancel",
                )
            ],
        ]

        await query.edit_message_text(
            text=(
                f"🏆 AI Score: {best['score']}/100\n\n"
                f"💬 {best['reason']}\n\n"
                f"{post}"
            ),
            reply_markup=InlineKeyboardMarkup(keyboard),
        )
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(
    CommandHandler(
        "start",
        start,
    )
)

app.add_handler(
    CommandHandler(
        "news",
        news,
    )
)

app.add_handler(
    CallbackQueryHandler(
        buttons,
    )
)

print("⚡️ EV Pulse AI запущений...")

app.run_polling()