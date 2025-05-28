import requests
from config import url, api_key

def send_to_ocr_api(processed_image_path):
    with open(processed_image_path, "rb") as image_file:
        return requests.post(
            url,
            files={"file": image_file},
            headers={"apikey": api_key},
            data={'OCREngine': '2'}
        )
