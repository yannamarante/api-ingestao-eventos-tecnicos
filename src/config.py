import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Configuracoes:
    url_banco: str
    ambiente_flask: str
    porta: int


def obter_configuracoes() -> Configuracoes:
    url_banco = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://postgres:postgres@localhost:5432/engenharia",
    )
    ambiente_flask = os.getenv("FLASK_ENV", "development")
    porta = int(os.getenv("PORT", "8000"))

    return Configuracoes(
        url_banco=url_banco,
        ambiente_flask=ambiente_flask,
        porta=porta,
    )