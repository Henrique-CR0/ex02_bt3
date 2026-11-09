import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

load_dotenv()


def get_llm(temperature: float = 0):
    return init_chat_model(
        model=os.environ["LLM_MODEL"],
        model_provider=os.environ["LLM_PROVIDER"],
        temperature=temperature,
    )