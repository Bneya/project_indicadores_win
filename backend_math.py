'''Engine de todos los cálculos que realiza el programa. Llama a módulos más
 pequeños (gears) para realizar tareas específicas. Funciona cmo controlador'''

import decimal
import json
import pymysql as sql

import sql_management as sqlmng
import algorithms.bend.gear_analizar_indicador as analizar
import algorithms.bend.gear_op_perform as opperform


class DBBrowser:

    def __init__(self):
        self.target_ip = None
        # self.load_saved_settings()

        self.dbmanager = sqlmng.DBManager()
        self.dbb = None
        self.connect_to_db()

        self.cursor = self.dbb.cursor()
        self.subcursor = self.dbb.cursor()
        self.keycursor = sql.cursors.DictCursor(self.dbb)

        decimal.getcontext().prec = 2

    # Posible Deprecated, no estoy seguro
    def getall_entries_table(self, table_number):
        '''Retorna todos los valores de la tabla table_number'''

        query = "SELECT * FROM `{}`".format(table_number)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        print("DATA")
        return data

    def load_saved_settings(self):
        '''Carga las configs de data/settings.json (no hace nada ahora)'''

        save_file = open("data/settings.json")
        config_dict = json.load(save_file)
        self.target_ip = config_dict["target_ip"]
        save_file.close()

    def connect_to_db(self):
        '''Conecta con la base de datos en el ervidor remoto.
        Retorna objeto Connection'''

        self.dbb = self.dbmanager.connect_propio()

    def get_importants_of_table(self, table_number):
        """Retorna la columna <importants> de la tabla <important_questions>"""

        query = '''SELECT important
                   FROM preguntas_importantes
                   WHERE id = {}'''.format(table_number)

        self.cursor.execute(query)
        preguntas_importantes = self.cursor.fetchone()[0].split(";")

        return preguntas_importantes

    def get_all_operators(self):
        """Retorna todos los id y nombre de operadores de la db"""

        query = """SELECT id_op, nombre
                   FROM operadores_table
                   WHERE estamento != 'invalid'
                   ORDER BY nombre"""

        self.cursor.execute(query)
        operadores = ["{}- {}".format(op[0], op[1]) for op in self.cursor]
        print("OPERADORESSSSSSSSSSSSSSSSSSSSS........: ", operadores)

        return operadores

    # Esta es la función que se está usando actualmente
    def get_resume_table(self, table_n, idate=False, fdate=False):
        '''Obtiene el resumen de un indicador desde siempre o entre fechas'''
        if idate:
            info_result = analizar.rt_get_info_indicator(self.cursor,
                                                         table_n=table_n,
                                                         idate=idate,
                                                         fdate=fdate)
        else:
            info_result = analizar.rt_get_info_indicator(self.cursor,
                                                         table_n=table_n)
        return info_result

    # No es necesario cambiar si se implemeta importants_table
    def get_nombre_pautas(self):
        '''Retorna lista de nombres de todas las pautas en la DB'''

        query = '''SELECT id, name
                   FROM preguntas_importantes'''
        self.cursor.execute(query)

        nombres_raw = self.cursor.fetchall()
        nombres = ["{}- {}".format(nom[0], nom[1]) for nom in nombres_raw]
        return nombres

    def get_operator_performance(self, operator):
        # query = '''SELECT id, name
        #            FROM preguntas_importantes'''
        #
        # self.keycursor.execute(query)
        # result = self.keycursor.fetchall()
        # print("result", result)

        lista_resumen, lista_total = opperform.get_op_perform(self.cursor,
                                                              analizar,
                                                              operator)

        print("HASTA ACÁ LELGA LA FNCIÓN get_operador_performance de backend")
        return lista_resumen, lista_total


if __name__ == '__main__':
    DBB = DBBrowser()
    print(DBB.complete_resume_table("3"))
    DBB.between_dates_resume("3", "20171230", "20180111")
