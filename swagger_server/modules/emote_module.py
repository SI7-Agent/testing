from array_methods import ArrayMethods as np1
from robot import Robot

import cv2
import keras.preprocessing.image as preimage


class EmoteModule(Robot):
    @staticmethod
    def emt_decorate(function):
        def find_emote(self, frame):
            roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            roi = cv2.resize(roi, (64, 64))
            roi = roi.astype("float") / 255.0
            roi = preimage.img_to_array(roi)
            roi = np1.expand_dims(roi, axis=0)
            predicted = self.model.predict(roi)
            predicted_class = np1.argmax(predicted[0])

            return int(predicted_class)

        return find_emote
