import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(filepath):
    df = pd.read_csv(filepath)
    df['Data'] = pd.to_datetime(df['Data'], errors='coerce')
    df['Hora'] = pd.to_datetime(df['Hora'], errors='coerce').dt.time
    try:
        df['Dia_da_Semana'] = df['Data'].dt.day_name(locale='pt_BR')
    except:
        df['Dia_da_Semana'] = df['Data'].dt.day_name()
    df = df.dropna(subset=['Data', 'Hora'])
    return df

def average_vehicles_by_hour(df):
    return df.groupby(['Ponto de Contagem', 'Hora'])['Número de Veículos'].mean().reset_index()

def plot_average_vehicles_by_hour(df_avg):
    # Converter Hora para string 'HH:MM' para facilitar o gráfico
    df_avg['Hora_str'] = df_avg['Hora'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')
    
    plt.figure(figsize=(12,6))
    sns.lineplot(data=df_avg, x='Hora_str', y='Número de Veículos', hue='Ponto de Contagem', marker='o')
    plt.title('Média de Veículos por Hora em Cada Ponto de Contagem')
    plt.xlabel('Hora do Dia')
    plt.ylabel('Número Médio de Veículos')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def average_vehicles_by_day(df):
    return df.groupby(['Ponto de Contagem', 'Dia_da_Semana'])['Número de Veículos'].mean().reset_index()

def plot_average_vehicles_by_day(df_avg):
    # Criação da figura e eixos
    fig, ax = plt.subplots(figsize=(12,6))
    
    # Gerar o gráfico de barras
    sns.barplot(data=df_avg, x='Dia_da_Semana', y='Número de Veículos', hue='Ponto de Contagem', ax=ax)
    
    # Configuração do gráfico
    ax.set_title('Média de Veículos por Dia da Semana em Cada Ponto de Contagem')
    ax.set_xlabel('Dia da Semana')
    ax.set_ylabel('Número Médio de Veículos')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)

    # Retorna a figura e os eixos para uso no Streamlit
    return fig, ax
    
def plot_average_vehicles_by_hour(df_avg_hour):
    df_avg_hour['Hora_str'] = df_avg_hour['Hora'].apply(lambda x: x.strftime('%H:%M') if pd.notnull(x) else '')

    # Criar a figura e eixos explicitamente
    fig, ax = plt.subplots(figsize=(12, 6))
    for ponto in df_avg_hour['Ponto de Contagem'].unique():
        dados_ponto = df_avg_hour[df_avg_hour['Ponto de Contagem'] == ponto]
        ax.plot(dados_ponto['Hora_str'], dados_ponto['Número de Veículos'], marker='o', label=ponto)

    ax.set_title('Média de Veículos por Hora em Cada Ponto de Contagem')
    ax.set_xlabel('Hora do Dia')
    ax.set_ylabel('Número Médio de Veículos')
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.legend()
    ax.grid(True)

    return fig, ax  # Retorna a figura e eixos para uso no Streamlit
    

if __name__ == "__main__":
    data_path = "../data/dados_trafego_limpos.csv"
    df = load_data(data_path)
    
    df_avg_hour = average_vehicles_by_hour(df)
    plot_average_vehicles_by_hour(df_avg_hour)
    
    df_avg_day = average_vehicles_by_day(df)
    plot_average_vehicles_by_day(df_avg_day)
