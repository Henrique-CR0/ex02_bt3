from src.graph.state import State
from src.graph.tools import TOOLS
from src.utils.llm_adapter import get_llm


def analyze(state: State) -> dict:
    llm = get_llm().bind_tools(TOOLS)
    return {"messages": [llm.invoke(state["messages"])]}