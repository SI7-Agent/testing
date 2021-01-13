import os

import cv2
import pytest

from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.people_module import PeopleModuleWeb


@pytest.fixture()
def human_env():
    if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
        os.chdir("tests")
    os.chdir("..")
    human_module = PeopleModuleWeb(None)
    return human_module


@pytest.fixture()
def gender_env():
    if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
        os.chdir("tests")
    os.chdir("..")
    gender_module = GenderModule(None)
    return gender_module


@pytest.fixture()
def emote_env():
    if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
        os.chdir("tests")
    os.chdir("..")
    emote_module = EmoteModule(None)
    return emote_module


def test_int_human_module_and_gender_module_no_mock():
    frame = cv2.imread('tests/test_pics/human_one_ok.png')


def test_int_human_module_and_emote_module_no_mock():
    pass
