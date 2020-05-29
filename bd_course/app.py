from admin_tools.admin_tool import AdminTool
from concrete_base_helper import BaseChooser
from connect.connect_manager import ConnectManager
from file_checker import FileChecker
from gui.gui import OpencvGui
from logger import MyLogger
from modules.concrete_system import MySystem


class MyApplication:
    @staticmethod
    def start():
        if (error := FileChecker.check_files()) > -1:
            admin_connect = ConnectManager("connection_admin.ini")
            AdminTool(admin_connect).admin_tool().create_database()

            my_connect = ConnectManager()
            my_base_commands = BaseChooser.choose(my_connect)
            try:
                AdminTool(my_connect).admin_tool().create_tables()
                AdminTool(my_connect).admin_tool().create_side_funcs()
                system = MySystem(my_base_commands)
                interface = OpencvGui()
                interface.make_ui(system)
            except AttributeError:
                MyLogger.critical("Unable to create connection/database")
            finally:
                MyLogger.info("App is over")
                exit(error)
        else:
            MyLogger.warning("Unable to find configuration files")
            MyLogger.info("App is over")
            exit(error)
