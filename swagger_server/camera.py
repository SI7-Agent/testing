from array_methods import ArrayMethods as np1
from calibrate_camera import Calibrator

import cv2
import os
import pickle


class Camera:
    def __init__(self):
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = self.read_camera_config()
        obj, img = self.read_world_config()
        self.y_const = obj[0][1]
        ret, self.rvec, self.tvec = cv2.solvePnP(obj, img, self.mtx, self.dist)
        self.rmtx, self.jac = cv2.Rodrigues(self.rvec)

    @staticmethod
    def read_camera_config():
        with open(os.getcwd() + '/configs/camera.ini', 'rb') as file:
            data = pickle.load(file)

        return data

    @staticmethod
    def read_world_config():
        img_corn = np1.array([[0., 0.], [0., 150.], [150., 0.], [150., 150.]])

        with open(os.getcwd() + '/configs/coordinates_setup.ini', 'r') as file:
            coordinates = np1.array(
                [list(map(lambda x: float(x), row.strip().split(' '))) for row in file if row[0] != '#'])

        return coordinates, img_corn

    def calc_real_coordinates(self, x, z):
        left_matrix = np1.dot(np1.dot(np1.inv(self.rmtx), np1.inv(self.mtx)),
                              np1.array([float(x), 1., float(z)]).transpose())
        right_matrix = np1.dot(np1.inv(self.rmtx), self.tvec)
        s = (self.y_const + right_matrix[1][0]) / left_matrix[1]
        coords = np1.dot(np1.inv(self.rmtx),
                         (s * np1.dot(np1.inv(self.mtx),
                                      np1.array([float(x), 1., float(z)]).transpose()).reshape(3, 1) - self.tvec))

        return coords

    def refresh(self):
        self.read_world_config()

    @staticmethod
    def calibrate():
        Calibrator().calibrate_camera()
