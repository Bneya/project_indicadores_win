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

        self.cb_searchtype.addItems(["Desde el inicio de los tiempos",
                                     "Entre fechas"])

        self.nombres_pautas = self.engine.get_nombre_pautas()
        for name in self.nombres_pautas:
            print(name)

        self.cb_indicadores.addItems(self.nombres_pautas)

    def connect_butons(self):
        '''Conecta los botones a sus funciones respectivas'''

        self.bt_search.clicked.connect(self.click_search)
        self.cb_searchtype.currentIndexChanged.connect(self.change_searchtype)
    # ------------------------------------------------

    # ------------------------------------------------
    # -- Funciones de los botones --
    # ------------------------------------------------

    def get_results_from_db(self, table_number):
        '''Recupera lo datos de la db, entre fechas o todos'''

        option = self.cb_searchtype.currentText()
        # print(option)

        indicador_text = self.cb_indicadores.currentText()
        table_number = self.nombres_pautas.index(indicador_text) + 1

        if option == "Desde el inicio de los tiempos":
            resultados = self.engine.get_resume_table(table_n=table_number)

        elif option == "Entre fechas":
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
        table_number = self.nombres_pautas.index(indicador_text) + 1
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

    def change_searchtype(self):
        '''Cambia el tipo de búsqueda entre fechas o desde siempre en tab1'''

        if self.cb_searchtype.currentText() == "Entre fechas":
            self.de_inicio.setEnabled(True)
            self.de_final.setEnabled(True)

        elif self.cb_searchtype.currentText() == "Desde el inicio de los tiempos":
            self.de_inicio.setEnabled(False)
            self.de_final.setEnabled(False)

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
