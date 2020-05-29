from __future__ import print_function
from logger import MyLogger

import cv2
import numpy as np
import os
import pickle


class Calibrator:
    def calibrate_camera(self):
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        objp = np.zeros((9 * 6, 3), np.float32)
        objp[:, :2] = np.mgrid[0:9, 0:6].T.reshape(-1, 2)

        objpoints = []
        imgpoints = []

        cap = cv2.VideoCapture(0)

        while (True):
            ret, frame = cap.read()

            img = frame
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            ret, corners = cv2.findChessboardCorners(gray, (9, 6), None)

            if ret:
                objpoints.append(objp)

                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)

                img = cv2.drawChessboardCorners(img, (9, 6), corners2, ret)
                chess = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
                cv2.imshow('chess', chess)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        сap.release()
        cv2.destroyAllWindows()
        MyLogger.info("Run calibrateCamera:")
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

        np.save('mtx.npy', mtx)
        np.save('dist.npy', dist)
        MyLogger.info("mtx.npy and dist.npy saved")
        self.save_calibr((ret, mtx, dist, rvecs, tvecs))

    @staticmethod
    def save_calibr(data):
        if os.path.exists(os.getcwd() + '\\configs\\camera.ini'):
            os.rename(os.getcwd() + '\\configs\\camera.ini', os.getcwd() + '\\configs\\camera.ini.bak')
            MyLogger.info("\\configs\\camera.ini backed up")
        with open(os.getcwd() + '\\configs\\camera.ini', 'wb') as f:
            pickle.dump(data, f)
        MyLogger.info("\\configs\\camera.ini saved")
