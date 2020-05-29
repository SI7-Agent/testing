from logger import MyLogger

import os


class FileChecker:
    @staticmethod
    def check_files():
        path = os.getcwd()
        result = 0

        if not os.path.exists(path + '\\configs\\connection.ini'):
            MyLogger.warning("Cannot find connection.ini file")
            result = -1

        if not os.path.exists(path + '\\configs\\connection_admin.ini'):
            MyLogger.warning("Cannot find connection_admin.ini file")
            result = -2

        if not os.path.exists(path + '\\models\\mdl.caffemodel'):
            MyLogger.warning("Cannot find mdl.caffemodel file")
            result = -3

        if not os.path.exists(path + '\\models\\prt.txt'):
            MyLogger.warning("Cannot find prt.txt file")
            result = -4

        if not os.path.exists(path + '\\models\\emt_mdl.hdf5'):
            MyLogger.warning("Cannot find emt_mdl.hdf5 file")
            result = -5

        if not os.path.exists(path + '\\configs\\camera.ini'):
            MyLogger.warning("Cannot find camera.ini file. You need to launch camera_calibrator.py. Find chess pattern picture and print it")
            result = -6

        if not os.path.exists(path + '\\configs\\coordinates_setup.ini'):
            MyLogger.warning("Cannot find coordinates_setup.ini file")
            result = -7

        return result
