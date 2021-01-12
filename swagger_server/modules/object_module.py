from array_methods import ArrayMethods as np1
from robot import Robot

import cv2


class ObjectModule(Robot):
    @staticmethod
    def obj_decorate(function):
        def find_objects(self, frame):
            predictions = []

            try:
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            except TypeError:
                return None

            (h, w) = frame.shape[:2]
            self.net.setInput(blob)
            detections = self.net.forward()
            for i in np1.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > 0.2:
                    idx = int(detections[0, 0, i, 1])
                    if self.CLASSES[idx] == "Person":
                        continue

                    submassive = []
                    box = detections[0, 0, i, 3:7] * np1.array([w, h, w, h])
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

        return find_objects


class ObjectModuleWeb(Robot):
    @staticmethod
    def obj_decorate(function):
        def find_objects(self, frame):
            predictions = []

            try:
                blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
            except TypeError:
                return None

            (h, w) = frame.shape[:2]
            self.net.setInput(blob)
            detections = self.net.forward()
            for i in np1.arange(0, detections.shape[2]):
                confidence = detections[0, 0, i, 2]

                if confidence > 0.2:
                    idx = int(detections[0, 0, i, 1])
                    if self.CLASSES[idx] == "Person":
                        continue

                    submassive = {"left": 0, "top": 0, "right": 0, "bottom": 0, "label": "", "color": None, "chance": 0, "status": None}
                    box = detections[0, 0, i, 3:7] * np1.array([w, h, w, h])
                    (startX, startY, endX, endY) = box.astype("int")

                    submassive["label"] = self.CLASSES[idx]
                    submassive["left"] = startX
                    submassive["top"] = startY
                    submassive["right"] = endX
                    submassive["bottom"] = endY
                    submassive["color"] = self.COLORS[idx]
                    submassive["chance"] = confidence * 100
                    predictions.append(submassive)

            return predictions

        return find_objects

    def detect_objects(self, frame):
        predictions = []

        try:
            blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)
        except TypeError:
            return None

        (h, w) = frame.shape[:2]
        self.net.setInput(blob)
        detections = self.net.forward()
        for i in np1.arange(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]

            if confidence > 0.2:
                idx = int(detections[0, 0, i, 1])
                if self.CLASSES[idx] == "Person":
                    continue

                submassive = {"left": 0, "top": 0, "right": 0, "bottom": 0, "label": "", "color": None, "chance": 0,
                              "status": None}
                box = detections[0, 0, i, 3:7] * np1.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")

                submassive["label"] = self.CLASSES[idx]
                submassive["left"] = startX
                submassive["top"] = startY
                submassive["right"] = endX
                submassive["bottom"] = endY
                submassive["color"] = self.COLORS[idx]
                submassive["chance"] = confidence * 100
                predictions.append(submassive)

        return predictions