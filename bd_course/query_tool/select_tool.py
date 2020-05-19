from query_tool.abstract_query_tool import Commands

import pickle


class SelectPostgreSQL(Commands):
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

    def get_recognition(self, params='*', filters=''):
        query = 'SELECT ' + params + ' FROM recognitions ' + filters

        self.connectmanager.cursor.execute(query)
        metadatas = self.connectmanager.cursor.fetchall()

        return metadatas


class SelectInfluxDB(Commands):
    def get_guy(self, params='*', filters=''):
        pass

    def get_recognition(self, params='*', filters=''):
        pass
