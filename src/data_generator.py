import pandas as pd
import numpy as np
import random

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
                base += 80  # Aumenta para os horários de pico
            
            # Ajusta conforme dia da semana - menos veículos no fim de semana
            if dia_semana >= 5:  # sábado e domingo
                base = base * 0.5
            
            # Variação aleatória +/- 25% para uma maior variância
            var = base * 0.25  # Variância maior (25% do valor base)
            num_veiculos = int(np.random.normal(loc=base, scale=var))
            if num_veiculos < 0:
                num_veiculos = 0
            
            # Adicionar dados inválidos intencionalmente
            if random.random() < 0.005:  # 5% de chance de gerar dados inválidos
                if random.random() < 0.5:
                    # Adicionar horário inválido (fora do intervalo)
                    hora = random.choice([25, 26])  # Hora inválida
                    num_veiculos = random.randint(-10, -1)  # Número de veículos negativo
                else:
                    # Adicionar data faltando
                    data = None  # Data inválida
                    hora = f"{random.randint(0, 24)}:00"  # Hora inválida
                    num_veiculos = random.randint(-10, -1)  # Número de veículos negativo

            dados.append({
                'Data': data.strftime('%Y-%m-%d') if data else None,
                'Hora': f"{hora:02d}:00" if isinstance(hora, int) else hora,
                'Ponto de Contagem': ponto,
                'Número de Veículos': num_veiculos
            })

# Cria DataFrame
df = pd.DataFrame(dados)

# Salvando em um arquivo .csv
file_path = '../data/dados_trafego_ficticios.csv'
df.to_csv(file_path, index=False)

# Mostrar o caminho do arquivo gerado
file_path