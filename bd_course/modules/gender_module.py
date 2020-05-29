from robot import Robot

import cv2


class GenderModule(Robot):
    @staticmethod
    def gnd_decorate(function):
        def find_gender(self, frame):
            blob = cv2.dnn.blobFromImage(frame, 1, (227, 227), (78.4263377603, 87.7689143744, 114.895847746), swapRB=False)
            self.gender_net.setInput(blob)
            gender_preds = self.gender_net.forward()
            gender = gender_preds[0].argmax()
            return int(gender)

        return find_gender
