import pytest
import cv2
import os

from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.object_module import ObjectModuleWeb
from modules.people_module import PeopleModuleWeb


@pytest.fixture()
def human_env():
    os.chdir("..")
    human_module = PeopleModuleWeb(None)
    return human_module


@pytest.fixture()
def object_env():
    os.chdir("..")
    object_module = ObjectModuleWeb(None)
    return object_module


@pytest.fixture()
def gender_env():
    os.chdir("..")
    human_module = PeopleModuleWeb(None)
    gender_module = GenderModule(None)
    return [human_module, gender_module]


@pytest.fixture()
def emote_env():
    os.chdir("..")
    human_module = PeopleModuleWeb(None)
    emote_module = EmoteModule(None)
    return [human_module, emote_module]
# ======================================


def test_human_module_one_ok(human_env):
    frame = cv2.imread('tests/test_pics/human_one_ok.png')
    test_values = human_env.detect_persons(frame)
    assert(len(test_values) == 1)


def test_human_module_many_ok(human_env):
    frame = cv2.imread('tests/test_pics/human_2+_ok.png')
    test_values = human_env.detect_persons(frame)
    assert(len(test_values) == 3)


def test_human_module_bad(human_env):
    frame = "asasd"
    test_values = human_env.detect_persons(frame)
    assert(test_values is None)


def test_human_module_zero(human_env):
    frame = cv2.imread('tests/test_pics/human_no.png')
    test_values = human_env.detect_persons(frame)
    assert(len(test_values) == 0)
# ====================================


def test_object_module_one_ok(object_env):
    frame = cv2.imread('tests/test_pics/object_one_ok.jpg')
    test_values = object_env.detect_objects(frame)
    assert(len(test_values) == 1 and test_values[0]["label"] == "Cat")
    # assert(len(test_values) == 1)
    # assert(test_values[0]["label"] == "Dog")


def test_object_module_many_ok(object_env):
    frame = cv2.imread('tests/test_pics/object_2+_ok.jpg')
    test_values = object_env.detect_objects(frame)
    assert(len(test_values) == 2 and test_values[0]["label"] == "Cat" and test_values[1]["label"] == "Dog")
    # assert(len(test_values) == 2)
    # assert(test_values[0]["label"] == "Cat")
    # assert(test_values[1]["label"] == "Dog")


def test_object_module_bad(object_env):
    frame = "asasd"
    test_values = object_env.detect_objects(frame)
    assert(test_values is None)


def test_object_module_zero(object_env):
    frame = cv2.imread('tests/test_pics/object_no.png')
    test_values = object_env.detect_objects(frame)
    assert(len(test_values) == 0)
# ====================================


def test_gender_module_ok(gender_env):
    frame = cv2.imread('tests/test_pics/human_one_ok.png')
    human_face = gender_env[0].detect_persons(frame)
    face_loc = int(human_face[0]["top"] / 4), \
               int(human_face[0]["right"] / 4), \
               int(human_face[0]["bottom"] / 4), \
               int(human_face[0]["left"] / 4)
    test_values = gender_env[1].detect_genders(gender_env[1].get_face_from_image(face_loc, human_face[0]["small"]))
    test_values = "Female" if test_values else "Male"
    assert(test_values == "Male")


def test_gender_module_bad(gender_env):
    frame = "asasd"
    test_values = gender_env[1].detect_genders(frame)
    assert(test_values is None)
# ====================================


def test_emote_module_ok(emote_env):
    frame = cv2.imread('tests/test_pics/human_one_ok.png')
    human_face = emote_env[0].detect_persons(frame)
    face_loc = int(human_face[0]["top"] / 4), \
               int(human_face[0]["right"] / 4), \
               int(human_face[0]["bottom"] / 4), \
               int(human_face[0]["left"] / 4)
    test_values = emote_env[1].detect_emotes(emote_env[1].get_face_from_image(face_loc, human_face[0]["small"]))
    test_values = emote_env[1].EMOTES[test_values]
    assert(test_values == "Happy")


def test_emote_module_bad(emote_env):
    frame = "asasd"
    test_values = emote_env[1].detect_emotes(frame)
    assert(test_values is None)
