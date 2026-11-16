import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_listar_produtos_status_200(client):
    resp = client.get("/api/produtos")
    assert resp.status_code == 200
    dados = resp.get_json()
    assert isinstance(dados, list)
    assert len(dados) >= 4


def test_rejeita_pedido_sem_moagem(client):
    payload = {
        "frete": 9.90,
        "total": 64.80,
        "itens": [{"id": 1, "moagem": "", "qtd": 1, "precoUnitario": 54.90}]
    }
    resp = client.post("/api/pedidos", json=payload)
    assert resp.status_code == 400
    assert "moagem" in resp.get_json()["erro"].lower()


def test_rejeita_pedido_sem_frete(client):
    payload = {
        "frete": 0,
        "total": 54.90,
        "itens": [{"id": 1, "moagem": "ESPRESSO", "qtd": 1, "precoUnitario": 54.90}]
    }
    resp = client.post("/api/pedidos", json=payload)
    assert resp.status_code == 400
    assert "frete" in resp.get_json()["erro"].lower()


def test_cria_pedido_valido_com_sucesso(client):
    payload = {
        "cupom": "CAFE10",
        "desconto": 5.74,
        "frete": 9.90,
        "total": 61.56,
        "itens": [{"id": 1, "moagem": "ESPRESSO", "qtd": 1, "precoUnitario": 57.40}]
    }
    resp = client.post("/api/pedidos", json=payload)
    assert resp.status_code == 201
    dados = resp.get_json()
    assert dados["sucesso"] is True
    assert "id_pedido" in dados
