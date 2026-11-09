from langchain_core.prompts import ChatPromptTemplate

PROMPT_UMA_LINHA = ChatPromptTemplate.from_messages(
    [("human", "Qual navio chega primeiro ao porto? Frota: {frota}")]
)
