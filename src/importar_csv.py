import pandas as pd
from psycopg2 import sql
from db import connect

df = pd.read_csv('../data/traffic.csv')

conn = connect()
cur = conn.cursor()

for i, row in df.iterrows():
    columns = list(df.columns)
    values = [row[col] for col in columns]

    insert = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
        sql.Identifier('trafego'),
        sql.SQL(', ').join(map(sql.Identifier, columns)),
        sql.SQL(', ').join(sql.Placeholder() * len(values))
    )

    cur.execute(insert, values)

conn.commit()
cur.close()
conn.close()
