import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
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
            print("Locale pt_BR não disponível, nomes de dias ficarão em inglês.")

    df['Dia_da_Semana'] = df['DateTime'].dt.day_name().str.capitalize()

    df.rename(columns={'Junction': 'Ponto de Contagem', 'Vehicles': 'Número de Veículos'}, inplace=True)

    return df

def average_vehicles_by_hour(df):
    return df.groupby(['Ponto de Contagem', 'Hora'])['Número de Veículos'].mean().reset_index()

def plot_average_vehicles_by_hour(df_avg):
    df_avg['Hora_str'] = df_avg['Hora'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')

    fig, ax = plt.subplots(figsize=(12,6))
    sns.lineplot(data=df_avg, x='Hora_str', y='Número de Veículos', hue='Ponto de Contagem', marker='o', ax=ax)
    ax.set_title('Média de Veículos por Hora em Cada Ponto de Contagem')
    ax.set_xlabel('Hora do Dia')
    ax.set_ylabel('Número Médio de Veículos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    return fig, ax

def average_vehicles_by_day(df):
    return df.groupby(['Ponto de Contagem', 'Dia_da_Semana'])['Número de Veículos'].mean().reset_index()

def plot_average_vehicles_by_day(df_avg):
    fig, ax = plt.subplots(figsize=(12,6))
    sns.barplot(data=df_avg, x='Dia_da_Semana', y='Número de Veículos', hue='Ponto de Contagem', ax=ax)
    ax.set_title('Média de Veículos por Dia da Semana em Cada Ponto de Contagem')
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Número Médio de Veículos')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    plt.tight_layout()
    return fig, ax

if __name__ == "__main__":
    df = load_data_from_db()

    df_avg_hour = average_vehicles_by_hour(df)
    fig_hour, ax_hour = plot_average_vehicles_by_hour(df_avg_hour)
    plt.show()

    df_avg_day = average_vehicles_by_day(df)
    fig_day, ax_day = plot_average_vehicles_by_day(df_avg_day)
    plt.show()
