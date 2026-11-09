import json
from pathlib import Path

from src.graph.state import State

ARQUIVO = Path(__file__).resolve().parents[3] / "dados" / "frota_tempestade.json"


def receive(state: State) -> dict:
    return {"frota": json.loads(ARQUIVO.read_text(encoding="utf-8"))}