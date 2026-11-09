from langchain_core.tools import tool

LIMITE_TEMPESTADE_KN = 12.0


@tool
def calcular_eta_horas(distancia_nm: float, velocidade_kn: float) -> float:
    """Calcula o ETA em horas: distancia_nm dividida por velocidade_kn."""
    return round(distancia_nm / velocidade_kn, 2)


@tool
def velocidade_efetiva(velocidade_kn: float, em_tempestade: bool) -> float:
    """Velocidade efetiva do navio. Em tempestade o limite é de 12 nós."""
    return min(velocidade_kn, LIMITE_TEMPESTADE_KN) if em_tempestade else velocidade_kn


@tool
def reserva_ok(combustivel_t: float, reserva_t: float) -> bool:
    """True se o combustível a bordo cobre a reserva mínima (navio pode zarpar)."""
    return combustivel_t >= reserva_t


TOOLS = [calcular_eta_horas, velocidade_efetiva, reserva_ok]