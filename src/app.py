import streamlit as st
import pandas as pd
from datetime import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Funções que você já tem

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
    st.write("R²:", r2_score(y_test, y_pred))
    st.write("MAE:", mean_absolute_error(y_test, y_pred))
    return modelo

def plot_previsao_7dias(modelo, ponto, horario, df):
    def hora_para_numero(t):
        return t.hour + t.minute / 60

    hoje = datetime.today().date()
    datas = [hoje + timedelta(days=i) for i in range(7)]

    previsoes = []
    labels = []

    X_cols = df.drop(columns=['Número de Veículos', 'Data', 'Hora']).columns
    hora_num = hora_para_numero(horario)

    for data in datas:
        try:
            dia_semana_pt = data.strftime('%A')
        except:
            dia_semana_pt = data.strftime('%A')

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

    plt.figure(figsize=(10,5))
    plt.plot(labels, previsoes, marker='o')
    plt.title(f'Previsão em {ponto} às {horario.strftime("%H:%M")} para os próximos 7 dias')
    plt.xlabel('Data')
    plt.ylabel('Número previsto de veículos')
    plt.grid(True)
    plt.tight_layout()
    st.pyplot(plt)
    plt.close()

# Streamlit UI

st.title("App de Previsão de Fluxo de Tráfego")

data_path = "../data/dados_trafego_limpos.csv"
df = load_data(data_path)

ponto_selecionado = st.selectbox("Escolha o ponto de contagem", df['Ponto de Contagem'].unique())
horario_selecionado = st.time_input("Escolha o horário", time(8, 0))

df_model = preparar_dados_para_modelo(df)
modelo = treinar_modelo(df_model)

if st.button("Gerar Previsão"):
    plot_previsao_7dias(modelo, ponto_selecionado, horario_selecionado, df_model)
