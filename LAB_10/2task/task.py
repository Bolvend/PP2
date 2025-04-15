import psycopg2
import csv

conn = psycopg2.connect(
    host = "localhost",
    database = "snake_db",
    user = "postgres",
    password = "12345678"
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id SERIAL PRIMARY KEY,
        user_name VARCHAR(255) NOT NULL)
""")

cur.execute("""
    CREATE TABLE IF NOT EXISTS user_score(
        id SERIAL PRIMARY KEY,
        user_scoreL INT,
        user_lvl INT,
        user_speed INT
    )
""")

conn.commit()
id = int(input("New user ID: "))
user_scoreL = input("New user_name: ")
user_lvl = int(input("New user lvl: "))
user_speed = input("New speed: ")
cur.execute("INSERT INTO user_score (id, user_scoreL , user_lvl ,user_speed) VALUES (%s, %s , %s, %s)", (id, user_scoreL , user_lvl ,user_speed  ))
conn.commit()

def print_rows():
    cur.execute("""SELECT * FROM user_score;""")
    rows = cur.fetchall()
    for row in rows:
        print(row)

print_rows()