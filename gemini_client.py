from google import genai
from google.genai.errors import ClientError

from config import GEMINI_KEYS, MODEL


def generate(prompt):

    last_error = None

    for i, key in enumerate(GEMINI_KEYS, start=1):

        print(f"🤖 Gemini: ключ {i}")

        try:

            client = genai.Client(api_key=key)

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
            )

            return response.text

        except ClientError as e:

            last_error = e
            error = str(e)

            if "RESOURCE_EXHAUSTED" in error:
                print(f"⚠️ Ключ {i}: закінчився ліміт")
                continue

            if "NOT_FOUND" in error:
                print(f"⚠️ Ключ {i}: модель недоступна")
                continue

            print(f"⚠️ Ключ {i}: {e}")
            continue

        except Exception as e:

            last_error = e
            print(f"⚠️ Ключ {i}: {e}")
            continue

    raise Exception(
        f"Усі API ключі недоступні.\n\n{last_error}"
    )