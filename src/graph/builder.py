from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from src.graph.nodes.analyze import analyze
from src.graph.nodes.answer_rules import answer_rules
from src.graph.nodes.classify import classify
from src.graph.nodes.format_output import format_output
from src.graph.nodes.human_review import human_review
from src.graph.nodes.prepare import prepare
from src.graph.nodes.receive import receive
from src.graph.nodes.refuse import refuse
from src.graph.nodes.validate import route_validate, validate
from src.graph.routing import route_by_intent
from src.graph.state import State
from src.graph.tools import TOOLS


def build_graph():
    graph = StateGraph(State)
    graph.add_node("receive", receive)
    graph.add_node("classify", classify)
    graph.add_node("prepare", prepare)
    graph.add_node("analyze", analyze)
    graph.add_node("tools", ToolNode(TOOLS))
    graph.add_node("validate", validate)
    graph.add_node("human_review", human_review)
    graph.add_node("format_output", format_output)
    graph.add_node("answer_rules", answer_rules)
    graph.add_node("refuse", refuse)

    graph.add_edge(START, "receive")
    graph.add_edge("receive", "classify")
    graph.add_conditional_edges(
        "classify",
        route_by_intent,
        {
            "primeiro_a_chegar": "prepare",
            "regras": "answer_rules",
            "fora_escopo": "refuse",
        },
    )
    graph.add_edge("prepare", "analyze")
    graph.add_conditional_edges(
        "analyze", tools_condition, {"tools": "tools", END: "validate"}
    )
    graph.add_edge("tools", "analyze")
    graph.add_conditional_edges(
        "validate", route_validate, {"analyze": "analyze", "human_review": "human_review"}
    )
    graph.add_edge("human_review", "format_output")
    graph.add_edge("format_output", END)
    graph.add_edge("answer_rules", END)
    graph.add_edge("refuse", END)
    return graph.compile(checkpointer=MemorySaver())