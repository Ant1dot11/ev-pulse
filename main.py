import asyncio

from pipeline import build_best_post
from review import send_for_review
from logger import is_published


async def main():

    result = build_best_post()

    if result is None:
        print("❌ Не вдалося створити пост.")
        return

    if is_published(result["link"]):
        print("✅ Ця новина вже була опублікована.")
        return

    print("📨 Відправляємо адміну...")

    await send_for_review(result)

    print("✅ Пост відправлено адміну!")


if __name__ == "__main__":
    asyncio.run(main())