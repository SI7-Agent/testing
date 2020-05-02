from query_tool.insert_tool import InsertPostgreSQL
from query_tool.select_tool import SelectPostgreSQL
from query_tool.update_tool import UpdatePostgreSQL

from query_tool.insert_tool import InsertInfluxDB
from query_tool.select_tool import SelectInfluxDB
from query_tool.update_tool import UpdateInfluxDB


class BaseChooser:
    @staticmethod
    def choose(connect_manager):
        if connect_manager.database_type == 'postgresql':
            insert_tool = InsertPostgreSQL(connect_manager)
            select_tool = SelectPostgreSQL(connect_manager)
            update_tool = UpdatePostgreSQL(connect_manager)
            return (insert_tool, select_tool, update_tool)
        elif connect_manager.database_type == 'influxdb':
            insert_tool = InsertInfluxDB(connect_manager)
            select_tool = SelectInfluxDB(connect_manager)
            update_tool = UpdateInfluxDB(connect_manager)
            return (insert_tool, select_tool, update_tool)
