import sqlite3
import numpy as np
from datetime import datetime, date, timedelta
import streamlit as st
import pandas as pd
def init_db(conn):

    """
    Inicializa o banco de dados.
    1. Cria a tabela 'tb_vendas' se ela não existir.
    2. Verifica se a tabela está vazia.
    3. Se estiver vazia, popula com 180 dias de dados fictícios.
    """

    # Cria um objeto 'cursor' para executar comandos SQL na conexão fornecida
    cursor = conn.cursor()
    
    # Define o comando SQL para criar a tabela
    # 'IF NOT EXISTS' é uma cláusula de segurança que impede erro se a tabela já existir
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

    # Confirma (commita) a transação de criação da tabela
    conn.commit()

    # Verifica quantos registros (linhas) existem na tabela
    cursor.execute("SELECT COUNT(*) FROM tb_vendas")

    # .fetchone()[0] captura o primeiro valor da primeira linha do resultado (a contagem)
    # Este 'if' garante que o código de popular dados SÓ rode se a tabela estiver vazia
    if cursor.fetchone()[0] == 0:

        # --- Geração de Dados Fictícios ---
        
        # Define a "semente" (seed) para o gerador de números aleatórios
        # Isso garante que os mesmos dados "aleatórios" sejam gerados toda vez
        # que o script for executado, tornando os resultados reprodutíveis.
        np.random.seed(42)
        
        # Define uma data de início fixa (1º de Jan de 2026) para os dados
        start_date = date(2026, 1, 1)
        
        # Cria uma lista de 180 objetos 'date' consecutivos
        datas = [start_date + timedelta(days = i) for i in range(180)]
        
        # Define as listas de dimensões para os dados
        regioes = ["Norte", "Nordeste", "Sul", "Sudeste", "Centro-Oeste"]
        categorias = ["Eletrônicos", "Roupas", "Alimentos", "Serviços"]
        
        # Dicionário aninhado para mapear produtos e seus preços base por categoria
        # Isso é crucial para criar a correlação positiva entre quantidade e faturamento
        dict_produtos = {
            "Eletrônicos": {"Smartphone": 1200, "Laptop": 3500, "Tablet": 800},
            "Roupas": {"Camiseta": 50, "Terno": 150, "Casaco": 300},
            "Alimentos": {"Congelados": 40, "Bebidas": 15, "Limpeza": 25},
            "Serviços": {"Consultoria": 1000, "Instalação": 400, "Suporte": 200}
        }

        # Lista vazia para armazenar todas as linhas (tuplas) de dados
        rows = []

        # Loop para cada dia na lista de datas
        for d in datas:

            # Simula um número aleatório de vendas (entre 5 e 14) para aquele dia
            vendas_diarias = np.random.randint(5, 15)

            # Loop para cada venda individual dentro do dia
            # Usamos '_' como variável pois não precisamos do número do índice
            for _ in range(vendas_diarias):

                # Escolhe aleatoriamente os atributos da venda
                r = np.random.choice(regioes)
                c = np.random.choice(categorias)
                
                # Escolhe um produto aleatório *baseado* na categoria escolhida
                p = np.random.choice(list(dict_produtos[c].keys()))
                
                # Obtém o preço base do produto escolhido
                preco_base = dict_produtos[c][p]
                
                # Gera uma quantidade aleatória (entre 1 e 24)
                quantidade = np.random.randint(1, 25) 
                
                # Calcula o faturamento base (preço * quantidade)
                base_faturamento = preco_base * quantidade
                
                # Adiciona "ruído" (noise) de +/- 20% para tornar os dados mais realistas
                # Isso simula descontos, impostos ou pequenas variações de preço
                noise = np.random.uniform(-0.20, 0.20)
                faturamento = base_faturamento * (1 + noise)
                
                # Garante que o faturamento nunca seja negativo
                faturamento = max(0, faturamento)

                # Adiciona a linha de venda (como uma tupla) à lista 'rows'
                # O formato da tupla deve corresponder exatamente à ordem das colunas no INSERT
                rows.append((d.isoformat(), r, c, p, round(faturamento, 2), quantidade))

        # --- Inserção em Massa (Bulk Insert) ---
        # 'executemany' é MUITO mais eficiente do que fazer um 'execute' para cada linha
        # Insere todas as tuplas da lista 'rows' no banco de dados de uma só vez
        cursor.executemany(
            "INSERT INTO tb_vendas (date, regiao, categoria, produto, faturamento, quantidade) VALUES (?, ?, ?, ?, ?, ?)",
            rows,
        )

        # Confirma (commita) a transação de inserção de dados
        conn.commit()

def cria_conexao(db_path = "database.db"):

    """
    Cria e retorna um objeto de conexão com o banco de dados SQLite.
    
    Parâmetros:
    db_path (str): O caminho e nome do arquivo .db a ser usado. 
                   O padrão é "database.db".
                   Se o arquivo não existir, o SQLite o criará.
    """

    # Cria a conexão com o banco de dados SQLite
    # check_same_thread=False: Esta é uma configuração importante para o Streamlit.
    # O Streamlit executa o código em diferentes threads (processos). 
    # Por padrão, o SQLite só permite que a thread que o criou interaja com ele.
    # Definir como 'False' permite que múltiplas threads (como as do Streamlit) 
    # acessem a mesma conexão.
    conn = sqlite3.connect(db_path, check_same_thread = False)
    
    # Retorna o objeto de conexão para ser usado por outras funções
    return conn
 
def carrega_dados():

    """
    Função principal para carregar os dados.
    1. Conecta ao banco.
    2. Garante que o banco esteja inicializado (chama Bloco 2).
    3. Carrega a tabela 'tb_vendas' em um DataFrame do Pandas.
    4. Fecha a conexão.
    5. Retorna o DataFrame.
    """
    
    # Chama a função do Bloco 3 para obter uma conexão com o DB
    conn = cria_conexao()
    
    # Chama a função do Bloco 2 para garantir que o DB e a tabela existam
    # Se a tabela estiver vazia, esta função também irá populá-la.
    init_db(conn) 
    
    # Executa uma consulta SQL para selecionar TUDO (*) da 'tb_vendas'
    # pd.read_sql_query: Função do Pandas que lê o resultado de um SQL direto para um DataFrame.
    # parse_dates=["date"]: Instrui o Pandas a converter a coluna 'date' (que é TEXTO no SQLite)
    # em um tipo de dado datetime, que é essencial para gráficos e filtros de tempo.
    df = pd.read_sql_query("SELECT * FROM tb_vendas", conn, parse_dates = ["date"])
    
    # Boa prática: Fecha a conexão com o banco de dados após a consulta
    conn.close()
    
    # Retorna o DataFrame carregado para ser usado pelo restante do app
    return df