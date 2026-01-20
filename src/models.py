from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class EventoTecnico(Base):
    __tablename__ = "eventos_tecnicos"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)

    origem: Mapped[str] = mapped_column(String(50), nullable=False)
    tipo_evento: Mapped[str] = mapped_column(String(60), nullable=False)
    data_hora: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    tipo_ativo: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    id_ativo: Mapped[str] = mapped_column(String(80), nullable=False)

    local: Mapped[Optional[str]] = mapped_column(String(120), nullable=True)
    id_externo: Mapped[Optional[str]] = mapped_column(String(80), nullable=True)

    # Evita tipos genéricos em Mapped[...] por compatibilidade com Python 3.14 + SQLAlchemy
    medicoes: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    payload_bruto: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
