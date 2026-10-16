import db.initialize_db as db_init
from templates.sidebar import filtros_sidebar
from templates.cards_kpis import renderiza_cards_kpis
from funcs.generate_pdf import gera_pdf_report
from styles.style import set_custom_theme

import sqlite3 

import numpy as np 
import pandas as pd
import plotly.express as px
import streamlit as st
from fpdf import FPDF
from fpdf.enums import XPos, YPos
from datetime import datetime, date, timedelta
st.set_page_config(
    page_title="Dashboard de Vendas",
    page_icon=":100:",
    layout="wide",
    initial_sidebar_state="expanded",
)

@st.cache_data(ttl=600)
def carrega_dados():
    return db_init.carrega_dados()

def main():
    set_custom_theme()
    df = carrega_dados()
    df_filtrado = filtros_sidebar(df)

    st.title("📊 Dashboard Interativo Financeiro")
    st.subheader("Com Banco de Dados SQLite e Streamlit")
    st.write("Navegue pelo dashboard e use os filtros na barra lateral para diferentes visualizações. Os dados podem ser exportados para formato CSV e PDF.")
    st.markdown("---")
    st.markdown(f"Visão Consolidada do Financeiro com KPIs.")

    if df_filtrado.empty:
        st.warning("⚠️ Nenhum dado encontrado com os filtros selecionados.")
        return


    total_faturamento, total_qty, avg_ticket = renderiza_cards_kpis(df_filtrado)
    st.markdown("---")

    tab1, tab2 = st.tabs(["📈 Visão Gráfica", "📄 Dados Detalhados & Exportação (CSV e PDF)"])

    with tab1:
        col_left, col_right = st.columns([2, 1])
        with col_left:
            
            st.subheader("Evolução da Receita Diária")
            daily_rev = df_filtrado.groupby("date")[["faturamento"]].sum().reset_index()
            fig_line = px.line(daily_rev, x = "date", y = "faturamento", template = "plotly_dark", height = 400)
            fig_line.update_traces(fill = 'tozeroy', line = dict(color = '#00CC96', width = 3))
            st.plotly_chart(fig_line, width = 'stretch')
        with col_right:
            
            st.subheader("Mix de Categorias")
            cat_rev = df_filtrado.groupby("categoria")[["faturamento"]].sum().reset_index()
            fig_pie = px.pie(cat_rev, values="faturamento", names="categoria", hole=0.4, template="plotly_dark", height=400)
            st.plotly_chart(fig_pie, width='stretch') 

        c_a, c_b = st.columns(2)
        
        with c_a:

            st.subheader("Performance Regional")
            fig_bar = px.bar(
                df_filtrado.groupby("regiao")[["faturamento"]].sum().reset_index(),
                x="regiao", y="faturamento", color="regiao", template="plotly_dark", text_auto='.2s'
            )

            st.plotly_chart(fig_bar, width='stretch')
        with c_b:

            st.subheader("Análise Dia da Semana")
            dias_pt_map = {
                0: "Segunda-feira", 1: "Terça-feira", 2: "Quarta-feira",
                3: "Quinta-feira", 4: "Sexta-feira", 5: "Sábado", 6: "Domingo"
            }

            dias_pt_ordem = [
                "Segunda-feira", "Terça-feira", "Quarta-feira", 
                "Quinta-feira", "Sexta-feira", "Sábado", "Domingo"
            ]

            df_filtrado["weekday_num"] = df_filtrado["date"].dt.dayofweek
            df_filtrado["dia_semana"] = df_filtrado["weekday_num"].map(dias_pt_map)
            wd_rev = df_filtrado.groupby("dia_semana")[["faturamento"]].mean().reindex(dias_pt_ordem).reset_index()
            fig_heat = px.bar(wd_rev, x="dia_semana", y="faturamento", title="Receita Média x Dia", template="plotly_dark")
            st.plotly_chart(fig_heat, width='stretch')
        st.subheader("Dispersão: Quantidade x Faturamento x Produto")
        
        fig_scat = px.scatter(
            df_filtrado, x="quantidade", y="faturamento", color="categoria", size="faturamento",
            hover_data=["produto"], template="plotly_dark", height=500
        )
        
        st.plotly_chart(fig_scat, width='stretch') 

    with tab2:
        st.subheader("Visualização Tabular")
        st.dataframe(df_filtrado, width='stretch', height=400) 
        
        st.markdown("### 📥 Área de Exportação")
        
        c_exp1, c_exp2 = st.columns(2)
        
        with c_exp1:
            
            csv = df_filtrado.to_csv(index=False).encode('utf-8')
            st.download_button(
                label = "💾 Baixar CSV (Excel)",
                data = csv,
                file_name = "dados_filtrados.csv",
                mime = "text/csv",
                width = 'stretch' 
            )
        with c_exp2:
            if st.button("📄 Gerar Relatório PDF", width='stretch'): 

                with st.spinner("Renderizando PDF..."):
                    
                    pdf_bytes = gera_pdf_report(df_filtrado, total_faturamento, total_qty, avg_ticket)
                    st.download_button(
                        label = "⬇️ Clique aqui para Salvar PDF",
                        data = pdf_bytes,
                        file_name = f"Relatorio_Vendas_{date.today()}.pdf",
                        mime = "application/pdf",
                        key = "pdf-download-final"
                    )

    st.markdown("---")
    with st.expander("ℹ️ Sobre Esta Data App", expanded=False):
        st.info("Este dashboard combina as melhores práticas de visualização e manipulação de dados.")
        st.markdown("""
        **Recursos Integrados:**
        - **Engine:** Python + Streamlit + SQLite.
        - **Visualização:** Plotly Express e tema Dark no Streamlit.
        - **Relatórios:** Geração de PDF com FPDF (compatível com Latin-1).
        - **Performance:** Cache de dados (`@st.cache_data`).
        """)



if __name__ == "__main__":
    main()
