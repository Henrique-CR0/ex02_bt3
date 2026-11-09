from typing import Literal

from pydantic import BaseModel

from src.graph.prompts.classify_prompt import CLASSIFY_PROMPT
from src.graph.state import State
from src.utils.llm_adapter import get_llm


class Intencao(BaseModel):
    intent: Literal["primeiro_a_chegar", "regras", "fora_escopo"]


def classify(state: State) -> dict:
    chain = CLASSIFY_PROMPT | get_llm().with_structured_output(Intencao)
    return {"intent": chain.invoke({"pergunta": state["pergunta"]}).intent}