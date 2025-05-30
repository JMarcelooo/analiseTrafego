import os
import tempfile
from fpdf import FPDF
from analysis import plot_average_vehicles_by_day, plot_average_vehicles_by_hour

def salvar_figura_temporaria(fig):
    tmp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    fig.savefig(tmp_file.name)
    fig.clf()  # limpa a figura para liberar memória
    tmp_file.close()
    return tmp_file.name

def gerar_relatorio_pdf(df_avg_hour, df_avg_day, arquivo_pdf, fig_previsao=None, fig_outline=None):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Título e texto introdutório
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "Relatório de Análise de Fluxo de Tráfego", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", '', 12)
    texto_intro = ("Este relatório apresenta a análise do fluxo de veículos em diversos pontos da cidade, "
                   "com dados agrupados por hora e por dia da semana. As informações abaixo incluem gráficos "
                   "e resumos que ajudam na compreensão dos padrões de tráfego.")
    pdf.multi_cell(0, 10, texto_intro)
    pdf.ln(10)

    # Lista de gráficos com título
    graficos = []

    fig_hour, _ = plot_average_vehicles_by_hour(df_avg_hour)
    graficos.append(("Média de Veículos por Hora", fig_hour))

    fig_day, _ = plot_average_vehicles_by_day(df_avg_day)
    graficos.append(("Média de Veículos por Dia da Semana", fig_day))

    if fig_previsao is not None:
        graficos.append(("Previsão de Fluxo para Próximos 7 Dias", fig_previsao))

    if fig_outline is not None:
        graficos.append(("Previsão com Intervalo de Confiança (Outline)", fig_outline))

    # Inserir 2 gráficos por página
    for i, (titulo, fig) in enumerate(graficos):
        if i % 2 == 0 and i != 0:
            pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.cell(0, 10, titulo, ln=True)
        arquivo_img = salvar_figura_temporaria(fig)
        pdf.image(arquivo_img, w=180)
        os.remove(arquivo_img)
        pdf.ln(10)

    # Salvar PDF
    pdf.output(arquivo_pdf)
    print(f"Relatório gerado: {arquivo_pdf}")