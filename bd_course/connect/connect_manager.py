from connect.create_connection import Connection

import os
import psycopg2


class ConnectManager:
    database_type = None
    database = None
    cursor = None
    connect_info = None

    def __init__(self, config_name='connection.ini'):
        try:
            self.connect_info = self.read_connection_config(config_name)
            self.database_type = self.connect_info['database']
            if self.database_type == 'postgresql':
                self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)
            elif self.database_type == 'influxdb':
                self.database, self.cursor = Connection.create_influxdb_connection(self.connect_info)

            if not (self.database and self.cursor):
                raise psycopg2.SqlclientUnableToEstablishSqlconnection
        except:
            print('Try to reconnect...\n')
            for i in range(1, 4):
                try:
                    if self.database_type == 'postgresql':
                        self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)
                    elif self.database_type == 'influxdb':
                        self.database, self.cursor = Connection.create_influxdb_connection(self.connect_info)
                except:
                    print('Can\'t connect\n')
        finally:
            if not (self.database and self.cursor):
                raise psycopg2.ConnectionFailure
            else:
                print('Connect established\n')

    def reconnect(self, new_connect_info):
        try:
            self.close_connection()
            self.connect_info = new_connect_info

            self.database_type = self.connect_info['database']
            if self.database_type == 'postgresql':
                self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)
            elif self.database_type == 'influxdb':
                self.database, self.cursor = Connection.create_influxdb_connection(self.connect_info)
        except:
            print("Can\'t close current database connection")
            for i in range(1, 4):
                try:
                    self.close_connection()
                    self.connect_info = new_connect_info
                    if self.database_type == 'postgresql':
                        self.database, self.cursor = Connection.create_postgresql_connection(self.connect_info)
                    elif self.database_type == 'influxdb':
                        self.database, self.cursor = Connection.create_influxdb_connection(self.connect_info)
                except:
                    print('Can\'t reconnect\n')
        finally:
            if not (self.database and self.cursor):
                raise psycopg2.ConnectionFailure
            else:
                print('Successful reconnect\n')

    @staticmethod
    def read_connection_config(config_name='connection.ini'):
        read_data = {}
        connect = open(os.getcwd() + "\\configs\\" + config_name, 'r')
        try:
            for i in connect:
                meta = i.split('=')
                read_data[meta[0][:-1]] = meta[-1][1:-1]
        except:
            print('Can\'t read config file\n')
        finally:
            connect.close()
            return read_data

    def close_connection(self):
        try:
            if self.database_type == 'postgresql':
                self.database.close()
            elif self.database_type == 'influxdb':
                pass
        except:
            print('Can\'t close current connection...\n')
        finally:
            if not self.database:
                print('Connection is closed\n')

    def __del__(self):
        self.close_connection()
