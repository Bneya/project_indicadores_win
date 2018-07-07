lista_args = ["primero", "segundo", "tercero", "cuarto", "decimo"]


txt = "Probando {0}, {1}, {4}".format(*lista_args)
print("txt: ", txt)
