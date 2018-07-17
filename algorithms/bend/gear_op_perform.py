"""Gear encargado de hacer los cálculos para obtener desempeño de un operador
en todas las pautas existentes"""


def get_op_perform(cursor, gear_analizar, op, idate=False, fdate=False):
    query_get_n_tablas = "SELECT id FROM preguntas_importantes"
    query_get_nombre_tablas = "SELECT name FROM preguntas_importantes"

    cursor.execute(query_get_n_tablas)
    num_of_tables_list = [item[0] for item in cursor.fetchall()]

    cursor.execute(query_get_nombre_tablas)
    lista_nombres = []
    for item in cursor:
        lista_nombres.append(item[0])
    print("---------num_of_tables_list:", num_of_tables_list)
    print("---------lista_nombres", lista_nombres)

    lista_total = []

    # Revisa si le estamos pidiendo entre fechas o todo las fechas
    if idate:
        for num in num_of_tables_list:
            sub_info = gear_analizar.rt_get_info_indicator(cursor,
                                                           table_n=2,
                                                           idate=idate,
                                                           fdate=fdate,
                                                           op=op)
            lista_total.append(sub_info)
    else:
        for num in num_of_tables_list:
            print("ESTOY REVISANDO EL NUMERO", num)
            sub_info = gear_analizar.rt_get_info_indicator(cursor,
                                                           table_n=num,
                                                           op=op)
            lista_total.append(sub_info)

    for row in lista_total:
        print(row)

    info_result = "HOLA"

    # lista1 = [1, 0, 0, 1, 1]

    # lista2 = ["hola" if item == 1 else "chao" for item in lista1]
    # print("LISTAAAAAAAAAAAAAAA2:", lista2)

    lista_resumen = [(name, 0, 0, 0) if values[0] == "error"
                     else (name, *values[-1][1:])
                     for values, name in zip(lista_total, lista_nombres)]

    print("ESTA ES LA LISTA RESUMEN FINAL")
    for item in lista_resumen:
        print(item)

    return lista_resumen, lista_total
