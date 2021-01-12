from query_tool.postgre_tool import PostgreSQLUserTool
from query_tool.influx_tool import InfluxDBTool


class BaseChooser:
    @staticmethod
    def choose(connect_manager):
        if connect_manager.database_type == 'postgresql':
            return PostgreSQLUserTool(connect_manager)
        elif connect_manager.database_type == 'influxdb':
            return InfluxDBTool(connect_manager)
