from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, Field, validator


class RequisicaoIngestao(BaseModel):
    origem: str = Field(..., min_length=1, max_length=50)
    tipo_evento: str = Field(..., min_length=1, max_length=60)
    data_hora: datetime

    tipo_ativo: Optional[str] = Field(None, max_length=40)
    id_ativo: str = Field(..., min_length=1, max_length=80)

    local: Optional[str] = Field(None, max_length=120)
    id_externo: Optional[str] = Field(None, max_length=80)

    medicoes: Dict[str, Any] = Field(default_factory=dict)
    payload_bruto: Dict[str, Any] = Field(default_factory=dict)

    @validator("origem")
    def _origem_lower(cls, v: str) -> str:
        return v.strip().lower()

    @validator("tipo_evento")
    def _tipo_upper(cls, v: str) -> str:
        return v.strip().upper()

    @validator("id_ativo")
    def _id_upper(cls, v: str) -> str:
        return v.strip().upper()


class RespostaIngestao(BaseModel):
    id_evento: int
