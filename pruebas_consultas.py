import pymysql


conn = pymysql.connect("localhost", "ucirepor_usuario", "usuario", "registro")

cursor1 = conn.cursor()

cursor1.execute("SELECT id, name from preguntas_importantes")

for row in cursor1:
    print(row)
