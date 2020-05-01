from query_tool.abstract_query_tool import Commands


class AdminTool(Commands):
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
