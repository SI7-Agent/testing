import connexion

from models.picture import Picture
from __main__ import worker
import json
import copy
from easy_jwt import auth

def get_filter_image(id, authorization, mark=None):  # noqa: E501
    """Return an image with special mark and id

     # noqa: E501

    :param id: Filter id option
    :type id: int
    :param authorization: 
    :type authorization: str
    :param mark: Filter mark option
    :type mark: str

    :rtype: List[ResultFilteredPicture]
    """
    return 'idi nahui'


def get_object_list():
    authorization = connexion.request.headers['Authorization']
    """Return a list of available objects to detect

     # noqa: E501

    :param authorization: 
    :type authorization: str

    :rtype: List[Object]
    """
    if authorization == "aa":
        list = copy.deepcopy(worker.CLASSES)
        for i in range(len(list)):
            list[i] = json.dumps({"id": i, "value": list[i]})
    else:
        return "Not authorized", 401
    return list


def process_object_image(picture):
    authorization = connexion.request.headers['Authorization']
    """Send a picture to process with object properties

     # noqa: E501

    :param picture: Picture to process
    :type picture: dict | bytes
    :param authorization: 
    :type authorization: str

    :rtype: Picture
    """
    if connexion.request.is_json:
        picture = Picture.from_dict(connexion.request.get_json())  # noqa: E501
    return 'do some magic!'
