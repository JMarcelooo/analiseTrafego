import pandas as pd
import numpy as np

# Configurações básicas
pontos = ['Avenida João da Escóssia', 'BR-304', 'Centro', 'Avenida Presidente Dutra']
datas = pd.date_range(start='2025-05-01', end='2025-05-07', freq='D')  # uma semana
horarios = list(range(6, 21))  # das 6h às 21h (intervalo horário)

dados = []

for data in datas:
    dia_semana = data.dayofweek  # 0=segunda, 6=domingo
    for ponto in pontos:
        for hora in horarios:
            # Simula número base de veículos
            base = 20
            
            # Ajusta conforme horário - simula pico (7-9h e 17-19h)
            if 7 <= hora <= 9 or 17 <= hora <= 19:
                base += 80
            
            # Ajusta conforme dia da semana - menos veículos no fim de semana
            if dia_semana >= 5:  # sábado e domingo
                base = base * 0.5
            
            # Variação aleatória +/- 10%
            var = base * 0.1
            num_veiculos = int(np.random.normal(loc=base, scale=var))
            if num_veiculos < 0:
                num_veiculos = 0
            
            dados.append({
                'Data': data.strftime('%Y-%m-%d'),
                'Hora': f"{hora:02d}:00",
                'Ponto de Contagem': ponto,
                'Número de Veículos': num_veiculos
            })

# Cria DataFrame
df = pd.DataFrame(dados)

# Salva em CSV para usar depois
df.to_csv('dados_trafego_ficticios.csv', index=False)

print(df.head(10))
