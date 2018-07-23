import numpy
import pymysql as sql


def rt_get_info_indicator(cursor, table_n, idate=False, fdate=False, op=False):
    """Router que centraliza la llamada a buscar en un indicador"""

    # Query base para obtener un resumen de los datos
    query_base = "SELECT {0} FROM `{1}` WHERE 1 "
    query = query_base

    # Ahora añade FILTROS a la consulta si es necesario
    if idate:
        extra_date = "AND fecha >= {2} AND fecha <= {3} "
        query += extra_date

    if op:
        extra_op = "AND (operador = '{4}' OR operador2 = '{4}')"
        query += extra_op

    args_entrada = [table_n, idate, fdate, op]
    print("#######query que se va a ejecutar:", query)
    return get_info_indicator(cursor, query, args_entrada)


def get_info_indicator(cursor, query_entrada, args_entrada):
    table_number = args_entrada[0]
    query_get_n_questions = """SELECT questions, n_questions
                               FROM preguntas_importantes
                               WHERE id = {}""".format(table_number)
    cursor.execute(query_get_n_questions)

    respuesta = cursor.fetchone()
    print("respuesta", respuesta)
    print("//////tipo de cursor:", type(cursor))

    # Comprueba si estoy usando un cursor tupla o un DictCursor
    if isinstance(cursor, sql.cursors.DictCursor):
        # print("···········RESPUESTA CON KEYCURSOR:", respuesta)
        questions_raw = respuesta["questions"]
        n_questions = respuesta["n_questions"]
        questions_list = questions_raw.split(";") + ["Bundle"]
        print("entré al if de keycursor")
    elif isinstance(cursor, sql.cursors.Cursor):
        questions_raw, n_questions = respuesta
        questions_list = questions_raw.split(";") + ["Bundle"]
        print("entré al if de cursor normal")

    # print("questions", questions_list)
    # print("n_questions", n_questions)

    txt_select = concatenador_promedios(n_questions)

    query_get_info = query_entrada.format(txt_select, *args_entrada)

    cursor.execute(query_get_info)

    # Comprueba si estoy usando un cursor tupla o un DictCursor
    if isinstance(cursor, sql.cursors.DictCursor):
        key_response = list(cursor.fetchall()[0].values())
        print("KEY_RESPONSE:", key_response)
        info = numpy.array(key_response)
    elif isinstance(cursor, sql.cursors.Cursor):
        info = numpy.array(cursor.fetchall()[0])

    print("info: ", info)
    print("numpy parsed:")

    parsed_info = numpy.split(info, n_questions + 1)

    tuple_list = []
    for question, numbers in zip(questions_list, parsed_info):
        aux_tuple = tuple(numbers)
        sub_tuple = (question, *aux_tuple)
        tuple_list.append(sub_tuple)
        print(sub_tuple)

    if tuple_list[0][1] is None:
        tuple_list = ("error", "consulta vacía")

    return tuple_list


def concatenador_promedios(number):
    rep_text = "SUM(q{0}) AS sq{0}, COUNT(q{0}) cq{0}, COALESCE(SUM(q{0})/COUNT(q{0}), -1) AS dq{0}"

    lista_aux = []
    for i in range(number):
        lista_aux.append(rep_text.format(i + 1))

    # Ahora añadimos el bundle
    txt_bundle = "SUM(bundle) AS sqbundle, COUNT(bundle) AS dqbundle, COALESCE(SUM(bundle)/COUNT(bundle), -1) AS dqbundle"
    lista_aux.append(txt_bundle)

    texto = ", ".join(lista_aux)

    print("texto", texto)

    return texto
