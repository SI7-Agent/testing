class Menu:
    def __init__(self):
        print("Welcome to console version of Robot Mind System")
        print("Choose an option")

    @staticmethod
    def print_main_menu():
        print("1. Quit App")
        print("2. Admin func")
        print("3. Check func")

    @staticmethod
    def print_sub_menu_admin():
        print("2.1. Modify tables (SQL)")
        print("2.2. Get values (SQL)")
        print("2.3. Clear tables")
        print("2.4. Insert config")
        print("2.5. Up")

    @staticmethod
    def print_sub_menu_check():
        print("3.1. Predict gender")
        print("3.2. Predict emote")
        print("3.3. Predict human")
        print("3.4. Predict object")
        print("3.5. Up")

    @staticmethod
    def print_sub_menu_source():
        print("1. Via camera")
        print("2. Via vk")
        print("3. Up")
