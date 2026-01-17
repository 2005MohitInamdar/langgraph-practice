import requests
from dotenv import load_dotenv
import os

load_dotenv()
url = "https://openrouter.ai/api/v1/models"

headers = {"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"}

response = requests.get(url, headers=headers)

model = response.json()["data"]
model_id = [m["id"] for m in model]

for x in model_id:
    print(x)