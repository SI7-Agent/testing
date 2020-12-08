import connexion

from models.picture import Picture
from __main__ import worker
from flask import jsonify
import copy
from easy_jwt import auth


def get_filter_image(type, picture):
    authorization = connexion.request.headers['Authorization']
    type = type.split(",")

    if auth.verify_token(authorization):
        for i in type:
            if i not in worker.CLASSES:
                return "Incorrect type param", 400

        try:
            image = processing['value']
            mimetype = image[:22]

            img = convert_img64_to_imgarray(image)
            orig_img = image_copy(img)

            objects = worker.find_objects(orig_img)

            for i in objects:
                if i["label"] in type:
                    i["status"] = "detection"
            img = put_on_cv_image(img, objects)

            for i in objects:
                if i["label"] in type:
                    i["status"] = "label"
            img = put_on_cv_image(img, objects)

            base64img = convert_imgarray_to_img64(img)

            return jsonify(value=mimetype + base64img), 200

        except:
            return "Server cant process", 500

    else:
        return "Unauthorized", 401


def get_object_list():
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        list = copy.deepcopy(worker.CLASSES)
        for i in range(len(list)):
            list[i] = {"id":i, "value":list[i]}
			
        return jsonify(list), 200
    else:
        return "Not authorized", 401


def process_object_image_with_id(id, picture):
    authorization = connexion.request.headers['Authorization']
    
    if auth.verify_token(authorization):
        try:
            img = picture['value']
            mimetype = img[:22]

            img = convert_img64_to_imgarray(img)
            persons = worker.find_objects(img)

            if id > len(persons):
                return "Not found", 404
                
            id_person = persons[id-1]
            
            base64img = convert_imgarray_to_img64(worker.get_face_from_image(face_loc, id_person["small"]))

            return jsonify(value=mimetype + base64img, name=id_person["label"], top y=id_person["top"], right x=id_person["right"], bottom y=id_person["bottom"], left x=id_person["left"]), 200

        except:
            return "Server cant process", 500
    else:
        return "Unauthorized", 401


def process_object_image(picture):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            img = picture['value']
            mimetype = img[:22]

            img = convert_img64_to_imgarray(img)
            objects = worker.find_objects(img)

            for i in objects:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["status"] = "detection"
            img = put_on_cv_image(img, objects)

            for i in objects:
                i["status"] = "label"
            img = put_on_cv_image(img, objects)

            base64img = convert_imgarray_to_img64(img)

            return jsonify(value=mimetype + base64img), 200

        except:
            return "Server cant process", 500

    else:
        return "Unauthorized", 401
