import os
import requests
import openai
from PIL import Image
import base64
from io import BytesIO

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_article():
    prompt = (
        "Создай статью в стиле «Пазлы Истории» на 4000–5000 знаков. "
        "Атмосферный исторический рассказ на малоизвестную тему, "
        "документальная подача, плавный стиль."
    )

    resp = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    return resp["choices"][0]["message"]["content"]


def generate_image():
    prompt = (
        "high contrast black and white archival documentary photograph, "
        "realistic, historical, film grain, 1:1 ratio, authentic look"
    )

    result = openai.Image.create(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = result["data"][0]["b64_json"]
    return base64.b64decode(image_base64)


def send_photo_with_caption(photo_bytes, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"

    files = {"photo": ("image.jpg", photo_bytes, "image/jpeg")}
    data = {"chat_id": CHAT_ID, "caption": caption}

    requests.post(url, files=files, data=data)


def main():
    article = generate_article()
    photo = generate_image()
    send_photo_with_caption(photo, article)
    print("Готово.")


if __name__ == "__main__":
    main()
