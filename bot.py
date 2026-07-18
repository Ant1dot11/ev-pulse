from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

from config import TOKEN
from parser import get_latest_news
from editor import get_best_news
from article import get_article
from ai import create_post
from fact_checker import check_post
from config import USE_FACT_CHECKER
from publisher import publish
from logger import add_published
from database import (
    get_pending_post,
    update_pending_post_text,
    delete_pending_post,
)

# Сесії користувачів (тільки для інтерактивного /news, живе в пам'яті процесу)
user_sessions = {}
NEWS_BUTTON_TEXT = "🔎 Шукати новину"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 Вітаю!\n\n"
        "Я EV Pulse AI ⚡️\n\n"
        "Натисни кнопку внизу, щоб знайти найкращу новину дня 📰"
    )

    keyboard = ReplyKeyboardMarkup(
        [[NEWS_BUTTON_TEXT]],
        resize_keyboard=True,
    )

    await update.message.reply_text(text, reply_markup=keyboard)


def build_preview_text(best, post):
    preview = post.strip()

    if len(preview) > 900:
        preview = preview[:900]

    cut = preview.rfind("\n\n")
    if cut == -1:
        cut = preview.rfind(". ")
    if cut == -1:
        cut = preview.rfind(" ")
    if cut > 500:
        preview = preview[:cut]

    preview += "\n\n..."

    return (
        f"🏆 AI Score: {best['score']}/100\n\n"
        f"💬 {best['reason']}\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"{preview}\n\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "⬇️ Оберіть дію:"
    )


def build_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Опублікувати", callback_data="publish")],
        [InlineKeyboardButton("⏭️ Наступна", callback_data="next")],
        [InlineKeyboardButton("❌ Скасувати", callback_data="cancel")],
    ])


async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id

    msg = await update.message.reply_text("🔎 Шукаю новини...")

    news_list = get_latest_news(20)

    if not news_list:
        await msg.edit_text("❌ Новини не знайдено.")
        return

    await msg.edit_text("🧠 AI аналізує новини...")

    ranking = get_best_news(news_list)

    if not ranking:
        await msg.edit_text("❌ AI не зміг оцінити новини.")
        return

    best = ranking[0]

    selected = next(
        (item for item in news_list if item["title"] == best["title"]),
        None
    )

    if selected is None:
        await msg.edit_text("❌ Не вдалося знайти новину.")
        return

    await msg.edit_text("📖 Завантажую статтю...")

    data = get_article(selected["link"])
    article = data["text"]
    image = data["image"]

    if not article:
        await msg.edit_text("❌ Не вдалося отримати статтю.")
        return

    await msg.edit_text("🤖 Створюю пост...")

    post = create_post(selected["title"], article, selected["source"])

    user_sessions[user_id] = {
        "news": news_list,
        "ranking": ranking,
        "current": 0,
        "post": post,
        "link": selected["link"],
        "image": image,
    }

    await msg.edit_text(
        text=build_preview_text(best, post),
        reply_markup=build_keyboard(),
    )

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    print(f"❌ Помилка: {context.error}")

    if isinstance(update, Update) and update.effective_chat:

        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="⚠️ Сталася помилка (сервер AI тимчасово недоступний). Спробуй ще раз через хвилину.",
            )
        except Exception:
            pass


async def interactive_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id

    if user_id not in user_sessions:
        await query.edit_message_text("❌ Сесію завершено.")
        return

    session = user_sessions[user_id]

    if query.data == "publish":

        await publish(session["post"], session["image"])
        add_published(session["link"])

        await query.edit_message_text("✅ Новину успішно опубліковано!")
        del user_sessions[user_id]
        return

    if query.data == "cancel":
        await query.edit_message_text("❌ Скасовано.")
        del user_sessions[user_id]
        return

    if query.data == "next":

        session["current"] += 1

        if session["current"] >= len(session["ranking"]):
            await query.edit_message_text("✅ Більше новин немає.")
            del user_sessions[user_id]
            return

        best = session["ranking"][session["current"]]

        selected = next(
            (item for item in session["news"] if item["title"] == best["title"]),
            None
        )

        if selected is None:
            await query.edit_message_text("❌ Не вдалося знайти наступну новину.")
            return

        await query.edit_message_text("📖 Завантажую наступну статтю...")

        data = get_article(selected["link"])
        article = data["text"]
        image = data["image"]

        if not article:
            await query.edit_message_text("❌ Не вдалося отримати статтю.")
            return

        post = create_post(selected["title"], article, selected["source"])

        session["post"] = post
        session["link"] = selected["link"]
        session["image"] = image

        await query.edit_message_text(
            text=build_preview_text(best, post),
            reply_markup=build_keyboard(),
        )


async def review_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Кнопки для постів, які прийшли з cron-сценарію (main.py -> review.py)."""

    query = update.callback_query
    await query.answer()

    action, _, raw_id = query.data.partition(":")
    pending_id = int(raw_id)

    pending = get_pending_post(pending_id)

    if pending is None:
        await query.edit_message_reply_markup(None)
        await query.message.reply_text("❌ Цей пост уже оброблено або застарів.")
        return

    if action == "review_publish":

        await publish(pending["post"], pending["image"])

        add_published(
            pending["link"],
            pending["title"],
            pending["source"],
            pending["score"],
        )

        delete_pending_post(pending_id)

        await query.edit_message_reply_markup(None)
        await query.message.reply_text("✅ Опубліковано в канал.")

    elif action == "review_reject":

        delete_pending_post(pending_id)

        await query.edit_message_reply_markup(None)
        await query.message.reply_text("❌ Пост відхилено.")

    elif action == "review_regen":

        await query.message.reply_text("🔄 Перегенеровую...")

        new_post = create_post(
            pending["title"],
            pending["article"],
            pending["source"],
        )

        if USE_FACT_CHECKER and pending["score"] < 80:
            new_post = check_post(new_post)

        update_pending_post_text(pending_id, new_post)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Опублікувати", callback_data=f"review_publish:{pending_id}")],
            [InlineKeyboardButton("🔄 Перегенерувати", callback_data=f"review_regen:{pending_id}")],
            [InlineKeyboardButton("❌ Відхилити", callback_data=f"review_reject:{pending_id}")],
        ])

        if query.message.photo:
            await query.message.reply_photo(
                photo=pending["image"] or query.message.photo[-1].file_id,
                caption=new_post[:1024],
                reply_markup=keyboard,
            )
        else:
            await query.message.reply_text(
                new_post,
                reply_markup=keyboard,
            )


app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("news", news))
app.add_handler(MessageHandler(filters.Text([NEWS_BUTTON_TEXT]), news))
app.add_handler(CallbackQueryHandler(interactive_buttons, pattern="^(publish|next|cancel)$"))
app.add_handler(CallbackQueryHandler(review_buttons, pattern="^review_"))
app.add_error_handler(error_handler)

print("⚡️ EV Pulse AI запущений...")

app.run_polling()
