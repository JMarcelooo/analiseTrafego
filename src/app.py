import streamlit as st
from datetime import time
import locale

from analysis import average_vehicles_by_hour, plot_average_vehicles_by_hour, average_vehicles_by_day, plot_average_vehicles_by_day
from prediction import preparar_dados_para_modelo, treinar_modelo, plot_previsao_7dias, plot_previsao_7dias_com_outline_ponto
from relatory_generator import gerar_relatorio_pdf

def load_data_from_db():
    import pandas as pd
    from sqlalchemy import create_engine
    from dotenv import load_dotenv
    import os

    load_dotenv()
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    query = 'SELECT "DateTime", "Junction", "Vehicles" FROM trafego'
    df = pd.read_sql_query(query, engine)

    df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')
    df = df.dropna(subset=['DateTime'])

    df['Data'] = df['DateTime'].dt.date
    df['Hora'] = df['DateTime'].dt.time

    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
    except locale.Error:
        try:
            locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
        except locale.Error:
            st.warning("Locale pt_BR não disponível, nomes de dias ficarão em inglês.")

    df['Dia_da_Semana'] = df['DateTime'].dt.day_name().str.capitalize()

    df.rename(columns={'Junction': 'Ponto de Contagem', 'Vehicles': 'Número de Veículos'}, inplace=True)

    return df

st.title("App de Previsão de Fluxo de Tráfego")

# Carrega os dados
df = load_data_from_db()

# Mostrar médias e gráficos
st.subheader("Média de Veículos por Hora")
df_avg_hour = average_vehicles_by_hour(df)
fig_hour, ax_hour = plot_average_vehicles_by_hour(df_avg_hour)
st.pyplot(fig_hour)

st.subheader("Média de Veículos por Dia da Semana")
df_avg_day = average_vehicles_by_day(df)
fig_day, ax_day = plot_average_vehicles_by_day(df_avg_day)
st.pyplot(fig_day)

st.sidebar.header("Configurações de Previsão")

# Cria modelo e std uma única vez e guarda em sessão
if 'modelo' not in st.session_state or 'std_residuo' not in st.session_state or 'df_model' not in st.session_state:
    df_model = preparar_dados_para_modelo(df)
    modelo, std_residuo = treinar_modelo(df_model)
    st.session_state['modelo'] = modelo
    st.session_state['std_residuo'] = std_residuo
    st.session_state['df_model'] = df_model
else:
    modelo = st.session_state['modelo']
    std_residuo = st.session_state['std_residuo']
    df_model = st.session_state['df_model']

# Seletor e botão para previsão normal
ponto_selecionado = st.sidebar.selectbox("Escolha o ponto de contagem para previsão normal", df['Ponto de Contagem'].unique())
horario_selecionado = st.sidebar.time_input("Escolha o horário para previsão normal", time(8, 0))

if st.sidebar.button("Gerar Previsão"):
    if ponto_selecionado and horario_selecionado:
        st.subheader(f"Previsão de Fluxo para {ponto_selecionado} às {horario_selecionado}")
        fig_previsao = plot_previsao_7dias(modelo, ponto_selecionado, horario_selecionado, df_model)
        st.pyplot(fig_previsao)
    else:
        st.warning("Por favor, selecione um ponto de contagem e um horário.")

st.sidebar.markdown("---")  # Divisória

# Seletor e botão para previsão outline (apenas ponto, sem horário)
ponto_selecionado_outline = st.sidebar.selectbox("Escolha o ponto de contagem para previsão Outline", df['Ponto de Contagem'].unique(), key="outline_ponto")

if st.sidebar.button("Previsão Outline"):
    if ponto_selecionado_outline:
        st.subheader(f"Previsão de Fluxo com Intervalo de Confiança para {ponto_selecionado_outline} (Média do Horário)")
        fig_real, fig_previsao = plot_previsao_7dias_com_outline_ponto(modelo, std_residuo, ponto_selecionado_outline, df)
        st.pyplot(fig_real)
        st.pyplot(fig_previsao)
    else:
        st.warning("Por favor, selecione um ponto de contagem.")

st.sidebar.markdown("---")  # Divisória

# Botão para gerar relatório PDF
if st.sidebar.button("Gerar Relatório PDF"):
    fig_previsao = plot_previsao_7dias(modelo, ponto_selecionado, horario_selecionado, df_model)
    fig_real, fig_outline = plot_previsao_7dias_com_outline_ponto(modelo, std_residuo, ponto_selecionado, df)
    gerar_relatorio_pdf(df_avg_hour, df_avg_day, "relatorio_fluxo_trafego.pdf", fig_previsao, fig_outline)
    st.success("Relatório PDF gerado com sucesso!")
