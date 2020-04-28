import psycopg2


class Connection:
    @staticmethod
    def create_postgresql_connection(connect_info):
        dbname = connect_info['dbname']
        user = connect_info['user']
        password = connect_info['password']
        host = connect_info['host']
        port = connect_info['port']

        database = psycopg2.connect(dbname=dbname, user=user,
                                    password=password, host=host, port=port)
        cursor = database.cursor()

        return database, cursor

    @staticmethod
    def create_influxdb_connection(connect_info):
        pass
