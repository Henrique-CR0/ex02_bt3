from src.graph.prompts.rules_prompt import RULES_PROMPT
from src.graph.state import State
from src.utils.llm_adapter import get_llm


def answer_rules(state: State) -> dict:
    resposta = (RULES_PROMPT | get_llm()).invoke({"pergunta": state["pergunta"]})
    return {"resultado": str(resposta.content)}