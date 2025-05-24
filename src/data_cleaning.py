import pandas as pd
import re

# Função para validar se a string está no formato HH:MM
def validar_hora(hora_str):
    if pd.isna(hora_str):
        return False
    hora_str = str(hora_str).strip()
    # Regex para horas no formato 00:00 até 23:59
    return bool(re.match(r'^(2[0-3]|[01]?[0-9]):[0-5][0-9]$', hora_str))

df = pd.read_csv('../data/dados_trafego_ficticios.csv')

# Limpar valores nulos e espaços
df['Hora'] = df['Hora'].astype(str).str.strip()

# Mostrar os valores problemáticos que não são validados
invalid_horas = df[~df['Hora'].apply(validar_hora)]
print("Valores inválidos encontrados na coluna Hora:")
print(invalid_horas['Hora'].unique())

# Remover as linhas que possuem valores inválidos em Hora
df = df[df['Hora'].apply(validar_hora)]

# Agora converter a coluna para datetime
df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M', errors='coerce').dt.time

# Verificar se ainda existem valores NaT depois da conversão
print("Linhas com Hora inválida após conversão:")
print(df[df['Hora'].isna()])

# 1. Carregar os dados do arquivo CSV
df = pd.read_csv('../data/dados_trafego_ficticios.csv')

# 2. Visualizar as primeiras linhas para entender a estrutura
print("Primeiras linhas do dataset:")
print(df.head())

# 3. Verificar informações gerais, tipos e dados faltantes
print("\nInformações do dataframe:")
print(df.info())

# 4. Filtrar linhas com valores inválidos na coluna 'Hora'
df['Hora'] = df['Hora'].astype(str).str.strip()  # Remove espaços extras
df = df[df['Hora'].apply(validar_hora)]

# 5. Converter colunas de data e hora para formatos datetime
df['Data'] = pd.to_datetime(df['Data'], errors='coerce')  # converte, coloca NaT em erros
df['Hora'] = pd.to_datetime(df['Hora'], format='%H:%M', errors='coerce').dt.time

# 6. Verificar se houve erros na conversão (valores NaT)
print("\nLinhas com datas ou horas inválidas após validação:")
print(df[df['Data'].isna() | df['Hora'].isna()])

# 7. Remover linhas com dados inválidos
df = df.dropna(subset=['Data', 'Hora'])

# 8. Criar coluna com o dia da semana (ex: Segunda-feira)
try:
    df['Dia_da_Semana'] = df['Data'].dt.day_name(locale='pt_BR')
except:
    # Caso a localidade pt_BR não esteja disponível, usa inglês
    df['Dia_da_Semana'] = df['Data'].dt.day_name()

# 9. Verificar valores negativos ou inconsistentes na contagem de veículos
print("\nValores negativos na coluna 'Número de Veículos':")
print(df[df['Número de Veículos'] < 0])

# 10. Corrigir ou remover valores negativos (excluir linhas)
df = df[df['Número de Veículos'] >= 0]

# 11. Resetar índice após remoções
df = df.reset_index(drop=True)

print("\nDataset limpo e pronto para análise:")
print(df.info())
print(df.head())

# 12. Salvar o dataframe limpo em CSV
df.to_csv('../data/dados_trafego_limpos.csv', index=False)
