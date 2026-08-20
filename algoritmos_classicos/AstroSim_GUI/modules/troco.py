
import mysql.connector
from modules.algoritmoGuloso import ordenar_por

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "mysql",
    "database": "astrosim"
}

def carregar_unidades(db_config=DB_CONFIG):
    """Carrega as unidades de recurso do banco (ordenadas por valor desc)."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM UnidadesRecurso ORDER BY valor_unitario DESC")
    unidades = cursor.fetchall()
    conn.close()
    return unidades


def pagar_compra(valor_devido, recursos_disp, db_config=DB_CONFIG):
    """
    Explorador compra um minério pagando com os recursos disponíveis.
    recursos_disp = {id_unidade: quantidade}
    """
    unidades = carregar_unidades(db_config)

    troco_restante = valor_devido
    pagamento = []

    for u in unidades:
        qtd_disp = recursos_disp.get(u["id_unidade"], 0)
        qtd_usada = 0
        while troco_restante >= u["valor_unitario"] and qtd_disp > 0:
            troco_restante -= float(u["valor_unitario"])
            qtd_usada += 1
            qtd_disp -= 1
        if qtd_usada > 0:
            pagamento.append((u["nome_recurso"], qtd_usada, u["valor_unitario"]))

    sucesso = troco_restante <= 0
    return sucesso, pagamento, troco_restante


def receber_venda(valor_venda, recursos_comprador, db_config=DB_CONFIG):
    """
    Explorador vende minério: verifica se o comprador consegue pagar.
    recursos_comprador = {id_unidade: quantidade}
    """
    return pagar_compra(valor_venda, recursos_comprador, db_config)


def registrar_transacao(vendedor, comprador, valor_devido, valor_pago, db_config=DB_CONFIG):
    """Registra a transação no banco."""
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    troco = valor_pago - valor_devido
    cursor.execute("""
        INSERT INTO LogTransacoesB2B (id_mercador_vendedor, id_mercador_comprador,
                                      valor_total_devido, valor_total_pago, valor_troco_calculado)
        VALUES (%s, %s, %s, %s, %s)
    """, (vendedor, comprador, valor_devido, valor_pago, troco))
    conn.commit()
    conn.close()
