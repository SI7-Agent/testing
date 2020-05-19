from camera import Camera
from datetime import datetime, timedelta
from gui.gui import OpencvGui
from struct_datas import ConstructorObject

import cv2
import face_recognition
import keras.models
import keras.preprocessing.image as preimage
import numpy as np
import os


class Robot:
    control_insert = None
    control_select = None
    control_update = None
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
    builder= None

    def __init__(self, ctrl):
        self.control_insert = ctrl[0]
        self.control_select = ctrl[1]
        self.control_update = ctrl[2]
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
        self.control_insert.push_event(new_metadata)

    def register_new_face(self, face_encoding, face_image, location, gnd):
        new_metadata = self.builder.generator(location, gnd=gnd, face_en=face_encoding, face_image=face_image)

        self.known_face_metadata.append(new_metadata)
        self.control_insert.push_face(new_metadata)

    def lookup_known_face(self, face_encoding):
        metadata = None
        self.known_face_encodings, self.known_face_metadata = self.control_select.get_guy(params='face')

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

    def find_gender(self, frame):
        blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
        self.gender_net.setInput(blob)
        gender_preds = self.gender_net.forward()
        gender = gender_preds[0].argmax()
        return int(gender)

    def find_emote(self, frame):
        roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        roi = cv2.resize(roi, (64, 64))
        roi = roi.astype("float") / 255.0
        roi = preimage.img_to_array(roi)
        roi = np.expand_dims(roi, axis=0)
        predicted = self.model.predict(roi)
        predicted_class = np.argmax(predicted[0])

        return int(predicted_class)

    def find_persons(self, frame):
        predictions = []
        frame_per_recognize = 3

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_labels = []
        for face_location, face_encoding in zip(face_locations, face_encodings):
            location = self.camera.calc_real_coordinates(face_location[3] * 2 + face_location[1] * 2,
                                                         face_location[0] * 2 + face_location[2] * 2)
            location = [str(location[i][0]) for i in range(3)]
            location = "; ".join(location)
            self.control_insert.push_event({"location": location})
            metadata = self.lookup_known_face(face_encoding)
            face_image = self.get_face_from_image(face_location, small_frame)
            type_of_emote = -1

            if metadata is not None:
                time_at_door = datetime.now() - metadata['first_seen_this_interaction']
                face_label = f"Detected {int(time_at_door.total_seconds())}s"

                if metadata['seen_frames'] == 1 + frame_per_recognize:
                    metadata['seen_frames'] -= frame_per_recognize
                    type_of_emote = self.find_emote(face_image)

                    if metadata['emote'] != self.EMOTES_RU[type_of_emote]:
                        metadata['emote'] = self.EMOTES_RU[type_of_emote]
                        self.control_insert.push_recognition(metadata)

                type_of_emote = self.EMOTES_RU.index(metadata['emote'])

                self.control_update.update_metadata(metadata)
                self.control_insert.push_event(metadata)
            else:
                face_label = "New visitor!"
                gnd = self.find_gender(face_image)
                self.register_new_face(face_encoding, face_image, location, gnd)

            face_labels.append((face_label, self.EMOTES[type_of_emote]))

        for (top, right, bottom, left), face_label in zip(face_locations, face_labels):
            submassive = []

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            submassive.append(left)
            submassive.append(top)
            submassive.append(right)
            submassive.append(bottom)
            submassive.append(face_label)
            submassive.append(self.COLORS[self.CLASSES.index("Person")])
            predictions.append(submassive)

        return predictions

    def find_objects(self, frame):
        predictions = []

        (h, w) = frame.shape[:2]
        blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in np.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] == "Person":
                    continue

                submassive = []
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                label = "{}: {:.2f}%".format(self.CLASSES[idx],
                                             confidence * 100)
                y = startY - 15 if startY - 15 > 15 else startY + 15
                location = self.camera.calc_real_coordinates((startX + endX)/2,
                                                             (startY + endY)/2)
                location = [str(location[i][0]) for i in range(3)]
                location = "; ".join(location)

                submassive.append(label)
                submassive.append(startX)
                submassive.append(startY)
                submassive.append(endX)
                submassive.append(endY)
                submassive.append(y)
                submassive.append(self.COLORS[idx])
                predictions.append(submassive)

                self.register_new_object(self.CLASSES_RU[idx], location)

        return predictions
