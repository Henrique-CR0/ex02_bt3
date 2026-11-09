from langchain_core.messages import HumanMessage

from src.graph.checks import verificar
from src.graph.state import State

MAX_TENTATIVAS = 2


def validate(state: State) -> dict:
    msgs = state["messages"]
    texto = msgs[-1].content if msgs else ""
    problemas = verificar(state["frota"], msgs, texto)
    tentativas = state.get("tentativas", 0)

    if problemas and tentativas < MAX_TENTATIVAS:
        aviso = HumanMessage(
            content=(
                "Validação automática: faltou "
                + "; ".join(problemas)
                + ". Chame as ferramentas que faltam (sem calcular de cabeça) "
                "e depois refaça a resposta final."
            )
        )
        return {
            "messages": [aviso],
            "tentativas": tentativas + 1,
            "problemas": problemas,
            "tentar_de_novo": True,
        }
    return {"problemas": problemas, "tentar_de_novo": False}


def route_validate(state: State) -> str:
    return "analyze" if state.get("tentar_de_novo") else "human_review"