import math
from typing import Optional


def calcular_potencia_aparente_kva(
    tensao_v: Optional[float],
    corrente_a: Optional[float],
    fases: Optional[int],
) -> Optional[float]:
    """
    Retorna kVA aproximado quando houver dados suficientes.
    - Monofásico: kVA = V * I / 1000
    - Trifásico: kVA = √3 * V * I / 1000
    """
    if tensao_v is None or corrente_a is None:
        return None

    if fases is None or fases == 1:
        return round((tensao_v * corrente_a) / 1000.0, 4)

    if fases == 3:
        return round((math.sqrt(3) * tensao_v * corrente_a) / 1000.0, 4)

    return None
