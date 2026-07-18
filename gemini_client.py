import time
import json

from google import genai
from google.genai.errors import ClientError, ServerError

from config import GEMINI_KEYS, MODEL

MAX_RETRIES_PER_KEY = 5
RETRY_DELAY_SECONDS = 8


def generate(prompt):

    last_error = None

    for i, key in enumerate(GEMINI_KEYS, start=1):

        client = genai.Client(api_key=key)

        for attempt in range(1, MAX_RETRIES_PER_KEY + 1):

            print(f"🤖 Gemini: ключ {i}, спроба {attempt}")

            try:

                response = client.models.generate_content(
                    model=MODEL,
                    contents=prompt,
                )

                return response.text

            except ServerError as e:

                last_error = e
                print(f"⚠️ Ключ {i}: сервер недоступний (спроба {attempt}/{MAX_RETRIES_PER_KEY})")

                if attempt < MAX_RETRIES_PER_KEY:
                    time.sleep(RETRY_DELAY_SECONDS * attempt)
                    continue

                break

            except ClientError as e:

                last_error = e
                error = str(e)

                if "RESOURCE_EXHAUSTED" in error:
                    print(f"⚠️ Ключ {i}: закінчився ліміт")
                    break

                if "NOT_FOUND" in error:
                    print(f"⚠️ Ключ {i}: модель недоступна")
                    break

                print(f"⚠️ Ключ {i}: {e}")
                break

            except Exception as e:

                last_error = e
                print(f"⚠️ Ключ {i}: {e}")
                break

    raise Exception(
        f"Усі API ключі недоступні.\n\n{last_error}"
    )

def generate_json(prompt, max_json_retries=2):

 last_error = None

 for attempt in range(1, max_json_retries + 1):

        text = generate(prompt).strip()

        if text.startswith("```"):
            text = text.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            last_error = e
            print(f"⚠️ AI повернув невалідний JSON (спроба {attempt}/{max_json_retries}): {e}")

            raise Exception(
 f"AI кілька разів поспіль повернув невалідний JSON.\n\n{last_error}"
 )