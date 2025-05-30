import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates  # <-- adicione esta linha
from datetime import datetime, timedelta, time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import locale

def load_data_from_db():
    load_dotenv()
    host = os.getenv('DB_HOST')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')
    query = 'SELECT "DateTime", "Junction", "Vehicles" FROM trafego'  # ajuste o nome da tabela se necessário
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
            print("Locale pt_BR não disponível, dias da semana ficarão em inglês.")

    df['Dia_da_Semana'] = df['DateTime'].dt.day_name().str.capitalize()

    df.rename(columns={'Vehicles': 'Número de Veículos', 'Junction': 'Ponto de Contagem'}, inplace=True)

    return df

def preparar_dados_para_modelo(df):
    def hora_para_numero(t):
        return t.hour + t.minute / 60
    df['Hora_num'] = df['Hora'].apply(hora_para_numero)
    df = pd.get_dummies(df, columns=['Dia_da_Semana', 'Ponto de Contagem'], drop_first=True)
    return df

def treinar_modelo(df):
    X = df.drop(columns=['Número de Veículos', 'Data', 'Hora', 'DateTime'])
    y = df['Número de Veículos']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    residuos = y_test - y_pred
    std_residuo = np.std(residuos)

    print("R²:", r2_score(y_test, y_pred))
    print("MAE:", mean_absolute_error(y_test, y_pred))

    return modelo, std_residuo

def plot_previsao_7dias(modelo, ponto, horario, df):
    dias_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    def hora_para_numero(t):
        return t.hour + t.minute / 60

    hoje = datetime.today().date()
    datas = [hoje + timedelta(days=i) for i in range(7)]

    previsoes = []
    labels = []

    X_cols = df.drop(columns=['Número de Veículos', 'Data', 'Hora', 'DateTime']).columns
    hora_num = hora_para_numero(horario)

    for data in datas:
        dia_semana_en = data.strftime('%A')
        dia_semana_pt = dias_pt.get(dia_semana_en, dia_semana_en)

        labels.append(data.strftime('%a %d/%m'))

        data_pred = {col: 0 for col in X_cols}
        data_pred['Hora_num'] = hora_num

        dia_col = f'Dia_da_Semana_{dia_semana_pt}'
        ponto_col = f'Ponto de Contagem_{ponto}'

        if dia_col in data_pred:
            data_pred[dia_col] = 1
        if ponto_col in data_pred:
            data_pred[ponto_col] = 1

        X_pred = pd.DataFrame([data_pred])
        pred = modelo.predict(X_pred)[0]
        previsoes.append(max(0, pred))

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, previsoes, marker='o', color='b', label=f'{ponto} - {horario.strftime("%H:%M")}')
    ax.set_title(f'Previsão de veículos em {ponto} às {horario.strftime("%H:%M")} para os próximos 7 dias')
    ax.set_xlabel('Data')
    ax.set_ylabel('Número previsto de veículos')
    ax.grid(True)
    ax.legend()

    return fig


def plot_previsao_7dias_com_outline_ponto(modelo_global, std_residuo_global, ponto, df_original):
    # Filtra dados do ponto específico
    df_ponto = df_original[df_original['Ponto de Contagem'] == ponto].copy()

    # Filtra só dados do mesmo dia do mês (exemplo: dia 10)
    dia_hoje = datetime.today().day
    df_ponto_dia_mes = df_ponto[df_ponto['Data'].apply(lambda d: d.day == dia_hoje)]

    if df_ponto_dia_mes.empty:
        print("Nenhum dado histórico para o dia do mês especificado.")
        # Pode lançar figura vazia ou mensagem no Streamlit
        return None

    df_ponto_model = preparar_dados_para_modelo(df_ponto_dia_mes)

    # Treina modelo para este ponto e dia
    X = df_ponto_model.drop(columns=['Número de Veículos', 'Data', 'Hora', 'DateTime'])
    y = df_ponto_model['Número de Veículos']
    modelo = LinearRegression()
    modelo.fit(X, y)
    y_pred = modelo.predict(X)
    residuos = y - y_pred
    std_residuo = np.std(residuos)

    dias_pt = {
        'Monday': 'Segunda-feira',
        'Tuesday': 'Terça-feira',
        'Wednesday': 'Quarta-feira',
        'Thursday': 'Quinta-feira',
        'Friday': 'Sexta-feira',
        'Saturday': 'Sábado',
        'Sunday': 'Domingo'
    }

    hoje = datetime.today().date()
    datas_previsao = [hoje + timedelta(days=i) for i in range(7)]

    previsoes = []
    upper = []
    lower = []

    X_cols = df_ponto_model.drop(columns=['Número de Veículos', 'Data', 'Hora', 'DateTime']).columns
    media_hora_num = df_ponto_model['Hora_num'].mean()

    for data in datas_previsao:
        dia_semana_en = data.strftime('%A')
        dia_semana_pt = dias_pt.get(dia_semana_en, dia_semana_en)

        data_pred = {col: 0 for col in X_cols}
        dia_col = f'Dia_da_Semana_{dia_semana_pt}'
        if dia_col in data_pred:
            data_pred[dia_col] = 1

        ponto_col = f'Ponto de Contagem_{ponto}'
        if ponto_col in data_pred:
            data_pred[ponto_col] = 1

        data_pred['Hora_num'] = media_hora_num

        X_pred = pd.DataFrame([data_pred])
        pred = modelo.predict(X_pred)[0]

        previsoes.append(pred)
        upper.append(pred + 1.96 * std_residuo)
        lower.append(max(0, pred - 1.96 * std_residuo))

    # Gráfico 1: histórico do dia do mês (pontos reais)
    fig, ax = plt.subplots(figsize=(12, 6))
    datas_reais = pd.to_datetime(df_ponto_dia_mes['Data'])
    ax.scatter(datas_reais, df_ponto_dia_mes['Número de Veículos'], color='red', s=20, alpha=0.6, label='Dados Reais')
    ax.set_title(f'Dados Reais para {ponto} no Dia {dia_hoje} do Mês')
    ax.set_xlabel('Data')
    ax.set_ylabel('Número de Veículos')
    ax.grid(True)
    ax.legend()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    fig.autofmt_xdate()

    # Gráfico 2: previsão próximos 7 dias com intervalo
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    ax2.plot(datas_previsao, previsoes, marker='o', color='blue', label='Previsão Próximos 7 dias')
    ax2.fill_between(datas_previsao, lower, upper, color='blue', alpha=0.2, label='Intervalo de Confiança 95%')
    ax2.set_title(f'Previsão de veículos em {ponto} para os próximos 7 dias (média horário)')
    ax2.set_xlabel('Data')
    ax2.set_ylabel('Número previsto de veículos')
    ax2.grid(True)
    ax2.legend()
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    fig2.autofmt_xdate()

    return fig, fig2


