from .app import criar_app
from .config import obter_configuracoes

app = criar_app()

if __name__ == "__main__":
    cfg = obter_configuracoes()
    app.run(
        host="0.0.0.0",
        port=cfg.porta,
        debug=(cfg.ambiente_flask == "development"),
    )