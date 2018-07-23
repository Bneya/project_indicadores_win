import sys
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from backend_math import DBBrowser
import pymysql as sql
import algorithms.fend.face_listview as facelw


MAINSCREEN = uic.loadUiType("ui/main_window.ui")
CUSTOMITEM = uic.loadUiType("ui/custom_listitem.ui")
POPUP = uic.loadUiType("ui/pop_up.ui")


class CustomItem(*CUSTOMITEM):
    '''Clase que maneja el custoitem de listview tab1'''

    def __init__(self, parent=None):
        super().__init__()
        super(CustomItem, self).__init__(parent)
        self.setupUi(self)

    def set_values(self, values):
        name, aproved, total, perc = values
        self.lb_name.setText(name)
        self.lb_aproved.setText(str(aproved))
        self.lb_reproved.setText(str(total - aproved))
        self.lb_total.setText(str(total))
        self.lb_perc.setText(str(perc))

        self.pbar_perc.setMaximum(total)
        self.pbar_perc.setValue(aproved)

        self.pbar_perc.setFormat('%.02f%%' % (perc * 100))


class PopupWindow(*POPUP):

    def __init__(self, texto):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Error")
        self.lb_popup.setText(texto)


class MainWindow(*MAINSCREEN):

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Indicadores")

        # ------------------------------------------
        # -- Iniciar todo --
        # ------------------------------------------

        # -- Iniciar variables --
        self.popup = None
        self.engine = DBBrowser()  # eSTA LINEA HAY QUE SACARLA LUEGO
        self.info_tab_op = None
        self.table_names = None
        self.list_ids = None

        try:
            self.engine = DBBrowser()
        except sql.err.OperationalError:
            print("nopeeeeeeeeeeeeeeeeeeeeeeee")
            self.hide()
            self.popup = PopupWindow("Dirección ip del servidor inválida")
            self.popup.show()

        else:

            self.nombres_pautas = None

            # -- Llamado a funciones de inicialización --
            self.populate_self()
            self.connect_butons()
            # ------------------------------------------

    # -----------------------------------------------
    # -- Funciones de inicialización --
    # -----------------------------------------------

    def populate_self(self):
        '''Rellena las interfaces con los datos de la DB'''

        self.cb_searchtype.addItems(["Todas las fechas",
                                     "Entre fechas específicas"])

        self.cb_searchtype_op.addItems(["Todas las fechas",
                                        "Entre fechas específicas"])

        self.nombres_pautas = self.engine.get_nombre_pautas()
        self.lista_operadores = self.engine.get_all_operators()
        for name in self.nombres_pautas:
            print(name)

        self.cb_indicadores.addItems(self.nombres_pautas)
        self.cb_operadores.addItems(self.lista_operadores)

    def connect_butons(self):
        '''Conecta los botones a sus funciones respectivas'''

        # Botones de la pestaña <Analizar indicador> ----------------------
        self.bt_search.clicked.connect(self.click_search)
        self.cb_searchtype.currentIndexChanged.connect(self.change_searchtype)

        # Botones de la pestaña <Desempeño de personal> -------------------
        self.bt_search_op_perform.clicked.connect(self.click_get_op_perform)
        self.lw_resultados_op.clicked.connect(self.click_op_list_item)
        searchop = self.cb_searchtype_op
        searchop.currentIndexChanged.connect(self.change_searchtype_op)
    # ------------------------------------------------

    # ------------------------------------------------
    # -- Funciones de los botones --
    # ------------------------------------------------

    def get_results_from_db(self, table_number):
        '''Recupera lo datos de la db, entre fechas o todos'''

        option = self.cb_searchtype.currentText()
        # print(option)

        indicador_text = self.cb_indicadores.currentText()
        # table_number = self.nombres_pautas.index(indicador_text) + 1
        table_number = self.engine.get_table_id_from_name(indicador_text)

        if option == "Todas las fechas":
            resultados = self.engine.get_resume_table(table_n=table_number)

        elif option == "Entre fechas específicas":
            idate = str(self.de_inicio.date().toString("yyyyMMdd"))
            fdate = str(self.de_final.date().toString("yyyyMMdd"))

            resultados = self.engine.get_resume_table(table_n=table_number,
                                                      idate=idate,
                                                      fdate=fdate)

        return resultados, table_number

    def click_search(self):
        '''Click en "Buscar" de tab1. Muestra análisis'''

        # Extraer datos de db
        indicador_text = self.cb_indicadores.currentText()
        print("indicador_text", indicador_text)
        # table_number = self.nombres_pautas.index(indicador_text) + 1
        # table_number = self.engine.get_table_id_from_name(indicador_text)
        table_number = "no actualizado"
        resultados, table_number = self.get_results_from_db(table_number)
        # ---------------------

        # Muestra los resultados en pantalla (Borra los que había antes)
        self.lw_resultados.clear()

        # print("resultados", resultados)
        if resultados[0] == "error":
            self.popup = PopupWindow("Consulta vacía")
            self.popup.show()

        else:
            # Nueva sub función y lógica ------------------------
            importants = self.engine.get_importants_of_table(table_number)
            facelw.show(resultados, self.lw_resultados, CustomItem, importants)

    def click_get_op_perform(self):
        """Llama al motor para mostrar desempeño de un operador"""

        # Limpia lista actual, la lista de dettales y nombre indicador select
        self.lw_resultados_op.clear()
        self.lw_resultados_op_detalles.clear()
        self.lb_indicator_name.setText("Indicador")

        op_cur = self.cb_operadores.currentText().strip("1234567890- ")
        print("op_actualllllll:", op_cur)

        # Pone el nombre en el título
        self.lb_current_operator.setText(op_cur)

        option = self.cb_searchtype_op.currentText()
        if option == "Todas las fechas":
            tuple_resp = self.engine.get_operator_performance(op_cur)
            list_res, list_tot, ids = tuple_resp

        elif option == "Entre fechas específicas":
            idate = str(self.de_inicio_op.date().toString("yyyyMMdd"))
            fdate = str(self.de_final_op.date().toString("yyyyMMdd"))
            print("????????????????idate:", idate, "fdate: ", fdate)
            tuple_resp = self.engine.get_operator_performance(op_cur,
                                                              idate=idate,
                                                              fdate=fdate)
            list_res, list_tot, ids = tuple_resp

        self.info_tab_op = list_tot
        self.table_names = [item[0] for item in list_res]
        self.list_ids = ids
        facelw.show(list_res, self.lw_resultados_op, CustomItem)

    def click_op_list_item(self):
        '''Muestra los detalles de un indicador en <lw_resultados_op_det>'''

        print("hola")
        clicked_row = self.lw_resultados_op.currentRow()
        info_row = self.info_tab_op[clicked_row]
        print("la fila clickeada es:", clicked_row)
        print("La info de esa fila es:", info_row)

        # Terminar esta función
        table_num = self.list_ids[clicked_row]
        to_bold_list = self.engine.get_importants_of_table(table_num)

        self.lb_indicator_name.setText(self.table_names[clicked_row])
        facelw.show_detailed(info_row,
                             self.lw_resultados_op_detalles,
                             CustomItem,
                             to_bold_list)

    # Activa o desactiva búsqueda de fechas en pestaña <Anaizar indicador>
    def change_searchtype(self):
        '''Cambia el tipo de búsqueda entre fechas o desde siempre en tab1'''

        if self.cb_searchtype.currentText() == "Entre fechas específicas":
            self.de_inicio.setEnabled(True)
            self.de_final.setEnabled(True)

        elif self.cb_searchtype.currentText() == "Todas las fechas":
            self.de_inicio.setEnabled(False)
            self.de_final.setEnabled(False)

        else:
            print("Falló la comprobación de texto")

    def change_searchtype_op(self):
        '''Cambia el tipo de búsqueda entre fechas o desde siempre en tab2'''

        if self.cb_searchtype_op.currentText() == "Entre fechas específicas":
            self.de_inicio_op.setEnabled(True)
            self.de_final_op.setEnabled(True)

        elif self.cb_searchtype_op.currentText() == "Todas las fechas":
            self.de_inicio_op.setEnabled(False)
            self.de_final_op.setEnabled(False)

        else:
            print("Falló la comprobación de texto")

    def export_data(self):
        results_raw = self.get_results_from_db()

    # -------------------------------


if __name__ == '__main__':
    def hook(type, value, traceback):
        print(type)
        print(traceback)
    sys.__excepthook__ = hook

    app = QtWidgets.QApplication([])
    mi_app = MainWindow()
    mi_app.show()
    app.exec()
