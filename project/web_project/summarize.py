import requests
from django.conf import settings

YANDEX_GPT_API_URL = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"


def summarize_text(text: str) -> str:
    """
    Генерирует краткий пересказ текста через YandexGPT.
    """
    headers = {
        "Authorization": f"Api-Key {settings.YANDEX_API_KEY}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Сделай краткий пересказ следующей статьи на русском языке, выделив основные идеи и выводы.
    Текст статьи:
    {text[:5000]}  # Ограничение длины
    """

    payload = {
        "modelUri": f"gpt://{settings.YANDEX_FOLDER_ID}/yandexgpt-lite/latest",
        "completionOptions": {
            "stream": False,
            "temperature": 0.3,
            "maxTokens": "1000"
        },
        "messages": [
            {
                "role": "system",
                "text": "Ты — помощник, который делает краткие и понятные пересказы статей."
            },
            {
                "role": "user",
                "text": prompt
            }
        ]
    }

    try:
        response = requests.post(YANDEX_GPT_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        summary = result['result']['alternatives'][0]['message']['text']
        return summary.strip()
    except Exception as e:
        return f"[Ошибка при генерации пересказа: {str(e)}]"
