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
        info = ConnectManager.read_connection_config()
        host_server = 'port=' + info['port'] + ' host=' + info['host'] + ' user='
        self.connectmanager.cursor.execute(query, (info['dbname'], info['user'],
                                                   info['password'], host_server))
        self.connectmanager.database.commit()

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

        self.connectmanager.cursor.execute('''CREATE TABLE IF NOT EXISTS users
                                        (firstName TEXT NOT NULL,
                                        lastName TEXT NOT NULL,
                                        username TEXT NOT NULL,
                                        gender TEXT NOT NULL,
                                        password TEXT NOT NULL);''')

        self.connectmanager.cursor.execute('''CREATE TABLE IF NOT EXISTS pics
                                        (id_pic INT PRIMARY KEY NOT NULL,
                                        orig_picture TEXT NOT NULL,
                                        mime TEXT NOT NULL);''')

        self.connectmanager.cursor.execute('''CREATE TABLE IF NOT EXISTS pics_data
                                        (id_data INT PRIMARY KEY NOT NULL,
                                        id_dependent INT NOT NULL,
                                        label TEXT NOT NULL,
                                        gender TEXT NOT NULL,
                                        emote TEXT NOT NULL,
                                        location TEXT NOT NULL);''')

        self.connectmanager.database.commit()

    def create_side_funcs(self):
        self.connectmanager.cursor.execute('''CREATE OR REPLACE FUNCTION get_object_with_intervals(what TEXT, from_time TIMESTAMP, to_time TIMESTAMP)
                                            RETURNS TABLE (id_event INT, 
                                                           name TEXT, 
                                                           first_detection TIMESTAMP, 
                                                           current_detection TIMESTAMP, 
                                                           location TEXT) AS
                                            $$
                                                select * from events where 
                                                        name like $1 and 
                                                        $2 <= first_detection and 
                                                        first_detection <= $3 
                                            $$
                                            language 'sql';''')

        self.connectmanager.cursor.execute('''CREATE OR REPLACE FUNCTION get_emote_with_intervals(what TEXT, from_time TIMESTAMP, to_time TIMESTAMP)
                                                    RETURNS TABLE (id_recognition INT, 
                                                                   name TEXT, 
                                                                   transaction_time TIMESTAMP) AS
                                                    $$
                                                        select * from recognitions where 
                                                                name like $1 and 
                                                                $2 <= transaction_time and 
                                                                transaction_time <= $3 
                                                    $$
                                                    language 'sql';''')

        self.connectmanager.cursor.execute('''CREATE OR REPLACE FUNCTION get_state_with_intervals(what TEXT, from_time TIMESTAMP, to_time TIMESTAMP)
                                                            RETURNS TABLE (name TEXT,
                                                                           description TEXT, 
                                                                           transaction_time TIMESTAMP) AS
                                                            $$
                                                                SELECT * FROM logs WHERE 
                                                                        name LIKE $1 AND 
                                                                        $2 <= transaction_time AND 
                                                                        transaction_time <= $3 
                                                            $$
                                                            LANGUAGE 'sql';''')

        self.connectmanager.cursor.execute('''CREATE OR REPLACE FUNCTION get_groups_objects()
                                                            RETURNS TABLE (time_to TIMESTAMP, name TEXT) AS
                                                            $$
                                                                SELECT to_timestamp(EXTRACT(epoch FROM now()) - 
                                                                    FLOOR(((EXTRACT(epoch FROM now()) - 
                                                                            EXTRACT(epoch FROM current_detection)) / 3600)) 
                                                                                * 3600)::timestamp without time zone AS current_detection, "name"
                                                                FROM events
                                                                GROUP BY 
                                                                    FLOOR(((EXTRACT(epoch FROM now()) - 
                                                                            EXTRACT(epoch FROM current_detection)) / 3600)) * 3600, "name"
                                                            $$
                                                            LANGUAGE "sql";''')
        self.connectmanager.database.commit()

    def push_log(self, table_name, exception_name):
        self.connectmanager.cursor.execute('''INSERT INTO logs (name, description, transaction_time) 
                                              VALUES (%s, %s, %s);''',
                                           (table_name, exception_name, datetime.now()))
        self.connectmanager.database.commit()


class AdminInfluxDB(AdminTool):
    def create_database(self):
        pass

    def create_tables(self):
        pass

    def create_side_funcs(self):
        pass

    def push_log(self, table_name, exception_name):
        pass
