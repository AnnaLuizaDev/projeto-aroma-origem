from flask import Flask, render_template, request, jsonify
from models import ProdutoModel, PedidoModel

app = Flask(__name__)


# Rota Principal (View)
@app.route("/")
def index():
    return render_template("index.html")


# Controller REST: Listar Cafes
@app.route("/api/produtos", methods=["GET"])
def api_listar_produtos():
    produtos = ProdutoModel.listar_todos()
    return jsonify(produtos), 200


# Controller REST: Registrar Pedido
@app.route("/api/pedidos", methods=["POST"])
def api_criar_pedido():
    dados = request.get_json(silent=True) or {}
    try:
        resultado = PedidoModel.criar_pedido(dados)
        return jsonify({
            "sucesso": True,
            "mensagem": "Pedido registrado com sucesso!",
            **resultado
        }), 201
    except ValueError as err:
        return jsonify({"sucesso": False, "erro": str(err)}), 400
    except Exception as err:
        return jsonify({"sucesso": False, "erro": f"Erro interno: {err}"}), 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
