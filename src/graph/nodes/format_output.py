from src.graph.state import State


def format_output(state: State) -> dict:
    nota = state.get("nota_operador", "")
    if state.get("aprovado"):
        texto = f"APROVADO pelo operador.\n{state['recomendacao']}"
    else:
        texto = "REJEITADO pelo operador."
    if nota:
        texto += f"\nNota do operador: {nota}"
    return {"resultado": texto}