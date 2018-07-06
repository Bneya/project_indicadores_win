import pymysql as sql
import sqlite3

'''Este script solo sirve para subir la base de datos de sqlite a mysql'''

DATABASE = sql.connect("localhost", "root", None, "registro")

CURSOR = DATABASE.cursor()

TABLA_SQLITE3 = sqlite3.connect("important_questions.sqlite")
CURSOR_SQLITE3 = TABLA_SQLITE3.cursor()

CURSOR_SQLITE3.execute("SELECT * from important_questions")

datos_originales = CURSOR_SQLITE3.fetchall()

# Borra todo lo de la TABLA en mysql
CURSOR.execute("truncate table preguntas_importantes")

for row in datos_originales:
    print(row)
    CURSOR.execute("INSERT INTO preguntas_importantes VALUES {}".format(row))

DATABASE.commit()
