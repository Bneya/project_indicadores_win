import decimal
import json
# import pymysql as sql
from decimal import Decimal as D
import sql_management as sqlmng
import algorithm_analizar_indicador as analizar

class DBBrowser:

    def __init__(self):
        self.target_ip = None
        # self.load_saved_settings()

        self.dbmanager = sqlmng.DBManager()
        self.dbb = None
        self.connect_to_db()

        self.cursor = self.dbb.cursor()
        self.subcursor = self.dbb.cursor()

        decimal.getcontext().prec = 2

    def getall_entries_table(self, table_number):
        '''Retorna todos los valores de la tabla table_number'''

        # self.cursor = self.dbb.cursor()
        query = "SELECT * FROM `{}`".format(table_number)
        # print("query", query)
        self.cursor.execute(query)

        data = self.cursor.fetchall()
        print("DATA")

        # for row in data[3:5]:
        #     print(row)
        #     result = self.eval_entry(table_number, row)
        #     print("result", result)

        return data

    def load_saved_settings(self):
        '''Carga las configs de data/settings.json (no hace nada ahora)'''

        save_file = open("data/settings.json")
        config_dict = json.load(save_file)
        self.target_ip = config_dict["target_ip"]
        save_file.close()

    def connect_to_db(self):

        # self.dbb = sql.connect(self.target_ip, "root", None, "registro")
        self.dbb = self.dbmanager.connect_propio()

    def getif_betweendates(self, table_number, idate, fdate):
        '''Retorna todos los valores de la tabla table_number
        que estén entre idate y fdate'''

        print("idate: {}; fdate: {}".format(idate, fdate))

        query = '''SELECT *
                   FROM `{}`
                   WHERE fecha >= {}
                   AND fecha <= {}'''.format(table_number, idate, fdate)

        self.cursor.execute(query)
        data = self.cursor.fetchall()
        # print("DATA")
        # for entry in data:
        #     print(entry)
        return data

    def get_importants_of_table(self, table_number):
        query = '''SELECT important
                   FROM preguntas_importantes
                   WHERE id = {}'''.format(table_number)

        self.cursor.execute(query)
        preguntas_importantes = self.cursor.fetchone()[0].split(";")
        # print("PREGUNTAS IMPORTANTES: ", preguntas_importantes)

        return preguntas_importantes

    def eval_entry(self, table_number, row):
        '''Evalúa para una entrada de pregunta si es 0 o 1 general, retorna
        ese valor'''

        sub_query = '''SELECT important
                       FROM preguntas_importantes
                       WHERE id = {}'''
        self.subcursor.execute(sub_query.format(table_number))
        importants = self.subcursor.fetchone()[0]
        # print(importants, type(importants))

        if importants == "0":
            if "0" in row[7:]:
                result = 0
            else:
                result = 1

        else:
            actual_index = 1
            for entry in row[7:]:
                # print("index", row.index(entry))
                print("entry", entry)
                print("row index", actual_index)
                print("Importants", importants)
                if str(actual_index) in importants:
                    if entry == "0":
                        result = 0
                        break
                else:
                    result = 1
                actual_index += 1

        return result

    def calculate_group(self, entry_group, table_number):
        '''Realiza análisis de grupo de preguntas entry_group,
        retorna el resumen'''

        try:
            sub_data = [[] for _ in range(len(entry_group[0][7:]))][:-1]
            nquestions = len(entry_group[0][7:]) - 1
            # print("n questions calculate group", nquestions)
            finals = []
        except IndexError:
            return ("error", "La tabla no tiene entradas")

        # print("sub data", sub_data)
        for entry in entry_group:

            final = self.eval_entry(table_number, entry)
            finals.append(final)

            # print("entry", entry)
            for i in range(nquestions):
                # print("nquestiosn", nquestions)
                # print("entry", entry[i + 7])
                sub_data[i].append(int(entry[i + 7]))
        sub_data.append(finals)
        resume = self.get_percentajes_group(sub_data)
        # print("sub_data", sub_data)
        # print("resume", resume)

        aux_query = '''SELECT questions
                       FROM preguntas_importantes
                       WHERE id = {}'''
        self.cursor.execute(aux_query.format(table_number))
        preguntas = self.cursor.fetchone()[0].split(";")
        preguntas.append("Total")
        # print("PREGUNTAS")
        # print(preguntas)

        to_return = []
        for i in range(len(preguntas)):
            aux = (preguntas[i], *resume[i])
            to_return.append(aux)

        # print("TO RETURN")
        # print(to_return)

        return to_return

    def get_percentajes_group(self, sub_data):
        '''Obtiene los porcentajes de completación de un grupo de preguntas'''

        # Saca la última columna porque son las notas
        # sub_data = sub_data[:-2]
        # print("sub_data", sub_data)
        resume_data = []

        for question in sub_data:
            # print("question", question)
            total = len(question)
            yesq = sum(question)
            percent = float(D(yesq)/D(total))
            resume_data.append((yesq, total, percent))
        return resume_data

    def complete_resume_table(self, table_number):
        '''Obtiene resumen de una tabla completa, recibe el número de tabla'''

        # entry_group = self.getall_entries_table(table_number)
        # to_return = self.calculate_group(entry_group, table_number)
        # return to_return

        # ----------------- HACIENDO PRUEBAS CON NUEVO ALGORITMO
        return analizar.get_indicator_all_dates(self.cursor, table_number)

    def between_dates_resume(self, table_number, idate, fdate):
        '''Obtiene resumen entre fechas y retorna para mostrarlo'''

        entry_group = self.getif_betweendates(table_number, idate, fdate)
        print("entry group", entry_group)
        to_return = self.calculate_group(entry_group, table_number)

        return to_return

    def get_nombre_pautas(self):
        '''Retorna lista de nombres de todas las pautas en la DB'''

        query = '''SELECT id, name
                   FROM preguntas_importantes'''
        self.cursor.execute(query)

        nombres_raw = self.cursor.fetchall()
        nombres = ["{}- {}".format(nom[0], nom[1]) for nom in nombres_raw]
        return nombres


if __name__ == '__main__':
    DBB = DBBrowser()
    print(DBB.complete_resume_table("3"))
    DBB.between_dates_resume("3", "20171230", "20180111")
