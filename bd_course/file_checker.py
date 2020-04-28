import os


class FileChecker:
    @staticmethod
    def check_files():
        path = os.getcwd()
        result = True

        if not os.path.exists(path + '\\configs\\connection.ini'):
            print("Cannot find connection.ini file")
            result = False

        if not os.path.exists(path + '\\models\\mdl.caffemodel'):
            print("Cannot find mdl.caffemodel file")
            result = False

        if not os.path.exists(path + '\\models\\prt.txt'):
            print("Cannot find prt.txt file")
            result = False

        if not os.path.exists(path + '\\models\\emt_mdl.hdf5'):
            print("Cannot find emt_mdl.hdf5 file")
            result = False

        if not os.path.exists(path + '\\configs\\camera.ini'):
            print("Cannot find camera.ini file")
            result = False

        if not os.path.exists(path + '\\configs\\coordinates_setup.ini'):
            print("Cannot find coordinates_setup.ini file")
            result = False

        return result
