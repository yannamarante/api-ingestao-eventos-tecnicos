from __future__ import annotations

from datetime import datetime
from typing import Optional

from flask import Blueprint, jsonify, request
from sqlalchemy import select, insert
from sqlalchemy.orm import Session

from .normalizacao import normalizar_evento_tecnico
from .schemas import RequisicaoIngestao, RespostaIngestao
from .tabelas import eventos_tecnicos


def _parse_data_query(valor: Optional[str]) -> Optional[datetime]:
    if not valor:
        return None
    s = valor.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(s)
    except Exception as e:
        raise ValueError(f"formato inválido para data: {valor}") from e


def construir_rotas(fabrica_sessoes, engine):
    bp = Blueprint("api", __name__)

    @bp.get("/saude")
    def saude():
        return jsonify({"status": "ok"}), 200

    @bp.post("/ingestao")
    def ingestao():
        sessao: Session = fabrica_sessoes()
        try:
            bruto = request.get_json(silent=True)
            if bruto is None:
                return jsonify({"erro": "json_invalido", "mensagem": "Corpo deve ser JSON"}), 400

            normalizado = normalizar_evento_tecnico(bruto)

            try:
                validado = RequisicaoIngestao(**normalizado)
            except Exception as e:
                return jsonify({"erro": "validacao", "mensagem": str(e)}), 422

            payload_insert = {
                "origem": validado.origem,
                "tipo_evento": validado.tipo_evento,
                "data_hora": validado.data_hora,
                "tipo_ativo": validado.tipo_ativo,
                "id_ativo": validado.id_ativo,
                "local": validado.local,
                "id_externo": validado.id_externo,
                "medicoes": validado.medicoes,
                "payload_bruto": validado.payload_bruto,
            }

            # Postgres: RETURNING id
            stmt = insert(eventos_tecnicos).values(**payload_insert).returning(eventos_tecnicos.c.id)
            novo_id = sessao.execute(stmt).scalar_one()
            sessao.commit()

            resp = RespostaIngestao(id_evento=int(novo_id))
            return jsonify(resp.dict()), 201

        except Exception:
            sessao.rollback()
            return jsonify({"erro": "interno", "mensagem": "Erro inesperado"}), 500
        finally:
            sessao.close()

    @bp.get("/eventos")
    def listar_eventos():
        sessao: Session = fabrica_sessoes()
        try:
            tipo_evento = request.args.get("tipo_evento")
            id_ativo = request.args.get("id_ativo")
            data_ini = _parse_data_query(request.args.get("data_ini"))
            data_fim = _parse_data_query(request.args.get("data_fim"))

            limite_raw = request.args.get("limite", "50")
            try:
                limite = int(limite_raw)
            except ValueError:
                return jsonify({"erro": "validacao", "mensagem": "limite deve ser inteiro"}), 422

            limite = max(1, min(limite, 200))

            stmt = select(eventos_tecnicos)

            if tipo_evento:
                stmt = stmt.where(eventos_tecnicos.c.tipo_evento == tipo_evento.strip().upper())
            if id_ativo:
                stmt = stmt.where(eventos_tecnicos.c.id_ativo == id_ativo.strip().upper())
            if data_ini:
                stmt = stmt.where(eventos_tecnicos.c.data_hora >= data_ini)
            if data_fim:
                stmt = stmt.where(eventos_tecnicos.c.data_hora <= data_fim)

            stmt = stmt.order_by(eventos_tecnicos.c.data_hora.desc()).limit(limite)

            rows = sessao.execute(stmt).mappings().all()

            saida = []
            for r in rows:
                saida.append(
                    {
                        "id": int(r["id"]),
                        "origem": r["origem"],
                        "tipo_evento": r["tipo_evento"],
                        "data_hora": r["data_hora"].isoformat() if r["data_hora"] else None,
                        "tipo_ativo": r["tipo_ativo"],
                        "id_ativo": r["id_ativo"],
                        "local": r["local"],
                        "id_externo": r["id_externo"],
                        "medicoes": r["medicoes"],
                    }
                )

            return jsonify({"total": len(saida), "eventos": saida}), 200

        except ValueError as e:
            return jsonify({"erro": "validacao", "mensagem": str(e)}), 422
        except Exception:
            return jsonify({"erro": "interno", "mensagem": "Erro inesperado"}), 500
        finally:
            sessao.close()

    return bp

