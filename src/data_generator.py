import pandas as pd
import numpy as np
import random

# Configurações básicas
pontos = ['Avenida João da Escóssia', 'BR-304', 'Centro', 'Avenida Presidente Dutra']
datas = pd.date_range(start='2025-05-01', end='2025-05-07', freq='D') 
horarios = list(range(6, 21)) 

dados = []

for data in datas:
    dia_semana = data.dayofweek  
    for ponto in pontos:
        for hora in horarios:
            base = 20
            
            if 7 <= hora <= 9 or 17 <= hora <= 19:
                base += 80
            if dia_semana >= 5:
                base = base * 0.5
            
            var = base * 0.25
            num_veiculos = int(np.random.normal(loc=base, scale=var))
            if num_veiculos < 0:
                num_veiculos = 0
            if random.random() < 0.015:
                if random.random() < 0.5:
                    hora = random.choice([25, 26])
                    num_veiculos = random.randint(-10, -1) 
                else:
                    data = None
                    hora = f"{random.randint(0, 24)}:00"
                    num_veiculos = random.randint(-10, -1)

            dados.append({
                'Data': data.strftime('%Y-%m-%d') if data else None,
                'Hora': f"{hora:02d}:00" if isinstance(hora, int) else hora,
                'Ponto de Contagem': ponto,
                'Número de Veículos': num_veiculos
            })

df = pd.DataFrame(dados)

file_path = '../data/dados_trafego_ficticios.csv'
df.to_csv(file_path, index=False)

file_path