import pytest
from unittest.mock import patch
from src.api.servidor import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c

@patch("src.api.servidor.listar_itens")
def test_get_estoque(mock_listar, client):
    # Simula o retorno do banco via função
    mock_listar.return_value = (
        {"AÇAI": {"quantidade": 10, "limite_minimo": 5, "status": "Ok"}}
        )
    
    r = client.get("/api/estoque")
    
    assert r.status_code == 200
    dados = r.get_json()
    assert "AÇAI" in dados
    assert dados["AÇAI"]["quantidade"] == 10

@patch("src.api.servidor.listar_itens")
@patch("src.api.servidor.adicionar_item")
def test_post_cadastrar_novo_produto(mock_adicionar, mock_listar, client):
    # Simula que o banco está vazio inicialmente
    mock_listar.return_value = {}
    
    r = client.post("/api/estoque", json={
        "nome": "NUTELLA",
        "quantidade": 5,
        "limite_minimo": 2
    })
    
    assert r.status_code == 201
    assert r.get_json()["ok"] is True
    mock_adicionar.assert_called_once_with("NUTELLA", 5, 2)

@patch("src.api.servidor.listar_itens")
def test_post_cadastrar_produto_existente(mock_listar, client):
    # Simula que NUTELLA já existe no banco
    mock_listar.return_value = {"NUTELLA": {"quantidade": 5, "limite_minimo": 2}}
    
    r = client.post("/api/estoque", json={
        "nome": "NUTELLA",
        "quantidade": 10,
        "limite_minimo": 5
    })
    
    assert r.status_code == 400
    assert "já cadastrado" in r.get_json()["mensagem"].lower()