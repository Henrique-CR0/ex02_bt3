import os
import sys
import time
import uuid

from src.graph.builder import build_graph

N = int(sys.argv[1]) if len(sys.argv) > 1 else 5
PERGUNTA = "Qual navio chega primeiro?"
ETA_ESPERADO = {760, 680, 820}
COMB_ESPERADO = {30, 100, 115, 145}


def norm(texto):
    return str(texto).replace("\u2011", "-").replace("\u2010", "-")


g = build_graph()
print(f"Modelo: {os.getenv('LLM_MODEL')} | execuções: {N}\n")
ok_ferr = ok_resp = erros = 0
inicio = time.time()

for i in range(1, N + 1):
    config = {"recursion_limit": 50, "configurable": {"thread_id": str(uuid.uuid4())}}
    chamadas, final, erro = [], "", ""
    try:
        for passo in g.stream({"pergunta": PERGUNTA}, config, stream_mode="updates"):
            for no, upd in passo.items():
                if no == "analyze":
                    msg = upd["messages"][-1]
                    tc = getattr(msg, "tool_calls", None)
                    if tc:
                        chamadas += [(c["name"], c["args"]) for c in tc]
                    else:
                        final = norm(msg.content)
    except Exception as e:
        erro = str(e)[:70]

    etas = {a.get("distancia_nm") for n, a in chamadas if n == "calcular_eta_horas"}
    combs = {a.get("combustivel_t") for n, a in chamadas if n == "reserva_ok"}
    completo = ETA_ESPERADO <= etas and COMB_ESPERADO <= combs
    acertou = "S3-CORAL" in final and any(x in final for x in ("56,6", "56,7", "56.6", "56.7"))
    ok_ferr += completo
    ok_resp += acertou
    erros += bool(erro)
    print(f"{i:>2} | chamadas={len(chamadas):>2} | todas as ferramentas={'sim' if completo else 'NAO'} | S3 56,67={'sim' if acertou else 'NAO'} | erro={erro or '-'}")

print(f"\nResumo: ferramentas completas {ok_ferr}/{N} | resposta com S3-CORAL {ok_resp}/{N} | erros {erros}/{N} | {time.time() - inicio:.0f}s")