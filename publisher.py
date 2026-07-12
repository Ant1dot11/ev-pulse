import os
import tempfile
import requests

from telegram import Bot

from config import TOKEN, CHANNEL_ID, ADMIN_ID

bot = Bot(token=TOKEN)


def split_text(text, size=4096):
    parts = []

    while len(text) > size:

        pos = text.rfind("\n", 0, size)

        if pos == -1:
            pos = text.rfind(" ", 0, size)

        if pos == -1:
            pos = size

        parts.append(text[:pos].strip())
        text = text[pos:].strip()

    if text:
        parts.append(text)

    return parts


async def publish(post, image_url=None):
    await send(post, CHANNEL_ID, image_url)


async def send_to_admin(post, image_url=None):
    await send(post, ADMIN_ID, image_url)


async def send(post, chat_id, image_url=None):

    # Если фото нет
    if not image_url:

        for part in split_text(post):
            await bot.send_message(
                chat_id=chat_id,
                text=part,
            )

        return

    temp_path = None

    try:

        response = requests.get(
            image_url,
            timeout=20,
            headers={
                "User-Agent": "Mozilla/5.0"
            }
        )

        response.raise_for_status()

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".jpg"
        ) as file:

            file.write(response.content)
            temp_path = file.name

        with open(temp_path, "rb") as photo:

            # Если подпись помещается
            if len(post) <= 1024:

                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=post,
                )

            else:

                caption = post[:1024]

                cut = caption.rfind("\n")

                if cut == -1:
                    cut = caption.rfind(" ")

                if cut > 700:
                    caption = caption[:cut]

                await bot.send_photo(
                    chat_id=chat_id,
                    photo=photo,
                    caption=caption,
                )

                rest = post[len(caption):].strip()

                for part in split_text(rest):
                    await bot.send_message(
                        chat_id=chat_id,
                        text=part,
                    )

    except Exception as e:

        print(f"❌ Не вдалося завантажити фото: {e}")

        for part in split_text(post):
            await bot.send_message(
                chat_id=chat_id,
                text=part,
            )

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)