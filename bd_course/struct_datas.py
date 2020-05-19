from datetime import datetime

import enum
import faker


class RecognitionType(enum.Enum):
    no_changes = 0
    emote_changed = 1
    motion_changed = 2


class DetectionType(enum.Enum):
    human = 'human'
    object = ["Background", "Aeroplane", "Bicycle", "Bird", "Boat", "Bottle", "Bus", "Car",
              "Cat", "Chair", "Cow", "Dinning table", "Dog", "Horse", "Motorbike", "Person",
              "Potted plant", "Sheep", "Sofa", "Train", "Tv monitor"]


class ConstructorObject:
    def generator(self, location, gnd=None, face_en=None, face_image=None, type=DetectionType.human):
        return self.generate_object(type, location) if (type != DetectionType.human) else self.generate_human(face_en, face_image, location, gnd)

    @staticmethod
    def generate_object(name, location):
        return {
            "first_seen": datetime.now(),
            "first_seen_this_interaction": datetime.now(),
            "last_seen": datetime.now(),
            "seen_count": 1,
            "seen_frames": 1,
            "name": name,
            "emote": None,
            "location": location,
            "face_image": None,
            "face_encoding": None
        }

    @staticmethod
    def generate_human(encode, image, location, gender):
        if gender == 0:
            name = faker.Faker('ru_RU').name_male()
        else:
            name = faker.Faker('ru_RU').name_female()

        return {
            "first_seen": datetime.now(),
            "first_seen_this_interaction": datetime.now(),
            "last_seen": datetime.now(),
            "seen_count": 1,
            "seen_frames": 1,
            "name": name,
            "emote": "Нейтральный(-ая)",
            "location": location,
            "face_image": image,
            "face_encoding": encode
        }
