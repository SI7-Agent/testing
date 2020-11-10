import connexion
import six
import json

from models.object import Object
from models.picture import Picture
import util
import copy
from easy_jwt import auth
from __main__ import worker
from image_tools import convert_img64_to_imgarray, convert_imgarray_to_img64, put_on_cv_image, image_copy, convert_imgarray_to_file


def get_human_list():
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        list = copy.deepcopy(worker.EMOTES)
        list.append("Male")
        list.append("Female")
        for i in range(len(list)):
            list[i] = json.dumps({"id": i, "value": list[i]})
    else:
        return "Unauthorized", 401

    return list


def process_human_image(picture):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            img = picture['value']
            mimetype = img[:22]

            img = convert_img64_to_imgarray(img)
            persons = worker.find_persons(img)

            for i in persons:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["emote"] = worker.EMOTES[worker.find_emote(worker.get_face_from_image(face_loc, i["small"]))]

            for i in persons:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["label"] = "Woman" if worker.find_gender(worker.get_face_from_image(face_loc, i["small"])) else "Man"

            img = put_on_cv_image(img, persons)
            base64img = convert_imgarray_to_img64(img)

            return json.dumps({"value": mimetype + base64img}), 200

        except:
            return "Server cant process", 500

    else:
        return "Unauthorized", 401


def process_human_image_custom(module, processing):
    authorization = connexion.request.headers['Authorization']
    modules = ["detection", "emote", "gender"]

    if auth.verify_token(authorization):
        if module not in modules:
            return "Incorrect module param", 400

        try:
            image = processing['value']
            mimetype = image[:22]

            people_analysed = False
            persons = []

            img = convert_img64_to_imgarray(image)
            orig_img = image_copy(img)

            if "detection" in module:
                people_analysed = True
                persons = worker.find_persons(orig_img)

            if "emote" in module:
                if len(persons) == 0 and not people_analysed:
                    people_analysed = True
                    persons = worker.find_persons(orig_img)

                for i in persons:
                    face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                    i["left"] = None
                    i["emote"] = worker.EMOTES[worker.find_emote(worker.get_face_from_image(face_loc, i["small"]))]

            if "gender" in module:
                if len(persons) == 0 and not people_analysed:
                    persons = worker.find_persons(orig_img)

                for i in persons:
                    face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                    i["left"] = None
                    i["label"] = "Woman" if worker.find_gender(worker.get_face_from_image(face_loc, i["small"])) else "Man"

            img = put_on_cv_image(img, persons)
            base64img = convert_imgarray_to_img64(img)

            return json.dumps({"value": mimetype + base64img}), 200

        except:
            return "Server cant process", 500

    else:
        return "Unauthorized", 401
