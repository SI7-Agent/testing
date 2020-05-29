from abc import abstractmethod
from camera import Camera
from datetime import datetime, timedelta
from struct_datas import ConstructorObject

import cv2
import face_recognition
import keras.models
import numpy as np
import os


class Robot:
    control_tool = None
    known_face_encodings = None
    known_face_metadata = None
    CLASSES = None
    CLASSES_RU = None
    COLORS = None
    EMOTES = None
    EMOTES_RU = None
    model = None
    net = None
    gender_net = None
    camera = None
    builder = None

    def __init__(self, ctrl):
        self.control_tool = ctrl
        self.known_face_encodings = []
        self.known_face_metadata = []

        self.CLASSES = ["Background", "Aeroplane", "Bicycle", "Bird", "Boat",
                        "Bottle", "Bus", "Car", "Cat", "Chair", "Cow", "Dinning table",
                        "Dog", "Horse", "Motorbike", "Person", "Potted plant", "Sheep",
                        "Sofa", "Train", "Tv monitor"]
        self.CLASSES_RU = ["Фон", "Аэроплан", "Велосипед", "Птица", "Лодка",
                           "Бутылка", "Автобус", "Автомобиль", "Кошка", "Стул",
                           "Корова", "Обеденный стол", "Собака", "Лошадь", "Мотоцикл",
                           "Человек", "Растение в горшке", "Овца", "Диван", "Поезд", "Телеэкран"]
        self.COLORS = np.random.uniform(0, 255, size=(len(self.CLASSES), 3))

        self.EMOTES = ["Angry", "Disgust", "Scared", "Happy", "Sad", "Surprised", "Neutral"]
        self.EMOTES_RU = ["Злой(-ая)", "Чувствующий(-ая) отвращение", "Испуганный(-ая)",
                          "Счастливый(-ая)", "Грустный(-ая)", "Удивленный(-ая)", "Нейтральный(-ая)"]

        self.net = cv2.dnn.readNetFromCaffe(os.getcwd() + '\\models\\prt.txt', os.getcwd() + '\\models\\mdl.caffemodel')
        self.model = keras.models.load_model(os.getcwd() + '\\models\\emt_mdl.hdf5')
        self.gender_net = cv2.dnn.readNetFromCaffe(os.getcwd() + '\\models\\gender.prototxt', os.getcwd() + '\\models\\gender.caffemodel')
        self.camera = Camera()
        self.builder = ConstructorObject()

    def refresh_configs(self):
        self.camera.refresh()

    def refresh_models(self):
        self.net = cv2.dnn.readNetFromCaffe(os.getcwd() + '\\models\\prt.txt', os.getcwd() + '\\models\\mdl.caffemodel')
        self.model = keras.models.load_model(os.getcwd() + '\\models\\emt_mdl.hdf5')
        self.gender_net = cv2.dnn.readNetFromCaffe(os.getcwd() + '\\models\\gender.prototxt', os.getcwd() + '\\models\\gender.caffemodel')

    def register_new_object(self, name, location):
        new_metadata = self.builder.generator(location, type=name)
        self.control_tool.push_event(new_metadata)

    def register_new_face(self, face_encoding, face_image, location, gnd):
        new_metadata = self.builder.generator(location, gnd=gnd, face_en=face_encoding, face_image=face_image)

        self.known_face_metadata.append(new_metadata)
        self.control_tool.push_face(new_metadata)

    def lookup_known_face(self, face_encoding):
        metadata = None
        self.known_face_encodings, self.known_face_metadata = self.control_tool.get_guy(params='face')

        if len(self.known_face_encodings) == 0:
            return metadata

        face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if face_distances[best_match_index] < 0.65:
            metadata = self.known_face_metadata[best_match_index]

            metadata["last_seen"] = datetime.now()
            metadata["seen_frames"] += 1

            if datetime.now() - metadata["first_seen_this_interaction"] > timedelta(minutes=5):
                metadata["first_seen_this_interaction"] = datetime.now()
                metadata["seen_count"] += 1

        return metadata

    @staticmethod
    def get_face_from_image(face_location, small_frame):
        top, right, bottom, left = face_location
        face_image = small_frame[top:bottom, left:right]
        face_image = cv2.resize(face_image, (150, 150))

        return face_image

    @abstractmethod
    def find_gender(self, frame):
        pass

    @abstractmethod
    def find_emote(self, frame):
        pass

    @abstractmethod
    def find_persons(self, frame):
        pass

    @abstractmethod
    def find_objects(self, frame):
        pass
