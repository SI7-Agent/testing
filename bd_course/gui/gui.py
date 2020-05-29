from gui.abstract_gui import gui

import cv2


class OpencvGui(gui):
    def __init__(self):
        self.camera = cv2.VideoCapture(0)

    def make_ui(self, handler):
        while self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                objects = handler.find_objects(frame)
                persons = handler.find_persons(frame)

                for i in objects:
                    cv2.rectangle(frame, (i[1], i[2]), (i[3], i[4]), i[-1], 2)
                    cv2.putText(frame, i[0], (i[1], i[-2]), cv2.FONT_HERSHEY_SIMPLEX, 0.5, i[-1], 2)

                #           =======================================================

                for i in persons:
                    cv2.rectangle(frame, (i[0], i[1]), (i[2], i[3]), i[-1], 2)
                    cv2.putText(frame, i[-2][0], (i[0] + 6, i[3] - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
                    cv2.putText(frame, i[-2][1], (i[0] + 6, i[1] - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)

                cv2.imshow('Video', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
        self.camera.release()
        cv2.destroyAllWindows()
