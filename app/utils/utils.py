import os
import requests
from dotenv import load_dotenv

load_dotenv()

url = os.getenv("CALORIES_URL")
APP_ID = os.getenv("APP_ID")
API_KEY = os.getenv("API_KEY")

headers = {"Content-Type": "application/json", "x-app-id": APP_ID, "x-app-key": API_KEY}


def get_calories(text: str):
    data = {"query": text}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return 0
    result = response.json().get("foods")
    calories = 0
    for food in result:
        calories = calories + food.get("nf_calories")
    return int(calories)
