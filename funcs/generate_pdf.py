from fpdf import FPDF
from fpdf.enums import XPos, YPos
import numpy as np
import pandas as pd 
from datetime import datetime, date

def gera_pdf_report(df_filtrado, total_faturamento, total_quantidade, avg_ticket):

    """
    Gera um relatório PDF customizado usando a biblioteca FPDF.
    
    Parâmetros:
    df_filtrado (pd.DataFrame): O DataFrame filtrado.
    total_faturamento (float): O valor do KPI de faturamento.
    total_quantidade (int): O valor do KPI de quantidade.
    avg_ticket (float): O valor do KPI de ticket médio.
    
    Retorna:
    (bytes): Os bytes brutos do arquivo PDF gerado.
    """
    
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Relatorio Executivo de Vendas", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)
    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_fill_color(240, 240, 240)
    pdf.rect(10, 35, 190, 25, 'F')
    pdf.set_y(40)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(60, 8, f"Receita Total", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"Quantidade", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"Ticket Medio", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(60, 8, f"R$ {total_faturamento:,.2f}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"{total_quantidade:,}", align="C", new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(60, 8, f"R$ {avg_ticket:,.2f}", align="C", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(15)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, "Top 15 Vendas (por receita):", new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    col_widths = [30, 30, 30, 40, 25, 30] 
    headers = ["Data", "Regiao", "Categoria", "Produto", "Qtd", "Receita"]
    pdf.set_font("Helvetica", "B", 9)
    for i, h in enumerate(headers):
        pdf.cell(col_widths[i], 8, h, 1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    
    pdf.ln()
    
    pdf.set_font("Helvetica", "", 9)
    df_top = df_filtrado.sort_values("faturamento", ascending=False).head(15)
    
    for _, row in df_top.iterrows():
        
        data = [
            str(row['date'].date()),
            row['regiao'],
            row['categoria'],
            row['produto'][:20], 
            str(row['quantidade']),
            f"R$ {row['faturamento']:,.2f}"
        ]
        
        for i, d in enumerate(data):
            
            safe_txt = str(d).encode("latin-1", "replace").decode("latin-1")
            pdf.cell(col_widths[i], 7, safe_txt, 1, align=('C' if i==4 else 'L'), new_x=XPos.RIGHT, new_y=YPos.TOP)
        
        pdf.ln()

    result = pdf.output()
    return result.encode("latin-1") if isinstance(result, str) else bytes(result)

