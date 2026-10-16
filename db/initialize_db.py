import sqlite3
import numpy as np
from datetime import datetime, date, timedelta
import streamlit as st
import pandas as pd
def init_db(conn):

    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tb_vendas (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            date TEXT,
            regiao TEXT,
            categoria TEXT,
            produto TEXT,
            faturamento REAL,
            quantidade INTEGER
        )
    """)

    conn.commit()
    cursor.execute("SELECT COUNT(*) FROM tb_vendas")

    if cursor.fetchone()[0] == 0:
        np.random.seed(42)
        start_date = date(2026, 1, 1)
        datas = [start_date + timedelta(days = i) for i in range(180)]
        regioes = ["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"]
        categorias = ["Eletrônicos", "Roupas", "Alimentos", "Serviços"]
        dict_produtos = {
            "Eletrônicos": {"Smartphone": 1200, "Laptop": 3500, "Tablet": 800},
            "Roupas": {"Camiseta": 50, "Terno": 150, "Casaco": 300},
            "Alimentos": {"Congelados": 40, "Bebidas": 15, "Limpeza": 25},
            "Serviços": {"Consultoria": 1000, "Instalação": 400, "Suporte": 200}
        }
        rows = []
        for d in datas:
            vendas_diarias = np.random.randint(5, 15)
            for _ in range(vendas_diarias):
                r = np.random.choice(regioes)
                c = np.random.choice(categorias)
                p = np.random.choice(list(dict_produtos[c].keys()))
                preco_base = dict_produtos[c][p]
                quantidade = np.random.randint(1, 25) 
                base_faturamento = preco_base * quantidade
                noise = np.random.uniform(-0.20, 0.20)
                faturamento = base_faturamento * (1 + noise)
                faturamento = max(0, faturamento)
                rows.append((d.isoformat(), r, c, p, round(faturamento, 2), quantidade))

        cursor.executemany(
            "INSERT INTO tb_vendas (date, regiao, categoria, produto, faturamento, quantidade) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )

        conn.commit()

def cria_conexao(db_path = "database.db"):

    """
    Cria e retorna um objeto de conexão com o banco de dados SQLite.
    
    Parâmetros:
    db_path (str): O caminho e nome do arquivo .db a ser usado. 
                   O padrão é "database.db".
                   Se o arquivo não existir, o SQLite o criará.
    """

    conn = sqlite3.connect(db_path, check_same_thread = False)
    return conn
 
def carrega_dados():
    conn = cria_conexao()
    init_db(conn)
    df = pd.read_sql_query("SELECT * FROM tb_vendas", conn, parse_dates = ["date"])
    conn.close()
    return df