from datetime import datetime, timedelta
from query_tool.abstract_query_tool import Commands


class AdminTool(Commands):
    def admin_tool(self):
        if self.connectmanager.database_type == 'postgresql':
            return AdminPostgreSQL(self.connectmanager)
        elif self.connectmanager.database_type == 'influxdb':
            return AdminInfluxDB(self.connectmanager)


class AdminPostgreSQL(AdminTool):
    def create_tables(self):
        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS people_id''')
        self.connectmanager.cursor.execute('''CREATE TABLE people_id
                        (id_people INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        face BYTEA NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS events''')
        self.connectmanager.cursor.execute('''CREATE TABLE events
                        (id_event INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        first_detection TIMESTAMP NOT NULL,
                        current_detection TIMESTAMP NOT NULL,
                        location TEXT NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS recognitions''')
        self.connectmanager.cursor.execute('''CREATE TABLE recognitions
                        (id_recognition INT PRIMARY KEY NOT NULL,
                        name TEXT NOT NULL,
                        transaction_time TIMESTAMP NOT NULL);''')

        self.connectmanager.cursor.execute('''DROP TABLE IF EXISTS logs''')
        self.connectmanager.cursor.execute('''CREATE TABLE logs
                                (name TEXT NOT NULL,
                                description TEXT NOT NULL,
                                transaction_time TIMESTAMP NOT NULL);''')

        self.connectmanager.database.commit()

    def push_log(self, table_name, exception_name):
        self.connectmanager.cursor.execute('''INSERT INTO logs (name, description, transaction_time) 
                                              VALUES (%s, %s, %s)''',
                                           (table_name, exception_name, datetime.now()))
        self.connectmanager.database.commit()
        self.currentid_log += 1


class AdminInfluxDB(AdminTool):
    def create_tables(self):
        pass

    def push_log(self):
        pass
