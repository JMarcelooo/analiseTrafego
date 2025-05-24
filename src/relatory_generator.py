import os
import matplotlib.pyplot as plt
from fpdf import FPDF
import pandas as pd

def gerar_grafico_media_veiculos_por_hora(df_avg_hour, arquivo_saida):
    plt.figure(figsize=(10,5))
    df_avg_hour['Hora_str'] = df_avg_hour['Hora'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')
    for ponto in df_avg_hour['Ponto de Contagem'].unique():
        dados_ponto = df_avg_hour[df_avg_hour['Ponto de Contagem'] == ponto]
        plt.plot(dados_ponto['Hora_str'], dados_ponto['Número de Veículos'], marker='o', label=ponto)
    plt.title('Média de Veículos por Hora em Cada Ponto')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número Médio de Veículos')
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig(arquivo_saida)
    plt.close()

def gerar_grafico_media_veiculos_por_dia(df_avg_day, arquivo_saida):
    plt.figure(figsize=(10,5))
    import seaborn as sns
    sns.barplot(data=df_avg_day, x='Dia_da_Semana', y='Número de Veículos', hue='Ponto de Contagem')
    plt.title('Média de Veículos por Dia da Semana em Cada Ponto')
    plt.xlabel('Dia da Semana')
    plt.ylabel('Número Médio de Veículos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(arquivo_saida)
    plt.close()

def gerar_relatorio_pdf(df_avg_hour, df_avg_day, arquivo_pdf):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório de Análise de Fluxo de Tráfego", ln=True, align='C')

    pdf.set_font("Arial", '', 12)
    pdf.ln(10)
    pdf.multi_cell(0, 10, "Este relatório apresenta a análise do fluxo de veículos em diversos pontos da cidade, com dados agrupados por hora e por dia da semana. As informações abaixo incluem gráficos e resumos que ajudam na compreensão dos padrões de tráfego.")

    # Gráfico média por hora
    arquivo_graf_hora = "grafico_media_hora.png"
    gerar_grafico_media_veiculos_por_hora(df_avg_hour, arquivo_graf_hora)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Média de Veículos por Hora", ln=True)
    pdf.image(arquivo_graf_hora, w=180)
    
    # Gráfico média por dia da semana
    arquivo_graf_dia = "grafico_media_dia.png"
    gerar_grafico_media_veiculos_por_dia(df_avg_day, arquivo_graf_dia)
    pdf.ln(10)
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(0, 10, "Média de Veículos por Dia da Semana", ln=True)
    pdf.image(arquivo_graf_dia, w=180)

    # Salvar PDF
    pdf.output(arquivo_pdf)

    # Remover imagens temporárias
    os.remove(arquivo_graf_hora)
    os.remove(arquivo_graf_dia)

    print(f"Relatório gerado: {arquivo_pdf}")
    
