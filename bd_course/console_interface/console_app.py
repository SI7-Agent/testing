from admin_tools.admin_tool import AdminTool
from concrete_base_helper import BaseChooser
from connect.connect_manager import ConnectManager
from console_interface.menu import Menu
from file_checker import FileChecker
from logger import MyLogger
from modules.concrete_system import MySystem

import cv2
import os
import shutil


class ConsoleApplication:
    @staticmethod
    def start():
        if (error := FileChecker.check_files()) > -1:
            admin_connect = ConnectManager("connection_admin.ini")
            AdminTool(admin_connect).admin_tool().create_database()

            my_connect = ConnectManager()
            my_base_commands = BaseChooser.choose(my_connect)
            error = -1
            try:
                AdminTool(my_connect).admin_tool().create_tables()
                system = MySystem(my_base_commands)
                menu_print = Menu()
                while True:
                    menu_print.print_main_menu()
                    if (k := input("Your choice: ")) == "1":
                        error = 0
                        break
                    elif k == "2":
                        while True:
                            menu_print.print_sub_menu_admin()
                            if (k2 := input("Your choice: ")) == "1":
                                query = input("Your modify query: ")
                                if query.lower().startswith("alter table"):
                                    try:
                                        my_connect.cursor.execute(query + ';')
                                        my_connect.database.commit()
                                    except:
                                        MyLogger.error("Query failed")
                                        print("Query failed")
                                else:
                                    print("Query tries to do something else")
                            elif k2 == "2":
                                query = input("Your select query: ")
                                if query.lower().startswith("select"):
                                    try:
                                        my_connect.cursor.execute(query + ';')
                                        data = my_connect.cursor.fetchall()
                                        for i in data:
                                            print(i)
                                    except:
                                        MyLogger.error("Query failed")
                                        print("Query failed")
                                else:
                                    print("Query tries to do something else")
                            elif k2 == "3":
                                AdminTool(my_connect).admin_tool().create_tables()
                            elif k2 == "4":
                                path = input("Destination of your config: ")
                                if not os.path.exists(path):
                                    replace_name = path[path.rfind("/")-1:]
                                    replace_path = os.getcwd() + "\\configs\\" + replace_name
                                    if os.path.exists(path):
                                        os.rename(os.getcwd() + '\\configs\\' + replace_name, os.getcwd() + '\\configs\\' + replace_name + '.bak')
                                    shutil.copyfile(path, replace_path)
                                    system.refresh_configs()
                                else:
                                    print("Can't find file")
                            elif k2 == "5":
                                break
                            else:
                                print("No such option")
                    elif k == "3":
                        cam = cv2.VideoCapture(0)
                        while True:
                            menu_print.print_sub_menu_check()
                            if (k3 := input("Your choice: ")) == "1":
                                ret, frame = cam.read()
                                gnd = system.find_gender(frame)
                                print("Found male") if not gnd else print("Found female")
                            elif k3 == "2":
                                ret, frame = cam.read()
                                emt = system.find_emote(frame)
                                print("Find ", system.EMOTES[emt])
                            elif k3 == "3":
                                ret, frame = cam.read()
                                pep = system.find_persons(frame)
                                for i in pep:
                                    print("Face found at", (i[0], i[1]), (i[2], i[3]))
                            elif k3 == "4":
                                ret, frame = cam.read()
                                obj = system.find_objects(frame)
                                for i in obj:
                                    print("Something found at", (i[1], i[2]), (i[3], i[4]))
                            elif k3 == "5":
                                cam.release()
                                break
                            else:
                                print("No such option")
                    else:
                        print("No such option")
            except AttributeError:
                MyLogger.critical("Unable to create connection/database")
            finally:
                if not error:
                    MyLogger.info("Successfully closed")
                    exit(error)
        else:
            MyLogger.warning("Unable to find configuration files")
            MyLogger.info("App is over")
            exit(error)