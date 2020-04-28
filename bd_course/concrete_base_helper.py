from query_tool import BaseCommandsPostgreSQL
from query_tool import BaseCommandsInfluxDB


class BaseChooser:
    @staticmethod
    def choose(connect_manager):
        if connect_manager.database_type == 'postgresql':
            return BaseCommandsPostgreSQL(connect_manager)
        elif connect_manager.database_type == 'postgresql':
            return BaseCommandsInfluxDB(connect_manager)
