import pytest
import os
import cv2

from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.people_module import PeopleModuleWeb


@pytest.fixture()
def human_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/testing")
    human_module = PeopleModuleWeb(None)
    return human_module


@pytest.fixture()
def gender_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/testing")
    gender_module = GenderModule(None)
    return gender_module


@pytest.fixture()
def emote_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/testing")
    emote_module = EmoteModule(None)
    return emote_module


def test_int_human_module_and_gender_module_mock(human_env, gender_env, database_env):
    frame = cv2.imread('tests/test_pics/human_one_ok.png')

    human_face = human_env.detect_persons(frame)
    face_loc = int(human_face[0]["top"] / 4), \
               int(human_face[0]["right"] / 4), \
               int(human_face[0]["bottom"] / 4), \
               int(human_face[0]["left"] / 4)
    test_values = gender_env.detect_genders(human_env.get_face_from_image(face_loc, human_face[0]["small"]))
    test_values = "Female" if test_values else "Male"

    assert(test_values == "Male")


# def test_int_human_module_and_emote_module_mock(human_env, emote_env, database_env):
#     frame = cv2.imread('tests/test_pics/human_one_ok.png')
#
#     human_face = human_env.detect_persons(frame)
#     face_loc = int(human_face[0]["top"] / 4), \
#                int(human_face[0]["right"] / 4), \
#                int(human_face[0]["bottom"] / 4), \
#                int(human_face[0]["left"] / 4)
#     test_values = emote_env.detect_emotes(human_env.get_face_from_image(face_loc, human_face[0]["small"]))
#     test_values = emote_env.EMOTES[test_values]
#
#     assert (test_values == "Happy")
