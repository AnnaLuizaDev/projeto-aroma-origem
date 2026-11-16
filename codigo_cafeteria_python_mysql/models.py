import mysql.connector
from mysql.connector import Error
from datetime import date

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "cafeteria_gourmet",
    "charset": "utf8mb4"
}

# Catálogo de contingência caso o MySQL local ainda não tenha sido iniciado
CATALOGO_FALLBACK = [
    {
        "id_produto": 1,
        "nome": "Blend Reserva Serra da Mantiqueira",
        "origem": "Sul de Minas Gerais • Altitude 1.250m",
        "notas_sensoriais": "Chocolate amargo, caramelo tostado e avelã",
        "intensidade": 8,
        "data_torra": str(date.today()),
        "preco_base": 54.90,
        "estoque_kg": 45.0
    },
    {
        "id_produto": 2,
        "nome": "Microlote Bourbon Amarelo",
        "origem": "Alta Mogiana - SP • Altitude 1.150m",
        "notas_sensoriais": "Frutas amarelas, mel silvestre e acidez cítrica",
        "intensidade": 6,
        "data_torra": str(date.today()),
        "preco_base": 68.50,
        "estoque_kg": 20.0
    },
    {
        "id_produto": 3,
        "nome": "Geisha Edição Limitada",
        "origem": "Serra do Caparaó - ES/MG • Altitude 1.400m",
        "notas_sensoriais": "Jasmim, flor de laranjeira, pêssego e mel",
        "intensidade": 5,
        "data_torra": str(date.today()),
        "preco_base": 92.00,
        "estoque_kg": 10.0
    },
    {
        "id_produto": 4,
        "nome": "Intenso Espresso Barista",
        "origem": "Cerrado Mineiro - MG • Altitude 1.100m",
        "notas_sensoriais": "Cacau 70%, nozes e crema densa persistente",
        "intensidade": 9,
        "data_torra": str(date.today()),
        "preco_base": 49.90,
        "estoque_kg": 60.0
    }
]


def get_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        if conn.is_connected():
            return conn
    except Error:
        return None
    return None


class ProdutoModel:
    @staticmethod
    def listar_todos():
        conn = get_connection()
        if not conn:
            return CATALOGO_FALLBACK
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM produtos_cafe WHERE ativo = 1")
            rows = cursor.fetchall()
            for r in rows:
                r["preco_base"] = float(r["preco_base"])
                r["estoque_kg"] = float(r["estoque_kg"])
                r["data_torra"] = str(r["data_torra"])
            return rows if rows else CATALOGO_FALLBACK
        finally:
            conn.close()


class PedidoModel:
    MOAGENS_VALIDAS = {
        "GRAOS_INTEIROS",
        "ESPRESSO",
        "FILTRO_V60",
        "PRENSA_FRANCESA",
        "MOKA"
    }

    @staticmethod
    def criar_pedido(dados: dict):
        itens = dados.get("itens", [])
        if not itens:
            raise ValueError("O pedido deve conter ao menos um item.")

        frete = float(dados.get("frete", 0))
        if frete <= 0:
            raise ValueError("O frete deve ser calculado antes de finalizar o pedido.")

        for item in itens:
            if item.get("moagem") not in PedidoModel.MOAGENS_VALIDAS:
                raise ValueError(f"Tipo de moagem inválido ou não informado: {item.get('moagem')}")
            if int(item.get("qtd", 0)) <= 0:
                raise ValueError("Quantidade inválida para o item.")

        conn = get_connection()
        if not conn:
            # Simulação transacional quando rodando sem servidor MySQL local
            import random
            return {"id_pedido": random.randint(100000, 999999), "modo": "simulacao_offline"}

        try:
            cursor = conn.cursor()
            sql_pedido = """
                INSERT INTO pedidos (id_cliente, id_endereco, cupom_aplicado, valor_desconto, valor_frete, valor_total)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql_pedido, (
                dados.get("id_cliente", 1),
                dados.get("id_endereco", 1),
                dados.get("cupom"),
                float(dados.get("desconto", 0)),
                frete,
                float(dados.get("total", 0))
            ))
            id_pedido = cursor.lastrowid

            sql_item = """
                INSERT INTO itens_pedido (id_pedido, id_produto, tipo_moagem, quantidade, preco_unitario)
                VALUES (%s, %s, %s, %s, %s)
            """
            for item in itens:
                cursor.execute(sql_item, (
                    id_pedido,
                    int(item["id"]),
                    item["moagem"],
                    int(item["qtd"]),
                    float(item["precoUnitario"])
                ))

            conn.commit()
            return {"id_pedido": id_pedido, "modo": "mysql_persistido"}
        except Exception as exc:
            conn.rollback()
            raise exc
        finally:
            conn.close()
