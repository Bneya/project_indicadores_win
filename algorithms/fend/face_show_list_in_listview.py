from PyQt5 import QtWidgets


def show(result_list, listview, listitem):
    '''Toma una <result_list>, tansforma cada uno a un <listitem> y
    lo añade a un <listview>. No retorna nada'''
    for resultado in result_list:
        print("resultado", resultado)
        item = QtWidgets.QListWidgetItem(listview)
        listview.addItem(item)
        custom_item = listitem()
        custom_item.set_values(resultado)

        # Si es importante, lo pone en negrita
        # importantes = self.engine.get_importants_of_table(table_number)

        # print("importantes", importantes)
        # index_pregunta = str(result_list.index(resultado) + 1)
        # print("index pregunta", index_pregunta)
        #
        # # Pone en negrita la fila si es parte del bundle
        # if index_pregunta in importantes or importantes == ["0"]:
        #     bold_font = QtGui.QFont()
        #     bold_font.setBold(True)
        #     custom_item.lb_name.setFont(bold_font)

        item.setSizeHint(custom_item.sizeHint())
        listview.setItemWidget(item, custom_item)
