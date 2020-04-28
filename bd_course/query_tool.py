from abstract_query_tool import Commands
from datetime import datetime, timedelta

import pickle
import psycopg2


class BaseCommandsPostgreSQL(Commands):
    def __init__(self, cm):
        self.connectmanager = cm

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
                                (id_log INT PRIMARY KEY NOT NULL,
                                name TEXT NOT NULL,
                                description TEXT NOT NULL,
                                transaction_time TIMESTAMP NOT NULL);''')

        self.connectmanager.database.commit()

    def push_face(self, face_metadata):
        try:
            data_to_add = pickle.dumps(face_metadata)

            self.connectmanager.cursor.execute("INSERT INTO people_id (id_people, name, face) VALUES (%s, %s, %s)",
                                               (str(self.currentid_human), face_metadata['name'], data_to_add))

            self.connectmanager.database.commit()
            self.currentid_human += 1
            self.push_log('people_id', 'People succeeded')
        except psycopg2.errors.NotNullViolation:
            self.push_log('people_id', 'People failed. NULL restriction')

    def get_guy(self, params='*', filters=''):
        encodings = []
        query = 'SELECT ' + params + ' FROM people_id ' + filters

        self.connectmanager.cursor.execute(query)
        metadatas = self.connectmanager.cursor.fetchall()
        try:
            for i in range(len(metadatas)):
                metadatas[i] = pickle.loads(metadatas[i][0])
                encodings.append(metadatas[i]['face_encoding'])

            return encodings, metadatas
        except:
            return metadatas

    def push_event(self, metadata):
        try:
            query = '''INSERT INTO events (id_event, name, first_detection, current_detection, location) VALUES (%s, %s, %s, %s, %s)'''

            try:
                if len(metadata) > 1:
                    if metadata['emote'] is not None:
                        self.connectmanager.cursor.execute(query,
                                                           (str(self.currentid_event), "Обнаруженный человек - " + metadata['name'],
                                                            metadata['first_seen'], datetime.now(), metadata['location']))
                        self.push_log('events', 'Known human recognition succeeded')
                    else:
                        self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружено: " + metadata['name'],
                                                        metadata['first_seen'], datetime.now(), metadata['location']))
                        self.push_log('events', 'Object recognition succeeded')
                else:
                    self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружен человек",
                                                        datetime.now(), datetime.now(), metadata['location']))
                    self.push_log('events', 'Human recognition succeeded')

                self.connectmanager.database.commit()
                self.currentid_event += 1
            except psycopg2.errors.InFailedSqlTransaction:
                self.push_log('recognitions', 'Transaction failed')
        except psycopg2.errors.NotNullViolation:
            self.push_log('events', 'Event failed. NULL restriction')

    def push_recognition(self, metadata):
        try:
            query = '''INSERT INTO recognitions (id_recognition, name, transaction_time) VALUES (%s, %s, %s)'''
            string_data = metadata['name'] + ' поменял(а) свою эмоцию и стал(а) ' + metadata['emote']

            self.connectmanager.cursor.execute(query, (str(self.currentid_recognition), string_data, datetime.now()))

            self.connectmanager.database.commit()
            self.currentid_recognition += 1
            self.push_log('recognitions', 'Emote recognition succeeded')
        except psycopg2.errors.NotNullViolation:
            self.push_log('recognitions', 'Emote recognition failed. NULL restriction')

    def get_recognition(self, params='*', filters=''):
        query = 'SELECT ' + params + ' FROM recognitions ' + filters

        self.connectmanager.cursor.execute(query)
        metadatas = self.connectmanager.cursor.fetchall()

        return metadatas

    def update_metadata(self, new_metadata):
        try:
            data_to_upd = pickle.dumps(new_metadata)

            name = "'" + new_metadata['name'] + "'"
            param = 'id_people'
            filter = 'where name = ' + name
            ids = self.get_guy(param, filter)[0][0]

            self.connectmanager.cursor.execute("UPDATE people_id SET face = %s where id_people = %s", (data_to_upd, str(ids)))

            self.connectmanager.database.commit()
            self.push_log('people_id', 'Face metadata update succeeded')
        except psycopg2.errors.NotNullViolation:
            self.push_log('people_id', 'Face metadata update failed. NULL restriction')

    def push_log(self, table_name, exception_name):
        self.connectmanager.cursor.execute('''INSERT INTO logs (id_log, name, description, transaction_time) 
                                              VALUES (%s, %s, %s, %s)''',
                                           (str(self.currentid_log), table_name, exception_name, datetime.now()))
        self.connectmanager.database.commit()
        self.currentid_log += 1


class BaseCommandsInfluxDB(Commands):
    def __init__(self, cm):
        self.connectmanager = cm

    def create_tables(self):
        pass

    def push_face(self, face_metadata):
        pass

    def get_guy(self, params='*', filters=''):
        pass

    def push_event(self, metadata):
        pass

    def push_recognition(self, metadata):
        pass

    def get_recognition(self, params='*', filters=''):
        pass

    def update_metadata(self, new_metadata):
        pass

    def push_log(self, table_name, exception_name):
        pass
