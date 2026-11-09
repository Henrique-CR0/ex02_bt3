from src.graph.state import State


def format_output(state: State) -> dict:
    r = state["resposta_llm"]
    linhas = [
        "| Navio | Situação | Vel. efetiva (kn) | ETA (h) |",
        "|---|---|---:|---:|",
    ]
    for d in r["detalhes"]:
        vel = "-" if d["vel"] is None else d["vel"]
        eta = "-" if d["eta"] is None else f"{d['eta']:.2f}"
        linhas.append(f"| {d['id']} | {d['situacao']} | {vel} | {eta} |")

    if r["navio"]:
        texto = f"O navio que chega primeiro é o {r['navio']}, com ETA de {r['eta_horas']:.2f} horas."
    else:
        texto = "Nenhum navio elegível: todos estão bloqueados."
    return {"resultado": f"Pergunta: {state['pergunta']}\nResposta:\n" + "\n".join(linhas) + "\n\n" + texto}