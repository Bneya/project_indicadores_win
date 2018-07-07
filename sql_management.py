import pymysql
import json


class DBManager:

    def __init__(self):
        self.target_ip = None
        self.target_user = None
        self.target_pass = None
        self.target_db = None
        self.load_saved_settings()

    def load_saved_settings(self):
        '''Carga las configs de data/settings.json'''

        save_file = open("data/settings.json")
        config_dict = json.load(save_file)
        # print("config_dict", config_dict)
        self.target_ip = config_dict["target_ip"]
        self.target_user = config_dict["target_user"]
        self.target_pass = config_dict["target_pass"]
        self.target_db = config_dict["target_db"]

        print("cosas dentro: ", self.target_ip, self.target_user, self.target_pass, self.target_db)

    def connect_propio(self):
        ipp, user, pswd = self.target_ip, self.target_user, self.target_pass
        target_db = self.target_db
        # conn0 = pymysql.connect("localhost", "ucirepor_usuario", "usuario", "registro")

        conn2 = pymysql.connect(ipp, user, pswd, target_db)

        return conn2


if __name__ == '__main__':
    DBMANAGER = DBManager()
    conn = DBMANAGER.connect_propio()
    print("COOOOOON:", conn)
