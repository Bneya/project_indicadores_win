from PyQt5 import QtWidgets, QtGui


def show(result_list, listview, listitem, to_bold_list=False):
    '''Toma una <result_list>, tansforma cada uno a un <listitem> y
    lo añade a un <listview>. No retorna nada'''
    for resultado in result_list:
        print("resultado", resultado)
        item = QtWidgets.QListWidgetItem(listview)
        listview.addItem(item)
        custom_item = listitem()
        custom_item.set_values(resultado)

        # Pone filas en negrita si recibe el argumento to_bold_List
        if to_bold_list:
            index_pregunta = str(result_list.index(resultado) + 1)
            if index_pregunta in to_bold_list or to_bold_list == ["0"]:
                bold_font = QtGui.QFont()
                bold_font.setBold(True)
                custom_item.lb_name.setFont(bold_font)

        item.setSizeHint(custom_item.sizeHint())
        listview.setItemWidget(item, custom_item)


# Pobando esta función. No sé cómo acceder al contenido de QListWidgetItem
def make_bold(listview, to_bold_list):
    print("Estas son las filas de listview:")
    for i in range(listview.count()):
        item = listview.item(i)
        print(item)
        print(dir(item))
        if i in to_bold_list:
            bold_font = QtGui.QFont()
            bold_font.setBold(True)
            # item.lb_name.setFont(bold_font)
            item.setFont(bold_font)
