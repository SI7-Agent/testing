import connexion

import copy
import json
from easy_jwt import auth
from __main__ import worker
from image_tools import image_copy, put_on_cv_image, convert_imgarray_to_img64, convert_img64_to_imgarray
  

def get_image_by_id(id):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            data = worker.control_tool.get_picture_props(filters='WHERE pics.id_pic='+str(id))

            if len(data) == 0:
                return "Not found", 404

            base64_img = data[0][7]
            mime = data[0][8]

            image = convert_img64_to_imgarray(mime+base64_img)

            values_to_print = []
            for i in data:
                loc = list(map(lambda x: int(x), i[5].split(";")))
                values_to_print.append({"label": i[2], "top": loc[0], "right": loc[1], "bottom": loc[2], "left": loc[3], "emote": i[4], "gender": i[3], "color": tuple(worker.COLORS[0 if i[2] == "Human" else 1])})

            put_on_cv_image(image, values_to_print)

            send_image = convert_imgarray_to_img64(image)

            return json.dumps({"value": mime + send_image}), 200
        except:
            return "Server cant process", 500
    else:
        return "Unauthorized", 401


def get_detections_from_image(id, type="", emotion="", gender=""):
    authorization = connexion.request.headers['Authorization']
    type = type.split(",")
    emotion = emotion.split(",")
    gender = gender.split(",")

    if auth.verify_token(authorization):
        try:
            for i in type:
                if type.count(i) > 1:
                    return "Invalid query params", 400
            for i in emotion:
                if emotion.count(i) > 1:
                    return "Invalid query params", 400
            for i in gender:
                if gender.count(i) > 1:
                    return "Invalid query params", 400

            if "" not in emotion and "Human" not in type:
                return "Invalid query params", 400
            if "" not in gender and "Human" not in type:
                return "Invalid query params", 400
            
            data = "where pics.id_pic="+str(id)
            if type[0] != "":
                data += " and ("
                for t in type:
                    if t == "Human":
                        data += "(pics_data.label = 'Human'"
                        if emotion[0] != "":
                            data += " and ("    
                            for e in emotion:
                                data += "pics_data.emote='"+e+"' or "
                            data = data[:-4] + ")"
                        if gender[0] != "":
                            data += " and ("
                            for g in gender:
                                data += "pics_data.gender='"+g+"' or "
                            data = data[:-4] + ")"
                        data += ")"
                    else:
                        data += " or pics_data.label = '"+t+"'"
                data += ")"
                
            metadata = worker.control_tool.get_picture_props(filters=data)

            if len(metadata) == 0:
                return "Not found", 404

            result = []
            mime = metadata[0][8]
            my_img_pr = convert_img64_to_imgarray(mime+metadata[0][7])
            for i in metadata:
                loc = list(map(lambda x: int(x), i[5].split(";")))
                mini_img = worker.get_object_from_image(loc, my_img_pr)
                base64 = convert_imgarray_to_img64(mini_img)
                result.append(json.dumps({"base64": mime+base64, "gender": i[3], "location": i[5], "type": i[2], "emote": i[4]}))
            
            return result, 200 
        except:
            return "Server cant process", 500
    else:
        return "Unauthorized", 401


def get_list(filter=None):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        list = []
        if filter is None:
            list = copy.deepcopy(worker.CLASSES)
            list.append("Human")
            list += worker.EMOTES
            list.append("Male")
            list.append("Female")
        elif filter == "gender":
            list = ["Male", "Female"]
        elif filter == "emotion":
            list = copy.deepcopy(worker.EMOTES)
        elif filter == "objects":
            list = copy.deepcopy(worker.CLASSES)
            list.append("Human")

        list = [json.dumps({"id": i, "value": list[i]}) for i in range(len(list))]

        return list
    else:
        return "Unauthorized", 401
    


def process_image2(picture):
    authorization = connexion.request.headers['Authorization']

    if auth.verify_token(authorization):
        try:
            img = picture['value']
            mimetype = img[:22]

            img = convert_img64_to_imgarray(img)

            persons = worker.find_persons(img)
            objects = worker.find_objects(img)

            data = []
            for i in persons:
                face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
                i["emote"] = worker.EMOTES[worker.find_emote(worker.get_face_from_image(face_loc, i["small"]))]
                i["label"] = "Female" if worker.find_gender(worker.get_face_from_image(face_loc, i["small"])) else "Male"
                data.append({"label": "Human", "gender": i["label"], "location": ";".join([str(i["top"]),str(i["right"]),str(i["bottom"]),str(i["left"])]), "emote": i["emote"]})

            for i in objects:
                data.append({"label": i["label"], "gender": "None", "location": ";".join([str(i["top"]),str(i["right"]),str(i["bottom"]),str(i["left"])]), "emote": "None"})

            id = worker.control_tool.push_picture(picture['value'][22:], mimetype)
   
            for i in data:
                worker.control_tool.push_picture_data(i)           

            return json.dumps({"id": id}), 200

        except:
            return "Server cant process", 500
    else:
        return "Unauthorized", 401


def get_image_props(id, type, filter):
    authorization = connexion.request.headers['Authorization']
    filter = filer.split(",")

    if auth.verify_token(authorization):
        if type not in ["location", "objects", "all"]:
            return "Incorrect type param", 400

        for i in filter:
            if i not in worker.CLASSES+["emote","gender", "location"]:
                return "Incorrect filter param", 400
 
        try:
            params = ''
            #for i in filter
            #data = worker.control_tool.get_picture_props()
        except:
            return "Server cant process", 500
    else:
        return "Unauthorized", 401


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
    else:
        return "Unauthorized", 401
