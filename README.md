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
  - `app.py` - aplicação web com Streamlit;
  - `relatory_generator.py` - geração de relatórios em PDF;
  - `data_generator.py` - criação de dados fictícios no formato .csv;
  - `data_cleaning.py` - limpeza e filtragem dos dados;
  - `analysis.py` - análise e modelagem;
  - `prediction.py` - usa dos dados pra realizar previsões
  - `db.py` - arquivo necessário para a conexão dom o banco de dados;
  - `importar_csv.py` - import de dados .csv para o banco de dados;
- `requirements.txt` - lista de dependências Python.

## Requisitos

- Python 3.7 ou superior
- Banco de Dados PostgreSQL

## Configuração do Banco de Dados PostgreSQL

Para que o projeto funcione corretamente, é necessário configurar o banco de dados PostgreSQL com os dados de tráfego. Siga os passos abaixo:

### 1. Instale o PostgreSQL

- [Download e instruções oficiais](https://www.postgresql.org/download/) para Windows, Linux ou MacOS.

### 2. Crie um banco de dados

Abra o terminal ou o pgAdmin e execute o comando para criar um banco:

```sql
CREATE DATABASE nome_do_banco;
```

### 3. Crie a tabela para armazenar os dados

```sql
CREATE TABLE trafego (
    "DateTime" TIMESTAMP NOT NULL,
    "Junction" VARCHAR(255) NOT NULL,
    "Vehicles" INTEGER NOT NULL
);
```

### 4. Importe os dados iniciais

Caso possua um arquivo CSV com dados, importe para a tabela:
```bash
psql -h localhost -U seu_usuario -d nome_do_banco -c "\copy trafego FROM 'caminho/para/seu_arquivo.csv' CSV HEADER;"
```

### 5. Configure as variáveis de ambiente

No arquivo .env do projeto, defina as credenciais do banco

```env
DB_HOST=localhost
DB_NAME=nome_do_banco
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
```

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

  - No Windows

```bash
.\venv\Scripts\Activate.ps1
```

  -  No Linux/MacOS
```bash
source venv/bin/activate
```

5. Instale as dependências:
```bash
pip install -r requirements.txt
```
