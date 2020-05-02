from admin_tools.admin_tool import AdminTool
from datetime import datetime, timedelta
from query_tool.abstract_query_tool import Commands

import pickle
import psycopg2


class InsertPostgreSQL(Commands):
    def push_face(self, face_metadata):
        try:
            data_to_add = pickle.dumps(face_metadata)

            self.connectmanager.cursor.execute("INSERT INTO people_id (id_people, name, face) VALUES (%s, %s, %s)",
                                               (str(self.currentid_human), face_metadata['name'], data_to_add))

            self.connectmanager.database.commit()
            self.currentid_human += 1
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People succeeded')
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People failed. NULL restriction')

    def push_event(self, metadata):
        admin_tool = AdminTool(self.connectmanager).admin_tool()
        try:
            query = '''INSERT INTO events (id_event, name, first_detection, current_detection, location) VALUES (%s, %s, %s, %s, %s)'''

            try:
                if len(metadata) > 1:
                    if metadata['emote'] is not None:
                        self.connectmanager.cursor.execute(query,
                                                           (str(self.currentid_event), "Обнаруженный человек - " + metadata['name'],
                                                            metadata['first_seen'], datetime.now(), metadata['location']))
                        admin_tool.push_log('events', 'Known human recognition succeeded')
                    else:
                        self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружено: " + metadata['name'],
                                                        metadata['first_seen'], datetime.now(), metadata['location']))
                        admin_tool.push_log('events', 'Object recognition succeeded')
                else:
                    self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружен человек",
                                                        datetime.now(), datetime.now(), metadata['location']))
                    admin_tool.push_log('events', 'Human recognition succeeded')

                self.connectmanager.database.commit()
                self.currentid_event += 1
            except psycopg2.errors.InFailedSqlTransaction:
                admin_tool.push_log('recognitions', 'Transaction failed')
        except psycopg2.errors.NotNullViolation:
            admin_tool.push_log('events', 'Event failed. NULL restriction')

    def push_recognition(self, metadata):
        try:
            query = '''INSERT INTO recognitions (id_recognition, name, transaction_time) VALUES (%s, %s, %s)'''
            string_data = metadata['name'] + ' поменял(а) свою эмоцию и стал(а) ' + metadata['emote']

            self.connectmanager.cursor.execute(query, (str(self.currentid_recognition), string_data, datetime.now()))

            self.connectmanager.database.commit()
            self.currentid_recognition += 1
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition succeeded')
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition failed. NULL restriction')


class InsertInfluxDB(Commands):
    def push_face(self, face_metadata):
        pass

    def push_event(self, metadata):
        pass

    def push_recognition(self, metadata):
        pass
