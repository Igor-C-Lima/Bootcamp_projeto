import os
from pathlib import Path

import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

from src.estoque.funcoes import alerta_estoque_baixo

# IMPORTAÇÕES NOVAS DO SUPABASE (Issue 1)
from src.storage.estoque_armazenamento import (
    listar_itens,
    adicionar_item,
    atualizar_quantidade,
    remover_item
)

ROOT_DIR = Path(__file__).resolve().parents[2]

app = Flask(__name__, static_folder=str(ROOT_DIR))
CORS(app)

@app.get("/")
def index():
    """Serve o HTML principal."""
    return send_from_directory(str(ROOT_DIR), "estoque.html")

@app.get("/api/estoque")
def get_estoque():
    """Retorna todo o estoque atual vindo do Supabase."""
    return jsonify(listar_itens())

@app.post("/api/estoque")
def post_cadastrar():
    """Cadastra um novo produto na nuvem."""
    dados = request.get_json()
    nome = dados["nome"].upper()
    
    # Verifica se já existe usando os dados da nuvem
    estoque_atual = listar_itens()
    if nome in estoque_atual:
         return jsonify({"ok": False, "mensagem": "Produto já cadastrado."}), 400

    try:
        adicionar_item(nome, int(dados["quantidade"]), int(dados["limite_minimo"]))
        return jsonify({"ok": True, "mensagem": "Produto cadastrado com sucesso."}), 201
    except Exception as e:
        return jsonify({"ok": False, "mensagem": str(e)}), 400

@app.patch("/api/estoque/<nome>")
def patch_atualizar(nome):
    """Atualiza quantidade na nuvem."""
    dados = request.get_json()
    nome = nome.upper()
    estoque_atual = listar_itens()
    
    if nome not in estoque_atual:
         return jsonify({"ok": False, "mensagem": "Produto não encontrado."}), 404

    valor = int(dados["valor"])
    operacao = dados["operacao"].upper()
    qtd_atual = estoque_atual[nome]["quantidade"]
    limite = estoque_atual[nome]["limite_minimo"]

    # Lógica de somar ou subtrair
    if operacao == "AUMENTAR":
        nova_qtd = qtd_atual + valor
    elif operacao == "DIMINUIR":
        nova_qtd = qtd_atual - valor
        if nova_qtd < 0:
            return jsonify(
                {"ok": False, "mensagem": 
                    "Quantidade final não pode ser negativa."}
                ), 400
    else:
        return jsonify({"ok": False, "mensagem": "Operação inválida."}), 400

    try:
        atualizar_quantidade(nome, nova_qtd, limite)
        return jsonify({"ok": True, "mensagem": "Quantidade atualizada."})
    except Exception as e:
        return jsonify({"ok": False, "mensagem": str(e)}), 400

@app.delete("/api/estoque/<nome>")
def delete_produto(nome):
    """Remove um produto da nuvem."""
    nome = nome.upper()
    try:
        remover_item(nome)
        return jsonify({"ok": True, "mensagem": "Produto removido."})
    except Exception as e:
        return jsonify({"ok": False, "mensagem": str(e)}), 404

@app.get("/api/estoque/alertas")
def get_alertas():
    """Verifica alertas usando a função legado e os dados da nuvem."""
    return jsonify(alerta_estoque_baixo(listar_itens()))

# ── Clima (proxy OpenWeather) ──────────────────────────────────────────────────
@app.get("/api/clima")
def get_clima():
    cidade = request.args.get("cidade", "").strip()
    if not cidade:
        return jsonify({"erro": "Parâmetro 'cidade' é obrigatório."}), 400

    api_key = os.environ.get("OPENWEATHER_KEY")
    if not api_key:
        return jsonify({"erro": "OPENWEATHER_KEY não configurada no servidor."}), 500

    try:
        resp = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": cidade,
                "appid": api_key,
                "units": "metric",
                "lang": "pt_br",
            },
            timeout=8,
        )
        return jsonify(resp.json()), resp.status_code
    except requests.exceptions.Timeout:
        return jsonify({"erro": "OpenWeather não respondeu a tempo."}), 504
    except requests.exceptions.RequestException as e:
        return jsonify({"erro": str(e)}), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)