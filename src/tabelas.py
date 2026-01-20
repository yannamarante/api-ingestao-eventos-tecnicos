from sqlalchemy import Table, Column, BigInteger, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB

from .db import metadata

eventos_tecnicos = Table(
    "eventos_tecnicos",
    metadata,
    Column("id", BigInteger, primary_key=True, autoincrement=True),

    Column("origem", String(50), nullable=False),
    Column("tipo_evento", String(60), nullable=False),
    Column("data_hora", DateTime(timezone=True), nullable=False),

    Column("tipo_ativo", String(40), nullable=True),
    Column("id_ativo", String(80), nullable=False),

    Column("local", String(120), nullable=True),
    Column("id_externo", String(80), nullable=True),

    Column("medicoes", JSONB, nullable=False, default=dict),
    Column("payload_bruto", JSONB, nullable=False, default=dict),
)
