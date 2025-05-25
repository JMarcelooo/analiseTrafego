import streamlit as st
import pandas as pd
from datetime import time
from analysis import load_data, average_vehicles_by_hour, plot_average_vehicles_by_hour, average_vehicles_by_day, plot_average_vehicles_by_day
from prediction import preparar_dados_para_modelo, treinar_modelo, plot_previsao_7dias
from relatory_generator import gerar_grafico_media_veiculos_por_hora, gerar_grafico_media_veiculos_por_dia, gerar_relatorio_pdf

# Título do aplicativo
st.title("App de Previsão de Fluxo de Tráfego")

# Carregar os dados
data_path = "../data/dados_trafego_limpos.csv"
df = load_data(data_path)

# Exibir gráficos de média de veículos por hora
st.subheader("Média de Veículos por Hora")
df_avg_hour = average_vehicles_by_hour(df)
fig_hour, ax_hour = plot_average_vehicles_by_hour(df_avg_hour)  # Chama a função e obtém a figura
st.pyplot(fig_hour)  # Exibe a figura no Streamlit

# Exibir gráficos de média de veículos por dia
st.subheader("Média de Veículos por Dia da Semana")
df_avg_day = average_vehicles_by_day(df)
fig_day, ax_day = plot_average_vehicles_by_day(df_avg_day)  # Chama a função e obtém a figura
st.pyplot(fig_day)  # Exibe a figura no Streamlit

# Entradas para previsão
st.sidebar.header("Configurações de Previsão")
ponto_selecionado = st.sidebar.selectbox("Escolha o ponto de contagem", df['Ponto de Contagem'].unique())
horario_selecionado = st.sidebar.time_input("Escolha o horário", time(8, 0))

# Preparar os dados e treinar o modelo
df_model = preparar_dados_para_modelo(df)
modelo = treinar_modelo(df_model)

# Gerar a previsão quando o botão for clicado
if st.sidebar.button("Gerar Previsão"):
    if ponto_selecionado and horario_selecionado:
        st.subheader(f"Previsão de Fluxo para {ponto_selecionado} às {horario_selecionado}")
        fig_previsao = plot_previsao_7dias(modelo, ponto_selecionado, horario_selecionado, df_model)
        st.pyplot(fig_previsao)  # Exibe o gráfico gerado
    else:
        st.warning("Por favor, selecione um ponto de contagem e um horário.")


# Gerar o relatório PDF com gráficos
if st.sidebar.button("Gerar Relatório PDF"):
    gerar_relatorio_pdf(df_avg_hour, df_avg_day, "relatorio_fluxo_trafego.pdf")
    st.success("Relatório PDF gerado com sucesso!")
