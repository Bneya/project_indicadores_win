import sql_management as sqlmg
import numpy


def get_indicator_all_dates(cursor, table_number):
    query_get_n_questions = """SELECT questions, n_questions
                               FROM preguntas_importantes
                               WHERE id = {}""".format(table_number)
    cursor.execute(query_get_n_questions)

    respuesta = cursor.fetchone()
    print("respuesta", respuesta)
    questions_raw, n_questions = respuesta
    questions_list = questions_raw.split(";") + ["Bundle"]

    print("####query_get_n_questions:", query_get_n_questions)
    print("questions:", questions_list)
    print("n_questions:", n_questions)

    txt_select = concatenador_promedios(n_questions)

    query_get_info = """SELECT {0}
                        FROM `{1}`""".format(txt_select, table_number)

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





# concatenador_promedios(3)
