import sqlite3
import pytest
import image_tools

from modules.emote_module import EmoteModule
from modules.gender_module import GenderModule
from modules.object_module import ObjectModuleWeb
from modules.people_module import PeopleModuleWeb
from query_tool.postgre_tool import PostgreSQLUserTool

TEST_REPEAT = 1


class BuildData:
    class ConnectManager:
        def __init__(self):
            self.cursor = None
            self.database = None

        def set_cursor(self, c):
            self.cursor = c

        def set_database(self, d):
            self.database = d

        def to_dict(self):
            d = {"database": self.database, "cursor": self.cursor}
            return d

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

    def build_connectmanager_with_cursor_and_database(self, c, d):
        test_connect_manager = self.ConnectManager()
        test_connect_manager.set_database(d)
        test_connect_manager.set_cursor(c)

        return test_connect_manager


@pytest.fixture()
def database_env():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    sql_file = open("setup.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    return connection


@pytest.fixture()
def human_env():
    human_module = PeopleModuleWeb(None)
    return human_module


@pytest.fixture()
def object_env():
    object_module = ObjectModuleWeb(None)
    return object_module


@pytest.fixture()
def gender_env():
    gender_module = GenderModule(None)
    return gender_module


@pytest.fixture()
def emote_env():
    emote_module = EmoteModule(None)
    return emote_module


@pytest.mark.parametrize('times', range(1, TEST_REPEAT+1))
def test_get_image_and_return_meta(times, human_env, object_env, gender_env, emote_env, database_env):
    my_con = BuildData().build_connectmanager_with_cursor_and_database(database_env.cursor(), database_env)
    database_controller = PostgreSQLUserTool(my_con)

    pic = database_controller.get_picture_props(filters='WHERE pics.id_pic=4')
    assert(len(pic) == 1)
    data = pic[0][-1] + pic[0][-2]
    frame = image_tools.convert_img64_to_imgarray(data)
    assert(frame is not None)

    persons = human_env.detect_persons(frame)
    assert(len(persons) == 1)

    objects = object_env.detect_objects(frame)
    assert(len(objects) == 0)

    data = []
    for i in persons:
        face_loc = int(i["top"] / 4), int(i["right"] / 4), int(i["bottom"] / 4), int(i["left"] / 4)
        i["emote"] = emote_env.EMOTES[emote_env.detect_emotes(human_env.get_face_from_image(face_loc, i["small"]))]
        i["label"] = "Female" if gender_env.detect_genders(human_env.get_face_from_image(face_loc, i["small"])) else "Male"
        data.append({"label": "Human", "gender": i["label"],
                     "location": ";".join([str(i["top"]), str(i["right"]), str(i["bottom"]), str(i["left"])]),
                     "emote": i["emote"]})

    for i in objects:
        data.append({"label": i["label"], "gender": "None",
                     "location": ";".join([str(i["top"]), str(i["right"]), str(i["bottom"]), str(i["left"])]),
                     "emote": "None"})
    assert(len(data) == 1)

    id_in_base = database_controller.push_picture(pic[0][-1], pic[0][-2], t='t')
    assert(id_in_base == 5)

    for i in data:
        database_controller.push_picture_data(i, t='t')

    pic_in_base = database_controller.get_picture_props(filters='WHERE pics.id_pic=5')
    assert(len(pic_in_base) == 1)
    assert(pic_in_base[0][2] == 'Human')
    assert(pic_in_base[0][3] == 'Male')
    assert(pic_in_base[0][4] == 'Happy')
