from datetime import datetime
from robot import Robot

import cv2
import face_recognition


class PeopleModule(Robot):
    @staticmethod
    def people_decorate(function):
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
                self.control_tool.push_event({"location": location})
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
                            self.control_tool.push_recognition(metadata)

                    type_of_emote = self.EMOTES_RU.index(metadata['emote'])

                    self.control_tool.update_metadata(metadata)
                    self.control_tool.push_event(metadata)
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

        return find_persons


class PeopleModuleWeb(Robot):
    @staticmethod
    def people_decorate(function):
        def find_persons(self, frame):
            predictions = []

            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

            face_locations = face_recognition.face_locations(small_frame)

            for (top, right, bottom, left) in face_locations:
                submassive = {"left": None, "top": None, "right": None, "bottom": None, "label": "", "color": None, "small": None}

                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                submassive["left"] = left
                submassive["top"] = top
                submassive["right"] = right
                submassive["bottom"] = bottom
                submassive["color"] = self.COLORS[self.CLASSES.index("Person")]
                submassive["small"] = small_frame
                predictions.append(submassive)

            return predictions

        return find_persons