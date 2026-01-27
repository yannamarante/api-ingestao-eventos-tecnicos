# API de Ingestão de Eventos Técnicos

API desenvolvida em **Python com FastAPI** para ingestão, validação e organização de eventos técnicos (logs, falhas, medições e status).

Projeto criado com foco em **boas práticas**, **arquitetura limpa** e **escalabilidade**, servindo como base para integrações com sensores, bancos de dados, dashboards e sistemas externos.

---

## Objetivo

- Receber eventos técnicos via HTTP
- Validar dados de entrada
- Padronizar registros
- Facilitar análise e integração futura
- Servir como projeto de estudo e portfólio

---

## Tecnologias

- Python 3.10+
- FastAPI
- Uvicorn
- Pydantic
- Pytest

---

## Estrutura do Projeto

```text
api-ingestao-eventos-tecnicos/
├── src/
│   ├── main.py
│   ├── api.py
│   ├── schemas.py
│   ├── models.py
│   └── database.py
├── tests/
│   └── test_eventos.py
├── requirements.txt
├── .env
└── README.md

```
---
## ▶️ Executando o Projeto

### 1️⃣ Criar o ambiente virtual
```bash
python -m venv .venv
```
### 2️⃣ Ativar o ambiente virtual
#### No Windows
```
.venv\Scripts\activate
```
#### Linux/macOS
```
source .venv/bin/activate
```
### 3️⃣ Instalar dependências
```
pip install -r requirements.txt
```
### 4️⃣ Executar a aplicação
```
uvicorn src.main:app --reload
```

## Documentação da API
Após iniciar o servidor, acesse:

- http://127.0.0.1:8000/docs

- http://127.0.0.1:8000/redoc

## Evoluções Futuras

- Persistência em banco (PostgreSQL)

- Autenticação

- Filas de eventos
 
- Dashboards e métricas

- Alertas automáticos
- 
---
## Autor
Yann Amarante
Engenheiro Eletricista pós-graduando em Engenharia de Software
