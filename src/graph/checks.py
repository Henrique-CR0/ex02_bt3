from src.graph.tools import LIMITE_TEMPESTADE_KN


def esperado(frota: dict) -> dict:
    bloqueados, etas = [], {}
    for n in frota["navios"]:
        if n["combustivel_t"] < n["reserva_t"]:
            bloqueados.append(n["id"])
            continue
        vel = min(n["velocidade_kn"], LIMITE_TEMPESTADE_KN) if n["em_tempestade"] else n["velocidade_kn"]
        etas[n["id"]] = round(n["distancia_nm"] / vel, 2)
    vencedor = min(etas, key=etas.get) if etas else None
    return {"bloqueados": bloqueados, "etas": etas, "vencedor": vencedor}


def verificar(frota: dict, mensagens: list, texto_final: str) -> list[str]:
    esp = esperado(frota)
    chamadas = []
    for m in mensagens:
        for c in getattr(m, "tool_calls", None) or []:
            chamadas.append((c["name"], c["args"]))

    reservas = {(a.get("combustivel_t"), a.get("reserva_t")) for nome, a in chamadas if nome == "reserva_ok"}
    etas = {(a.get("distancia_nm"), a.get("velocidade_kn")) for nome, a in chamadas if nome == "calcular_eta_horas"}

    problemas = []
    for n in frota["navios"]:
        if (n["combustivel_t"], n["reserva_t"]) not in reservas:
            problemas.append(f"falta reserva_ok para {n['id']}")
        if n["id"] in esp["etas"]:
            vel = min(n["velocidade_kn"], LIMITE_TEMPESTADE_KN) if n["em_tempestade"] else n["velocidade_kn"]
            if (n["distancia_nm"], vel) not in etas:
                problemas.append(f"falta calcular_eta_horas para {n['id']} (velocidade efetiva {vel})")

    texto = str(texto_final).replace("\u2011", "-").replace("\u2010", "-")
    if esp["vencedor"] and esp["vencedor"] not in texto:
        problemas.append(f"a resposta final não cita o vencedor {esp['vencedor']}")
    return problemas