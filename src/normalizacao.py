from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from .calculos import calcular_potencia_aparente_kva


def _get(d: Dict[str, Any], *chaves: str) -> Any:
    for k in chaves:
        if k in d and d[k] is not None:
            return d[k]
    return None


def _to_float(v: Any) -> Optional[float]:
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        s = v.strip().replace(",", ".")
        try:
            return float(s)
        except ValueError:
            return None
    return None


def _to_int(v: Any) -> Optional[int]:
    if v is None:
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        return int(v)
    if isinstance(v, str):
        s = v.strip()
        try:
            return int(float(s))
        except ValueError:
            return None
    return None


def _parse_data_hora(v: Any) -> datetime:
    """
    Aceita ISO 8601 com/sem timezone e também 'Z'.
    Retorna datetime (pode vir timezone-aware dependendo da string).
    """
    if not v:
        raise ValueError("campo 'data_hora' é obrigatório")

    if isinstance(v, datetime):
        return v

    if isinstance(v, (int, float)):
        # epoch segundos
        return datetime.fromtimestamp(float(v))

    if isinstance(v, str):
        s = v.strip()
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        try:
            return datetime.fromisoformat(s)
        except ValueError as e:
            raise ValueError(f"data_hora inválida: {v}") from e

    raise ValueError("data_hora inválida")


def normalizar_evento_tecnico(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normaliza chaves PT/EN para um formato único (português).
    Mantém payload original em payload_bruto.
    """
    origem = _get(payload, "origem", "source", "fonte")
    tipo_evento = _get(payload, "tipo_evento", "tipo", "event_type", "tipoEvento")
    data_hora_raw = _get(payload, "data_hora", "dataHora", "timestamp", "ocorrido_em", "occurred_at")

    # Ativo: em engenharia costuma vir como "quadro", "ativo", "panel_id", etc.
    tipo_ativo = _get(payload, "tipo_ativo", "asset_type", "tipoAtivo")
    id_ativo = _get(payload, "id_ativo", "ativo", "asset_id", "idAtivo", "quadro", "panel_id")

    local = _get(payload, "local", "site", "unidade", "endereco", "location")
    id_externo = _get(payload, "id_externo", "idExterno", "external_id", "os", "ordem_servico")

    tensao_v = _to_float(_get(payload, "tensao_v", "tensao", "voltage_v", "voltage"))
    corrente_a = _to_float(_get(payload, "corrente_a", "corrente", "current_a", "current"))
    potencia_kw = _to_float(_get(payload, "potencia_kw", "potencia", "power_kw", "power"))
    fp = _to_float(_get(payload, "fp", "fator_potencia", "power_factor"))
    fases = _to_int(_get(payload, "fases", "qtd_fases", "phases"))

    temperatura_c = _to_float(_get(payload, "temperatura", "temp_c", "temperatura_c"))

    data_hora = _parse_data_hora(data_hora_raw)

    # medições normalizadas
    medicoes: Dict[str, Any] = {
        "tensao_v": tensao_v,
        "corrente_a": corrente_a,
        "potencia_kw": potencia_kw,
        "fp": fp,
        "fases": fases,
        "temperatura_c": temperatura_c,
    }

    kva = calcular_potencia_aparente_kva(tensao_v, corrente_a, fases)
    if kva is not None:
        medicoes["potencia_aparente_kva"] = kva

    # limpeza: remove None
    medicoes = {k: v for k, v in medicoes.items() if v is not None}

    normalizado = {
        "origem": (str(origem).strip().lower() if origem else None),
        "tipo_evento": (str(tipo_evento).strip().upper() if tipo_evento else None),
        "data_hora": data_hora,
        "tipo_ativo": (str(tipo_ativo).strip().upper() if tipo_ativo else None),
        "id_ativo": (str(id_ativo).strip().upper() if id_ativo else None),
        "local": (str(local).strip() if local else None),
        "id_externo": (str(id_externo).strip() if id_externo else None),
        "medicoes": medicoes,
        "payload_bruto": payload,
    }
    return normalizado
