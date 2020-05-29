from admin_tools.admin_tool import AdminTool
from datetime import datetime
from logger import MyLogger
from query_tool.abstract_query_tool import Commands
from string_methods import StringsMethods

import pickle
import psycopg2


class PostgreSQLTool(Commands):
    def push_face(self, face_metadata):
        try:
            self.currentid_human += 1
            data_to_add = pickle.dumps(face_metadata)

            self.connectmanager.cursor.execute("INSERT INTO people_id (id_people, name, face) VALUES (%s, %s, %s);",
                                               (str(self.currentid_human), face_metadata['name'], data_to_add))

            self.connectmanager.database.commit()
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People succeeded')
            MyLogger.info("People succeeded")
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People failed. NULL restriction')
            MyLogger.error("People failed. NULL restriction")
        except psycopg2.errors.UniqueViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People failed. Unique restriction')
            MyLogger.critical("People failed. Unique restriction")
        except:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'People failed. Undefined error')
            MyLogger.critical("People failed. Undefined error")

    def push_event(self, metadata):
        admin_tool = AdminTool(self.connectmanager).admin_tool()
        try:
            query = '''INSERT INTO events (id_event, name, first_detection, current_detection, location) VALUES (%s, %s, %s, %s, %s);'''

            try:
                self.currentid_event += 1
                if len(metadata) > 1:
                    if metadata['emote'] is not None:
                        self.connectmanager.cursor.execute(query,
                                                           (str(self.currentid_event), "Обнаруженный человек - " + metadata['name'],
                                                            metadata['first_seen'], datetime.now(), metadata['location']))
                        admin_tool.push_log('events', 'Known human recognition succeeded')
                        MyLogger.info("Known human recognition succeeded")
                    else:
                        self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружено: " + metadata['name'],
                                                        metadata['first_seen'], datetime.now(), metadata['location']))
                        admin_tool.push_log('events', 'Object recognition succeeded')
                        MyLogger.info("Object recognition succeeded")
                else:
                    self.connectmanager.cursor.execute(query,
                                                       (str(self.currentid_event), "Обнаружен человек",
                                                        datetime.now(), datetime.now(), metadata['location']))
                    admin_tool.push_log('events', 'Human recognition succeeded')
                    MyLogger.info("Human recognition succeeded")

                self.connectmanager.database.commit()
            except psycopg2.errors.InFailedSqlTransaction:
                admin_tool.push_log('recognitions', 'Transaction failed')
                MyLogger.critical("Transaction failed")
        except psycopg2.errors.NotNullViolation:
            admin_tool.push_log('events', 'Event failed. NULL restriction')
            MyLogger.error("Event failed. NULL restriction")
        except psycopg2.errors.UniqueViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('events', 'Event failed. Unique restriction')
            MyLogger.critical("Events failed. Unique restriction")
        except:
            AdminTool(self.connectmanager).admin_tool().push_log('events', 'Emote recognition failed. Undefined error')
            MyLogger.critical("Events failed. Undefined error")

    def push_recognition(self, metadata):
        try:
            self.currentid_recognition += 1
            query = '''INSERT INTO recognitions (id_recognition, name, transaction_time) VALUES (%s, %s, %s);'''
            string_data = metadata['name'] + ' поменял(а) свою эмоцию и стал(а) ' + metadata['emote']

            self.connectmanager.cursor.execute(query, (str(self.currentid_recognition), string_data, datetime.now()))

            self.connectmanager.database.commit()
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition succeeded')
            MyLogger.info("Emote recognition succeeded")
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition failed. NULL restriction')
            MyLogger.error("Emote recognition failed. NULL restriction")
        except psycopg2.errors.UniqueViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition failed. Unique restriction')
            MyLogger.critical("Emote recognition failed. Unique restriction")
        except:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Emote recognition failed. Undefined error')
            MyLogger.critical("Emote recognition failed. Undefined error")

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

    def get_emotes_with_interval(self, interval, *args):
        query = 'SELECT * FROM get_emote_with_intervals(%s, %s, %s)'
        cutter = StringsMethods()
        metadatas = []
        try:
            left = cutter.cut_to(cutter.cut_from(interval, "from "), " to")
            right = cutter.cut_to(cutter.cut_from(interval, "to "))
            intervals = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"), [left, right]))
        except ValueError:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions', 'Error in interval')
            MyLogger.error("Error in interval")
            return metadatas

        try:
            for i in args:
                self.connectmanager.cursor.execute(query, (i, intervals[0], intervals[1]))
                metadata = self.connectmanager.cursor.fetchall()
                metadatas.append(metadata)
        except:
            MyLogger.critical("Unexpected error")
        finally:
            return metadatas if metadatas != [[]] else []

    def get_recognition(self, params='*', filters=''):
        query = 'SELECT ' + params + ' FROM recognitions ' + filters

        self.connectmanager.cursor.execute(query)
        metadatas = self.connectmanager.cursor.fetchall()

        return metadatas

    def get_object_with_interval(self, what_we_need, interval):
        query = 'SELECT * FROM get_object_with_intervals(%s, %s, %s)'
        cutter = StringsMethods()
        metadatas = []
        try:
            left = cutter.cut_to(cutter.cut_from(interval, "from "), " to")
            right = cutter.cut_to(cutter.cut_from(interval, "to "))
            intervals = list(map(lambda x: datetime.strptime(x, "%Y-%m-%d %H:%M:%S.%f"), [left, right]))
        except ValueError:
            AdminTool(self.connectmanager).admin_tool().push_log('events', 'Error in interval')
            MyLogger.error("Error in interval")
            return metadatas

        try:
            self.connectmanager.cursor.execute(query, (what_we_need, intervals[0], intervals[1]))
            metadatas = self.connectmanager.cursor.fetchall()
        except:
            AdminTool(self.connectmanager).admin_tool().push_log('events', 'Unexpected error')
            MyLogger.critical("Unexpected error")
        finally:
            AdminTool(self.connectmanager).admin_tool().push_log('events', 'Select with intervals was made')
            MyLogger.info("Select with intervals was made")
            return metadatas

    def update_metadata(self, new_metadata):
        try:
            data_to_upd = pickle.dumps(new_metadata)

            name = "'" + new_metadata['name'] + "'"
            param = 'id_people'
            filter = 'where name = ' + name
            ids = self.get_guy(param, filter)[0][0]

            self.connectmanager.cursor.execute("UPDATE people_id SET face = %s where id_people = %s",
                                               (data_to_upd, str(ids)))

            self.connectmanager.database.commit()
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'Face metadata update succeeded')
            MyLogger.info("Face metadata update succeeded")
        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('people_id', 'Face metadata update failed. NULL restriction')
            MyLogger.error("Face metadata update failed. NULL restriction")
