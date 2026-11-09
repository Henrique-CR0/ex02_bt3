from langchain_core.prompts import ChatPromptTemplate

ANALYZE_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é um despachante de porto. Para CADA navio faça, nesta ordem:\n"
            "1) use reserva_ok; se for False, o navio está bloqueado e não concorre;\n"
            "2) use velocidade_efetiva com o campo em_tempestade;\n"
            "3) use calcular_eta_horas com a velocidade efetiva.\n"
            "Nunca calcule de cabeça: use sempre as ferramentas. "
            "No fim, diga qual navio chega primeiro e liste o ETA de cada navio elegível "
            "e os navios bloqueados com o motivo.",
        ),
        ("human", "Frota:\n{frota}\n\nPergunta: {pergunta}"),
    ]
)