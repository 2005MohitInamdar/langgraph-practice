from langgraph.graph import StateGraph, MessagesState, START, END
from langchain.chat_models import init_chat_model
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.tools import tool
from typing import TypedDict
from dotenv import load_dotenv
import os
import requests
from IPython.display import Image, display


load_dotenv()

url = "https://openrouter.ai/api/v1/chat/completions"

model = ChatOpenAI(
    model="allenai/molmo-2-8b:free",
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    streaming=True,
    temperature=0.8
)

class State(TypedDict):
    question:str
    answer:str

def generate_question(state:State) -> State:
    """Generate a soft skill interview question."""
    question=[]
    for token in model.stream("Generate a soft skill interview question"):
        print(token.content, end="", flush=True)
        question.append(token.content)
    print()
    return {"question" : "".join(question)}
    
def generate_answer(state:State) -> State:
    """Answer the given interview question."""
    question = state["question"]
    answer = []
    for token in model.stream(f"Answer this interview question: {question}"):
        print(token.content, end="", flush=True)
        answer.append(token.content)
    print()
    print("QUestion Printed from state: ", question)
    print("answer Printed from state: ", "".join(answer))
    return {"answer" : "".join(answer)}


workflow = StateGraph(State)
workflow.add_node("generate_question", generate_question)
workflow.add_node("generate_answer", generate_answer)

workflow.add_edge(START, "generate_question")
workflow.add_edge("generate_question", "generate_answer")
workflow.add_edge("generate_answer", END)

chain = workflow.compile()

final_state = {}

for state_update in chain.stream({}):
    if "question" in state_update:
        final_state["question"] = state_update["question"]
    if "answer" in state_update:
        final_state["answer"] = state_update["answer"]

print("\nFinal Question:", final_state.get("question"))
print("Final Answer:", final_state.get("answer"))