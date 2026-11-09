from langchain_core.prompts import ChatPromptTemplate

CLASSIFY_PROMPT = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Classifique a pergunta de um operador de porto em uma intenção:\n"
            "- primeiro_a_chegar: qual navio chega primeiro ao porto\n"
            "- regras: dúvida sobre as regras de navegação (velocidade, tempestade, combustível)\n"
            "- fora_escopo: qualquer outro assunto",
        ),
        ("human", "{pergunta}"),
    ]
)