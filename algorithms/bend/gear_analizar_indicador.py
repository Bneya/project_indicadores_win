import numpy


def rt_get_info_indicator(cursor, table_n, idate=False, fdate=False, op=False):

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
    return get_info_indicator(cursor, query, args_entrada)


def get_info_indicator(cursor, query_entrada, args_entrada):
    table_number = args_entrada[0]
    query_get_n_questions = """SELECT questions, n_questions
                               FROM preguntas_importantes
                               WHERE id = {}""".format(table_number)
    cursor.execute(query_get_n_questions)

    respuesta = cursor.fetchone()
    print("respuesta", respuesta)
    questions_raw, n_questions = respuesta
    questions_list = questions_raw.split(";") + ["Bundle"]

    # print("####query_get_n_questions:", query_get_n_questions)
    # print("questions:", questions_list)
    # print("n_questions:", n_questions)

    txt_select = concatenador_promedios(n_questions)

    # if idate:
    #     query_get_info = """SELECT {0}
    #                         FROM `{1}`
    #                         WHERE fecha >= {2}
    #                         AND fecha <= {3}
    #                         """.format(txt_select, table_number, idate, fdate)
    # else:
    #     query_get_info = """SELECT {0}
    #                         FROM `{1}`""".format(txt_select, table_number)

    query_get_info = query_entrada.format(txt_select, *args_entrada)

    cursor.execute(query_get_info)
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
    rep_text = "SUM(q{0}), COUNT(q{0}), COALESCE(SUM(q{0})/COUNT(q{0}), -1) AS dq{0}"

    lista_aux = []
    for i in range(number):
        lista_aux.append(rep_text.format(i + 1))

    # Ahora añadimos el bundle
    txt_bundle = "SUM(bundle), COUNT(bundle), COALESCE(SUM(bundle)/COUNT(bundle), -1) AS dqbundle"
    lista_aux.append(txt_bundle)

    texto = ", ".join(lista_aux)

    print("texto", texto)

    return texto
