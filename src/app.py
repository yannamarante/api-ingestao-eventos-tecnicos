from flask import Flask

from .config import obter_configuracoes
from .db import criar_engine, criar_fabrica_sessoes, metadata
from .routes import construir_rotas

# garante que a tabela seja registrada no metadata
from . import tabelas  # noqa: F401


def criar_app() -> Flask:
    cfg = obter_configuracoes()

    engine = criar_engine(cfg.url_banco)
    metadata.create_all(engine)

    fabrica_sessoes = criar_fabrica_sessoes(engine)

    app = Flask(__name__)
    app.register_blueprint(construir_rotas(fabrica_sessoes, engine))
    return app
