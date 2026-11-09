import uuid

from langgraph.types import Command

from src.graph.builder import build_graph

PERGUNTA_PADRAO = "Qual navio chega primeiro ao porto?"
LIMITE = 3  # perguntas por sessão; 0 = sem limite


def main() -> None:
    graph = build_graph()
    feitas = 0
    print(f"Digite uma pergunta (Enter = padrão, 'sair' para encerrar). Limite: {LIMITE or 'sem limite'}.")
    while not LIMITE or feitas < LIMITE:
        pergunta = input(f"\nPergunta {feitas + 1}/{LIMITE}: ").strip()
        if pergunta.lower() in {"sair", "exit", "q"}:
            break
        pergunta = pergunta or PERGUNTA_PADRAO
        config = {"recursion_limit": 50, "configurable": {"thread_id": str(uuid.uuid4())}}
        try:
            saida = graph.invoke({"pergunta": pergunta}, config)
            if "__interrupt__" in saida:  # o grafo pausou em human_review
                pedido = saida["__interrupt__"][0].value
                print("Recomendação do agente:\n", pedido["recomendacao"])
                aprovado = input("Aprovar? (s/n): ").strip().lower() == "s"
                nota = input("Nota (opcional): ").strip()
                saida = graph.invoke(Command(resume={"aprovado": aprovado, "nota": nota}), config)
            print(saida["resultado"])
        except Exception as e:
            print(f"Erro nesta pergunta: {e}")
        feitas += 1
    print("\nEncerrado.")


if __name__ == "__main__":
    main()