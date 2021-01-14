from admin_tools.admin_tool import AdminTool
from datetime import datetime
from logger import MyLogger
from query_tool.abstract_query_tool import Commands
from string_methods import StringsMethods

import hashlib
import pickle
import psycopg2


class PostgreSQLTool(Commands):
    def push_picture_data(self, metadata, t=None):
        self.connectmanager.cursor.execute("select * from pics;")
        id_pics = len(self.connectmanager.cursor.fetchall())

        self.connectmanager.cursor.execute("select * from pics_data;")
        id_pics_data = len(self.connectmanager.cursor.fetchall()) + 1

        query = '''INSERT INTO pics_data (id_data, id_dependent, label, gender, emote, location) VALUES (%s, %s, %s, %s, %s, %s);'''
        if t == 't':
            query = query.replace('%s', '?')

        self.connectmanager.cursor.execute(query, (
        str(id_pics_data), str(id_pics), metadata["label"], metadata["gender"], metadata["emote"],
        metadata["location"]))

        self.connectmanager.database.commit()
        MyLogger.info("Data insert succeeded")

    def get_picture_props(self, params='*', filters=';'):
        query = 'SELECT ' + params + ' FROM pics_data join pics on pics_data.id_dependent = pics.id_pic ' + filters

        self.connectmanager.cursor.execute(query)
        metadatas = self.connectmanager.cursor.fetchall()

        return metadatas

    def push_picture(self, orig_picture, mime, t=None):
        id_pics = None
        try:
            query = "INSERT INTO pics (id_pic, orig_picture, mime) VALUES (%s, %s, %s);"
            if t == 't':
                query = query.replace('%s', '?')
            self.connectmanager.cursor.execute("select * from pics;")
            id_pics = len(self.connectmanager.cursor.fetchall()) + 1

            self.connectmanager.cursor.execute(query, (str(id_pics), orig_picture, mime))

            self.connectmanager.database.commit()
            MyLogger.info("Pic load succeeded")
        except psycopg2.errors.NotNullViolation:
            id_pics = None
            MyLogger.error("Pics failed. NULL restriction")
        except psycopg2.errors.UniqueViolation:
            id_pics = None
            MyLogger.critical("Pics failed. Unique restriction")
        except:
            id_pics = None
            MyLogger.critical("Pics failed. Undefined error")
        finally:
            return id_pics

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
                                                           (str(self.currentid_event),
                                                            "Обнаруженный человек - " + metadata['name'],
                                                            metadata['first_seen'], datetime.now(),
                                                            metadata['location']))
                        admin_tool.push_log('events', 'Known human recognition succeeded')
                        MyLogger.info("Known human recognition succeeded")
                    else:
                        self.connectmanager.cursor.execute(query,
                                                           (
                                                           str(self.currentid_event), "Обнаружено: " + metadata['name'],
                                                           metadata['first_seen'], datetime.now(),
                                                           metadata['location']))
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
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions',
                                                                 'Emote recognition failed. NULL restriction')
            MyLogger.error("Emote recognition failed. NULL restriction")
        except psycopg2.errors.UniqueViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions',
                                                                 'Emote recognition failed. Unique restriction')
            MyLogger.critical("Emote recognition failed. Unique restriction")
        except:
            AdminTool(self.connectmanager).admin_tool().push_log('recognitions',
                                                                 'Emote recognition failed. Undefined error')
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
            AdminTool(self.connectmanager).admin_tool().push_log('people_id',
                                                                 'Face metadata update failed. NULL restriction')
            MyLogger.error("Face metadata update failed. NULL restriction")


class PostgreSQLUserTool(PostgreSQLTool):
    def get_guy_user(self, user):
        query = 'SELECT * FROM users where users.username = %s'
        self.connectmanager.cursor.execute(query, (user,))
        guy = self.connectmanager.cursor.fetchall()

        if not len(guy):
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Selection failed. No user')
            MyLogger.error("Selection failed. No user")

            raise Exception("User not exists")
        else:
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Selection succeeded')
            MyLogger.info("Selection succeeded")

            return {"firstName": guy[0][0], "lastName": guy[0][1], "username": guy[0][2], "gender": guy[0][3],
                    "password": guy[0][4]}

    def update_data(self, user, data):
        query = 'SELECT * FROM users WHERE users.username = %s;'
        self.connectmanager.cursor.execute(query, (user,))

        if not (len(self.connectmanager.cursor.fetchall()) and len(data)):
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Patch failed. No user or data to patch')
            MyLogger.error("Patch failed. No user or data to patch")

            raise Exception("Bad patch data")

        query = 'UPDATE users SET '

        for i in data:
            query += i + " = %(" + i + ")s, "

        query = query[:-2]
        query += " WHERE users.username = %(destination)s;"
        data['destination'] = user

        if "password" in data:
            data['password'] = hashlib.sha1(data['password'].encode('utf-8')).hexdigest()

        self.connectmanager.cursor.execute(query, data)
        self.connectmanager.database.commit()

        AdminTool(self.connectmanager).admin_tool().push_log('users', 'Patch succeeded')
        MyLogger.error("Patch succeeded")

    def register_guy(self, userdata):
        try:
            nick = userdata.username

            query = 'SELECT username FROM users WHERE users.username = %s;'
            self.connectmanager.cursor.execute(query, (nick,))
            metadatas = self.connectmanager.cursor.fetchall()
            if len(metadatas):
                raise Exception("User exists")
            else:
                query = 'INSERT INTO users (firstName, lastName, username, gender, password) VALUES (%s, %s, %s, %s, %s);'
                password = hashlib.sha1(userdata.password.encode('utf-8')).hexdigest()
                f_name = userdata.first_name
                l_name = userdata.last_name
                gnd = userdata.gender

                self.connectmanager.cursor.execute(query, (f_name, l_name, nick, gnd, password))
                self.connectmanager.database.commit()

                AdminTool(self.connectmanager).admin_tool().push_log('users', 'Registration succeeded')
                MyLogger.info("Registration succeeded")

        except psycopg2.errors.NotNullViolation:
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Registration failed. NULL restriction')
            MyLogger.error("Registration failed. NULL restriction")

    def login_guy(self, login, password):
        code = 200
        try:
            query = 'SELECT username, password FROM users WHERE users.username = %s;'
            self.connectmanager.cursor.execute(query, (login,))
            user = self.connectmanager.cursor.fetchall()
            if not len(user):
                code = 400
            else:
                hash = hashlib.sha1(password.encode('utf-8')).hexdigest()
                if hash != user[0][1]:
                    code = 400

        except:
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Login failed. Undefined')
            MyLogger.error("Login failed. Undefined")
            code = 500

        return code

    def delete_guy(self, user):
        query = 'SELECT * FROM users WHERE users.username = %s;'
        self.connectmanager.cursor.execute(query, (user,))
        if not len(self.connectmanager.cursor.fetchall()):
            AdminTool(self.connectmanager).admin_tool().push_log('users', 'Deletion failed. No user')
            MyLogger.error("Deletion failed. No user")

            raise Exception("User not exist")

        query = 'DELETE FROM users WHERE users.username = %s;'
        self.connectmanager.cursor.execute(query, (user,))
        self.connectmanager.database.commit()

        AdminTool(self.connectmanager).admin_tool().push_log('users', 'Deletion succeeded')
        MyLogger.error("Deletion succeeded")
