from langgraph.types import interrupt

from src.graph.state import State


def human_review(state: State) -> dict:
    recomendacao = str(state["messages"][-1].content)
    decisao = interrupt(
        {"recomendacao": recomendacao, "pergunta": "Aprovar a recomendação?"}
    )
    return {
        "recomendacao": recomendacao,
        "aprovado": bool(decisao["aprovado"]),
        "nota_operador": decisao.get("nota", ""),
    }