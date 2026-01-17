from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="allenai/molmo-2-8b:free",
    model_provider="openai",
    base_url="https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENAI_API_KEY")
)

class State():
    question:list[str] = []
    answer:list[str] = []

def instructions(state : State) -> State:
    """Type of questions we have to generate"""
    
