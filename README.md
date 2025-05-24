# Projeto de Análise e Previsão de Fluxo de Tráfego

## Objetivos

Este projeto tem como objetivo analisar o fluxo de veículos em diferentes pontos da cidade de Mossoró, utilizando dados coletados de sensores fictícios. Através de técnicas de mineração de dados e modelagem preditiva, buscamos identificar padrões de tráfego por hora e dia da semana, além de prever o volume de veículos para os próximos dias em pontos e horários específicos.

A solução inclui:
- Limpeza e preparação dos dados;
- Análise exploratória com gráficos de médias por hora e dia da semana;
- Treinamento de modelo preditivo (regressão linear) para previsão de fluxo;
- Geração de relatórios em PDF com os resultados das análises;
- Aplicação web interativa para visualização das previsões usando Streamlit.

## Estrutura do projeto

- `data/` - pasta para arquivos de dados (CSV limpos e brutos);
- `src/` - código-fonte do projeto, incluindo:
  - `analysis.py` - análise e modelagem;
  - `pdf_report.py` - geração de relatórios em PDF;
  - `app.py` - aplicação web com Streamlit;
- `requirements.txt` - lista de dependências Python.

## Requisitos

- Python 3.7 ou superior

## Instalação

1. Clone este repositório:


```bash
git clone https://github.com/seu-usuario/projeto-trafego.git
```

2. Vá para o diretório do projeto
```bash
cd analiseTrafego
```

3. Crie um ambiente virtual (recomendado):
    
```bash
python -m venv venv
```

4. Ative o ambiente virtual:
```bash
.\venv\Scripts\Activate.ps1
```

5. Instale as dependências:
```bash
pip install -r requirements.txt
```