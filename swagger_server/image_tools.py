import base64
import cv2
import copy
import os


def convert_img64_to_imgarray(image64):
    convert_img64_to_file(image64, "special_file_name.png")
    imgarray = convert_file_to_imgarray("special_file_name.png")
    os.remove("special_file_name.png")
    return imgarray


def convert_imgarray_to_img64(imgarray):
    convert_imgarray_to_file(imgarray, "special_file_name.png")
    image64 = convert_file_to_img64("special_file_name.png")
    os.remove("special_file_name.png")
    return image64


def convert_img64_to_file(image64, filename):
    pic = image64[22:]
    pic = base64.b64decode(pic)
    with open(filename, "wb") as f:
        f.write(pic)


def convert_file_to_imgarray(filename):
    image = cv2.imread(filename)
    return image


def convert_file_to_img64(filename):
    with open(filename, "rb") as f:
        encode = base64.b64encode(f.read())

    return encode.decode("utf-8")


def convert_imgarray_to_file(imgarray, filename):
    cv2.imwrite(filename, imgarray)


def image_copy(img):
    return copy.deepcopy(img)


def put_on_cv_image(img, boxes):
    if len(boxes) > 0:
        for i in boxes:
            #rectangle_detection
            cv2.rectangle(img, (i["left"], i["top"]), (i["right"], i["bottom"]), i["color"], 2)

            #type_of_object
            y = i["top"] - 15 if i["top"] - 15 > 15 else i["top"] + 15
            cv2.putText(img, i["label"], (i["right"] + 6, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, i["color"], 2)
            
            if "emote" in i.keys() and i["emote"] != "None":
                y = i["bottom"] - 6 if i["bottom"] - 6 > 6 else i["bottom"] + 6
                cv2.putText(img, i["emote"], (i["right"] + 6, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, i["color"], 2)

            if "gender" in i.keys() and i["gender"] != "None":
                y = i["top"] - 15 if i["top"] - 15 > 15 else i["top"] + 15
                cv2.putText(img, i["gender"], (i["left"] + 6, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, i["color"], 2)

    return img
