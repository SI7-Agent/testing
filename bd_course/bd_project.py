from concrete_base_helper import BaseChooser
from connect_manager import ConnectManager
from file_checker import FileChecker
from robot import Robot

if __name__ == '__main__':
    if FileChecker.check_files():
        my_connect = ConnectManager()
        my_base_commands = BaseChooser.choose(my_connect)
        try:
            my_base_commands.create_tables()
            Robot(my_base_commands).main_loop()
        except AttributeError:
            print("Unable to create connection/database\n")
    else:
        print("Unable to find configuration files\n")