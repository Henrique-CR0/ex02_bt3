from src.graph.state import State

LIMITE_TEMPESTADE_KN = 12.0


def decide(state: State) -> dict:
    detalhes = []
    for n in state["frota"]["navios"]:
        if n["combustivel_t"] < n["reserva_t"]:
            detalhes.append({
                "id": n["id"],
                "situacao": f"bloqueado: {n['combustivel_t']} t < reserva de {n['reserva_t']} t",
                "vel": None,
                "eta": None,
            })
            continue
        vel = min(n["velocidade_kn"], LIMITE_TEMPESTADE_KN) if n["em_tempestade"] else n["velocidade_kn"]
        detalhes.append({
            "id": n["id"],
            "situacao": "tempestade" if n["em_tempestade"] else "ok",
            "vel": vel,
            "eta": round(n["distancia_nm"] / vel, 2),
        })

    elegiveis = [d for d in detalhes if d["eta"] is not None]
    if not elegiveis:
        return {"resposta_llm": {"detalhes": detalhes, "navio": None, "eta_horas": None}}
    vencedor = min(elegiveis, key=lambda d: d["eta"])
    return {"resposta_llm": {"detalhes": detalhes, "navio": vencedor["id"], "eta_horas": vencedor["eta"]}}