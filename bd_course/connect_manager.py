from create_connection import Connection

import os


class ConnectManager:
    database_type = None
    database = None
    cursor = None
    connect_info = None

    def __init__(self):
        self.connect_info = self.read_connection_config()
        self.database_type = self.connect_info['database']
        if self.database_type == 'postgresql':
            self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)

    def reconnect(self, new_connect_info):
        try:
            self.close_connection()
            self.connect_info = new_connect_info

            self.database_type = self.connect_info['database']
            if self.database_type == 'postgresql':
                self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)
        except:
            print("Cannot close current database connection")

    @staticmethod
    def read_connection_config():
        read_data = {}
        with open(os.getcwd() + "\\configs\\connection.ini", 'r') as connect:
            for i in connect:
                meta = i.split('=')
                read_data[meta[0][:-1]] = meta[-1][1:-1]

        return read_data

    def close_connection(self):
        if self.database_type == 'postgresql':
            self.database.close()

    def __del__(self):
        try:
            self.close_connection()
        except:
            print("Oops...")
