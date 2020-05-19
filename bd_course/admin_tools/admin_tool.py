from connect.connect_manager import ConnectManager
from datetime import datetime
from query_tool.abstract_query_tool import Commands


class AdminTool(Commands):
    def admin_tool(self):
        if self.connectmanager.database_type == 'postgresql':
            return AdminPostgreSQL(self.connectmanager)
        elif self.connectmanager.database_type == 'influxdb':
            return AdminInfluxDB(self.connectmanager)


class AdminPostgreSQL(AdminTool):
    def create_database(self):
        side_connect = ConnectManager('connection_admin.ini')
        query = '''DO
                            $do$
                            DECLARE
                              _db TEXT := %s;
                              _user TEXT := %s;
                              _password TEXT := %s;
                            BEGIN
                              CREATE EXTENSION IF NOT EXISTS dblink; -- enable extension 
                              IF EXISTS (SELECT 1 FROM pg_database WHERE datname = _db) THEN
                                RAISE NOTICE 'Database already exists';
                              ELSE
                                PERFORM dblink_connect(%s || _user || ' password=' || _password || ' dbname=' || current_database());
                                PERFORM dblink_exec('CREATE DATABASE ' || _db);
                              END IF;
                            END
                            $do$'''
        host_server = 'port=' + self.connectmanager.connect_info['port'] + ' host=' + self.connectmanager.connect_info['host'] + ' user='
        side_connect.cursor.execute(query, (self.connectmanager.connect_info['dbname'], self.connectmanager.connect_info['user'],
                                            self.connectmanager.connect_info['password'], host_server))
        side_connect.database.commit()
        side_connect.__del__()
        self.create_tables()

    def create_tables(self):
        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS people_id;''')
        self.connectmanager.cursor.execute('''CREATE TABLE people_id
                        (id_people INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        face BYTEA NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS events;''')
        self.connectmanager.cursor.execute('''CREATE TABLE events
                        (id_event INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        first_detection TIMESTAMP NOT NULL,
                        current_detection TIMESTAMP NOT NULL,
                        location TEXT NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS recognitions;''')
        self.connectmanager.cursor.execute('''CREATE TABLE recognitions
                        (id_recognition INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        transaction_time TIMESTAMP NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS logs;''')
        self.connectmanager.cursor.execute('''CREATE TABLE logs
                                (name TEXT NOT NULL,
                                description TEXT NOT NULL,
                                transaction_time TIMESTAMP NOT NULL);''')

        self.connectmanager.database.commit()

    def push_log(self, table_name, exception_name):
        self.connectmanager.cursor.execute('''INSERT INTO logs (name, description, transaction_time) 
                                              VALUES (%s, %s, %s);''',
                                           (table_name, exception_name, datetime.now()))
        self.connectmanager.database.commit()
        self.currentid_log += 1


class AdminInfluxDB(AdminTool):
    def create_database(self):
        pass

    def create_tables(self):
        pass

    def push_log(self, table_name, exception_name):
        pass
