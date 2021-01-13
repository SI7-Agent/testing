import pytest
import os
import cv2
import sqlite3
import image_tools

from concrete_base_helper import BaseChooser
from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.people_module import PeopleModuleWeb
from pytest_mock import mocker

from query_tool.postgre_tool import PostgreSQLUserTool


class BuildData:
    class ConnectManager:
        def __init__(self):
            self.cursor = None
            self.database = None

        def set_cursor(self, c):
            self.cursor = c

        def set_database(self, d):
            self.database = d

    class Picture:
        def __init__(self):
            self.picture = None
            self.mime = None

        def set_picture(self, pic):
            self.picture = pic

        def set_mime(self, mime):
            self.mime = mime

        def to_dict(self):
            d = {"picture": self.picture, "mime": self.mime}
            return d

    def build_picture_testing(self):
        test_picture = self.Picture()
        test_picture.set_picture("1111")
        test_picture.set_mime("2222")

        return test_picture

    def build_picture_with_picture(self, pic):
        test_picture = self.Picture()
        test_picture.set_picture(pic)

        return test_picture

    def build_picture_with_mime(self, mime):
        test_picture = self.Picture()
        test_picture.set_mime(mime)

        return test_picture

    def build_connectmanager_dummy(self):
        test_connect_manager = self.ConnectManager()
        test_connect_manager.set_cursor(True)
        test_connect_manager.set_database(True)

        return test_connect_manager

    def build_connectmanager_with_database(self, db):
        test_connect_manager = self.ConnectManager()
        test_connect_manager.set_database(db)
        test_connect_manager.set_cursor(True)

        return test_connect_manager

    def build_connectmanager_with_cursor(self, c):
        test_connect_manager = self.ConnectManager()
        test_connect_manager.set_database(True)
        test_connect_manager.set_cursor(c)

        return test_connect_manager


@pytest.fixture()
def database_env():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    sql_file = open("setup.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    return cursor


@pytest.fixture()
def human_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/git_for_gitlab/swagger_server")
    human_module = PeopleModuleWeb(None)
    return human_module


@pytest.fixture()
def gender_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/git_for_gitlab/swagger_server")
    gender_module = GenderModule(None)
    return gender_module


@pytest.fixture()
def emote_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/git_for_gitlab/swagger_server")
    emote_module = EmoteModule(None)
    return emote_module


def test_int_human_module_and_gender_module_mock(human_env, gender_env, database_env, mocker):
    my_con = BuildData().build_connectmanager_with_cursor(database_env)
    mocker.patch('concrete_base_helper.BaseChooser.choose', return_value=PostgreSQLUserTool(my_con))
    database_controller = BaseChooser.choose(my_con)

    pic = database_controller.get_picture_props(filters='WHERE pics.id_pic=4')
    data = pic[0][-1] + pic[0][-2]
    frame = image_tools.convert_img64_to_imgarray(data)
    human_face = human_env.detect_persons(frame)
    face_loc = int(human_face[0]["top"] / 4), \
               int(human_face[0]["right"] / 4), \
               int(human_face[0]["bottom"] / 4), \
               int(human_face[0]["left"] / 4)
    test_values = gender_env.detect_genders(human_env.get_face_from_image(face_loc, human_face[0]["small"]))
    test_values = "Female" if test_values else "Male"

    assert(test_values == "Male")


def test_int_human_module_and_emote_module_mock(human_env, emote_env, database_env, mocker):
    my_con = BuildData().build_connectmanager_with_cursor(database_env)
    mocker.patch('concrete_base_helper.BaseChooser.choose', return_value=PostgreSQLUserTool(my_con))
    database_controller = BaseChooser.choose(my_con)

    pic = database_controller.get_picture_props(filters='WHERE pics.id_pic=4')
    data = pic[0][-1] + pic[0][-2]
    frame = image_tools.convert_img64_to_imgarray(data)
    human_face = human_env.detect_persons(frame)
    face_loc = int(human_face[0]["top"] / 4), \
               int(human_face[0]["right"] / 4), \
               int(human_face[0]["bottom"] / 4), \
               int(human_face[0]["left"] / 4)
    test_values = emote_env.detect_emotes(human_env.get_face_from_image(face_loc, human_face[0]["small"]))
    test_values = emote_env.EMOTES[test_values]

    assert (test_values == "Happy")
