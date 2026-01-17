from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.chat_models import init_chat_model
from langchain.tools import tool
from typing import TypedDict
from dotenv import load_dotenv
import os
import requests
from IPython.display import Image, display

load_dotenv()

url = "https://openrouter.ai/api/v1/chat/completions"

model = init_chat_model(
    model = "allenai/molmo-2-8b:free",
    model_provider = "openai",
    base_url = "https://openrouter.ai/api/v1",
    api_key = os.getenv("OPENAI_API_KEY"),
)

class State(TypedDict):
    question:str
    answer:str

def generate_question(state:State) -> State:
    """Generate a soft skill interview question."""
    response = model.invoke("Generate a soft skill interview question")
    return {"question" : response.content}
    
def generate_answer(state:State) -> State:
    """Answer the given interview question."""
    question = state["question"]
    response = model.invoke(f"Answer this interview question: {question}")
    return {"answer" : response.content}

workflow = StateGraph(State)
workflow.add_node("generate_question", generate_question)
workflow.add_node("generate_answer", generate_answer)

workflow.add_edge(START, "generate_question")
workflow.add_edge("generate_question", "generate_answer")
workflow.add_edge("generate_answer", END)

chain = workflow.compile()
result = chain.invoke({})
print(result["question"])
print(result["answer"])
