from admin_tools.admin_tool import AdminTool
from concrete_base_helper import BaseChooser
from connect.connect_manager import ConnectManager
from file_checker import FileChecker
from gui.gui import OpencvGui
from robot import Robot


class MyApplication:
    @staticmethod
    def start():
        if FileChecker.check_files():
            my_connect = ConnectManager()
            my_base_commands = BaseChooser.choose(my_connect)
            try:
                AdminTool(my_connect).admin_tool().create_database()
                system = Robot(my_base_commands)
                interface = OpencvGui()
                interface.make_ui(system)
            except AttributeError:
                print("Unable to create connection/database\n")
        else:
            print("Unable to find configuration files\n")
