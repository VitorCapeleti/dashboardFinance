import streamlit as st
import pandas as pd
def filtros_sidebar(df):

    """
    Cria todos os widgets da sidebar (menu lateral).
    1. Exibe o cabeçalho da sidebar.
    2. Cria os filtros de data, região, categoria e produto.
    3. Aplica os filtros ao DataFrame.
    4. Retorna o DataFrame filtrado.
    
    Parâmetros:
    df (pd.DataFrame): O DataFrame original completo (antes dos filtros).
    """

    st.sidebar.markdown(
        """
        <div style="background-color:#5707f7; padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 15px;">
            <h3 style="color:white; margin:0; font-weight:bold;">Dashboard Financeiro</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.sidebar.header("🔍 Filtros")
    
    min_date = df["date"].min().date()
    max_date = df["date"].max().date()
    date_range = st.sidebar.date_input("Período de Análise", (min_date, max_date), min_value = min_date, max_value = max_date)

    all_regioes = sorted(df["regiao"].unique())
    selected_regioes = st.sidebar.multiselect("Regiões", all_regioes, default = all_regioes)

    all_categorias = sorted(df["categoria"].unique())
    selected_categorias = st.sidebar.multiselect("Categorias", all_categorias, default = all_categorias)
    
    all_produtos = sorted(df["produto"].unique())
    selected_produtos = st.sidebar.multiselect("Produtos", all_produtos, default = all_produtos)

    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        start_date, end_date = min_date, max_date

    df_filtrado = df[
        (df["date"].dt.date >= start_date) &
        (df["date"].dt.date <= end_date) &
        (df["regiao"].isin(selected_regioes)) &
        (df["categoria"].isin(selected_categorias)) &
        (df["produto"].isin(selected_produtos))
    ].copy()

    st.sidebar.markdown("---")
    with st.sidebar.expander("🆘 Suporte / Fale conosco", expanded = False):
        st.write("Se tiver dúvidas envie mensagem para email@email.com")
    
    st.sidebar.caption("Dashboard Desenvolvido para uso financeiro pessoal.")

    return df_filtrado