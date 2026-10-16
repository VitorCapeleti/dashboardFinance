# 📊 Dashboard Financeiro

Aplicação web em Python para analisar dados de vendas. Ela lê os registros de um banco SQLite, exibe indicadores e gráficos interativos que respondem a filtros, e exporta os dados filtrados em CSV ou em um relatório PDF.

Feita com **Streamlit**, **Pandas**, **Plotly** e **FPDF2**.

---

## Funcionalidades

### Filtros (barra lateral)

Todos os indicadores, gráficos e exportações usam apenas os dados que passam pelos filtros:

- **Período de análise:** intervalo de datas.
- **Regiões:** Norte, Nordeste, Sul, Sudeste e Centro-Oeste.
- **Categorias:** Eletrônicos, Roupas, Alimentos e Serviços.
- **Produtos:** os 12 produtos cadastrados.

Se nenhum registro atender aos filtros, a app mostra um aviso no lugar do dashboard.

### Indicadores (KPIs)

Quatro cards no topo da página:

| Card | Cálculo |
|---|---|
| Receita Total | Soma do faturamento |
| Vendas (Qtd) | Soma das unidades vendidas |
| Ticket Médio | Receita total ÷ quantidade total |
| Transações | Número de registros de venda |

### Aba "Visão Gráfica"

- **Evolução da Receita Diária:** gráfico de área com o faturamento somado por dia.
- **Mix de Categorias:** gráfico de rosca com a participação de cada categoria na receita.
- **Performance Regional:** barras com a receita total por região.
- **Análise Dia da Semana:** receita média por dia da semana, de segunda a domingo.
- **Dispersão Quantidade x Faturamento:** cada venda é um ponto, colorido pela categoria. O tamanho do ponto acompanha o faturamento.

Os gráficos são interativos: dá para passar o mouse, dar zoom e ocultar séries pela legenda.

### Aba "Dados Detalhados & Exportação"

- **Tabela** com todos os registros filtrados.
- **Baixar CSV:** exporta os dados filtrados em `dados_filtrados.csv`.
- **Gerar Relatório PDF:** cria o `Relatorio_Vendas_<data>.pdf` com:
  - data e hora de geração;
  - os KPIs de receita, quantidade e ticket médio;
  - uma tabela com as 15 maiores vendas por receita.

---

## Dados

Os dados ficam no arquivo `database.db` (SQLite), na tabela `tb_vendas`:

| Coluna | Tipo | Descrição |
|---|---|---|
| `id` | INTEGER | Chave primária autoincremental |
| `date` | TEXT | Data da venda (`AAAA-MM-DD`) |
| `regiao` | TEXT | Região da venda |
| `categoria` | TEXT | Categoria do produto |
| `produto` | TEXT | Nome do produto |
| `faturamento` | REAL | Valor da venda em R$ |
| `quantidade` | INTEGER | Unidades vendidas |

**Dados fictícios na primeira execução.** Se o banco não existir ou a tabela estiver vazia, a app cria a tabela e a preenche com 180 dias de vendas simuladas, a partir de 01/01/2026. São de 5 a 14 vendas por dia. O valor de cada venda é o preço base do produto × a quantidade, com uma variação aleatória de ±20%. A semente aleatória é fixa, então os dados gerados são sempre os mesmos.

**Usar seus próprios dados.** Insira seus registros na tabela `tb_vendas` seguindo o esquema acima. Enquanto a tabela tiver ao menos um registro, os dados fictícios não são gerados.

**Cache.** A leitura do banco fica em cache por 10 minutos (`@st.cache_data(ttl=600)`). Depois de alterar o banco, espere esse tempo ou limpe o cache pelo menu da app (☰ → *Clear cache*).

---

## Estrutura do projeto

```
.
├── app.py                  # Ponto de entrada: layout, gráficos e exportações
├── db/
│   └── initialize_db.py    # Conexão SQLite, criação da tabela e geração dos dados fictícios
├── templates/
│   ├── sidebar.py          # Filtros da barra lateral
│   └── cards_kpis.py       # Cálculo e exibição dos KPIs
├── funcs/
│   └── generate_pdf.py     # Geração do relatório PDF
├── styles/
│   └── style.py            # CSS customizado (cards e filtros)
├── requirements.txt        # Dependências com versões fixadas
└── database.db             # Banco SQLite (criado na primeira execução e fora do git)
```

---

## Como executar

### Pré-requisitos

- Python 3.13 ou superior
- Conda ou `venv`

### 1. Criar e ativar o ambiente

Com conda:

```bash
conda create --name dashboard python=3.13
conda activate dashboard
```

Ou com `venv`:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate
```

### 2. Instalar as dependências

```bash
pip install -r requirements.txt
```

### 3. Rodar a aplicação

```bash
streamlit run app.py
```

A app abre no navegador em `http://localhost:8501`.

### Remover o ambiente (opcional)

```bash
conda deactivate
conda remove --name dashboard --all
```

---

## Limitações conhecidas

- **Delta "vs meta" no card de Receita Total:** o percentual é um número aleatório entre -5% e +15%, gerado de novo a cada interação. Ele não compara a receita com nenhuma meta real.
- **Caracteres no PDF:** o relatório usa a codificação Latin-1. Caracteres fora dela aparecem como `?`, e os nomes de produto são cortados em 20 caracteres.
- **Valores em R$:** os números usam o formato americano, com vírgula para milhar e ponto para decimal. Exemplo: `R$ 1,234.56`.
