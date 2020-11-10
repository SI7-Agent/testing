import connexion

import copy
import json
from easy_jwt import auth
from __main__ import worker
from image_tools import image_copy, put_on_cv_image, convert_imgarray_to_img64, convert_img64_to_imgarray


def get_image_list():
    authorization = connexion.request.headers['Authorization']
    if auth.verify_token(authorization):
        list = copy.deepcopy(worker.CLASSES)
        list += worker.EMOTES
        list.append("Male")
        list.append("Female")
        list = [json.dumps({"id": i, "value": list[i]}) for i in range(len(list))]

        return list
    else:
        return "Unauthorized", 401


def process_image(picture):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            img = picture['value']
            mimetype = img[:22]

            img = convert_img64_to_imgarray(img)
            orig_img = image_copy(img)

            persons = worker.find_persons(orig_img)
            objects = worker.find_objects(orig_img)

            for i in persons:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["emote"] = worker.EMOTES[worker.find_emote(worker.get_face_from_image(face_loc, i["small"]))]

            img = put_on_cv_image(img, persons)

            for i in persons:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["label"] = "Woman" if worker.find_gender(worker.get_face_from_image(face_loc, i["small"])) else "Man"

            img = put_on_cv_image(img, persons)
            img = put_on_cv_image(img, objects)
            base64img = convert_imgarray_to_img64(img)

            return json.dumps({"value": mimetype + base64img}), 200

        except:
            return "Server cant process", 500
