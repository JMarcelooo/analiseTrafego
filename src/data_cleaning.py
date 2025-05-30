import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import os
import locale

load_dotenv()

host = os.getenv('DB_HOST')
database = os.getenv('DB_NAME')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASSWORD')

engine = create_engine(f'postgresql://{user}:{password}@{host}/{database}')

tabela_origem = 'trafego_limpo'  # Substitua pelo nome correto da tabela original

# Ler dados do banco
df = pd.read_sql_query(f'SELECT "DateTime", "Junction", "Vehicles" FROM {tabela_origem}', engine)

# Converter "DateTime" para datetime
df['DateTime'] = pd.to_datetime(df['DateTime'], errors='coerce')

# Remover linhas com "DateTime" inválido
df = df.dropna(subset=['DateTime'])

# Criar colunas Data e Hora separadas
df['Data'] = df['DateTime'].dt.date
df['Hora'] = df['DateTime'].dt.time

# Configurar locale para português (Brasil)
try:
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')
except locale.Error:
    try:
        locale.setlocale(locale.LC_TIME, 'Portuguese_Brazil.1252')
    except locale.Error:
        print("Locale pt_BR não disponível, nomes de dias ficarão em inglês.")

df['Dia da Semana'] = df['DateTime'].dt.day_name()
df['Dia da Semana'] = df['Dia da Semana'].str.capitalize()

# Renomear coluna 'Vehicles' para 'Número de Veículos'
df.rename(columns={'Vehicles': 'Número de Veículos'}, inplace=True)

# Filtrar valores negativos em 'Número de Veículos'
df = df[df['Número de Veículos'] >= 0]

df = df.reset_index(drop=True)

# Selecionar colunas para gravar na tabela final
df_limpo = df[['Data', 'Hora', 'Número de Veículos', 'Junction', 'Dia da Semana']]

# Gravar no banco na tabela 'trafego_limpo', substituindo se existir
df_limpo.to_sql('trafego_limpo', engine, if_exists='replace', index=False)

print("Dados limpos gravados na tabela 'trafego_limpo' com sucesso!")