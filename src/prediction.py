import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score

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

def preparar_dados_para_modelo(df):
    def hora_para_numero(t):
        return t.hour + t.minute / 60
    df['Hora_num'] = df['Hora'].apply(hora_para_numero)
    df = pd.get_dummies(df, columns=['Dia_da_Semana', 'Ponto de Contagem'], drop_first=True)
    return df

def treinar_modelo(df):
    X = df.drop(columns=['Número de Veículos', 'Data', 'Hora'])
    y = df['Número de Veículos']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    modelo = LinearRegression()
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    print("R²:", r2_score(y_test, y_pred))
    print("MAE:", mean_absolute_error(y_test, y_pred))
    return modelo

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
    datas = [hoje + timedelta(days=i) for i in range(7)]  # Próximos 7 dias

    previsoes = []
    labels = []

    X_cols = df.drop(columns=['Número de Veículos', 'Data', 'Hora']).columns
    hora_num = hora_para_numero(horario)

    for data in datas:
        dia_semana_en = data.strftime('%A')
        dia_semana_pt = dias_pt.get(dia_semana_en, dia_semana_en)

        labels.append(data.strftime('%a %d/%m'))  # Labels no formato desejado

        # Criar os dados para a previsão
        data_pred = {col: 0 for col in X_cols}
        data_pred['Hora_num'] = hora_num

        # Definir variáveis categóricas com 1 (um) se necessário
        dia_col = f'Dia_da_Semana_{dia_semana_pt}'
        ponto_col = f'Ponto de Contagem_{ponto}'

        if dia_col in data_pred:
            data_pred[dia_col] = 1
        if ponto_col in data_pred:
            data_pred[ponto_col] = 1

        # Criar DataFrame de entrada para o modelo
        X_pred = pd.DataFrame([data_pred])
        pred = modelo.predict(X_pred)[0]  # Previsão do modelo
        previsoes.append(max(0, pred))  # Garantir que o valor da previsão não seja negativo

    # Criar a figura e eixos explicitamente
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(labels, previsoes, marker='o', color='b', label=f'{ponto} - {horario.strftime("%H:%M")}')
    ax.set_title(f'Previsão de veículos em {ponto} às {horario.strftime("%H:%M")} para os próximos 7 dias')
    ax.set_xlabel('Data')
    ax.set_ylabel('Número previsto de veículos')
    ax.grid(True)
    ax.legend()

    # Retornar a figura
    return fig

if __name__ == "__main__":
    data_path = "../data/dados_trafego_limpos.csv"
    df = load_data(data_path)

    df_model = preparar_dados_para_modelo(df)
    modelo = treinar_modelo(df_model)

    from datetime import time
    # Exemplo: previsão para Domingo às 16:00 na Avenida João da Escóssia
    plot_previsao_7dias(modelo, 'Avenida João da Escóssia', time(7,0), df_model)
