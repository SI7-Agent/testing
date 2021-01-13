import os
import pytest
import psycopg2
import sqlite3

from admin_tools.admin_tool import AdminTool
from concrete_base_helper import BaseChooser
from connect.connect_manager import ConnectManager
import connect.connect_manager
from pytest_mock import mocker


class BuildData:
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

    class Config:
        def __init__(self):
            self.database = None
            self.dbname = None
            self.user = None
            self.password = None
            self.host = None
            self.port = None

        def set_database(self, db):
            self.database = db

        def set_dbname(self, name):
            self.dbname = name

        def set_user(self, user):
            self.user = user

        def set_password(self, pw):
            self.password = pw

        def set_host(self, host):
            self.host = host

        def set_port(self, port):
            self.port = port

        def to_dict(self):
            d = {"database": self.database, "dbname": self.dbname, "user": self.user, "password": self.password,
                 "host": self.host, "port": self.port}
            return d

    def build_config_ok(self):
        test_config = self.Config()
        test_config.set_database("postgresql")
        test_config.set_dbname("postgres")
        test_config.set_user("postgres")
        test_config.set_password("rocketman1")
        test_config.set_host("localhost")
        test_config.set_port("5433")

        return test_config

    def build_config_bad(self):
        test_config = self.Config()
        test_config.set_database("postgresql")
        test_config.set_dbname("postgres")
        test_config.set_user("postgres")
        test_config.set_password("zaqwsxcde")
        test_config.set_host("localhost")
        test_config.set_port("5433")

        return test_config

    def build_config_testing(self):
        test_config = self.Config()
        test_config.set_database("postgresql")
        test_config.set_dbname("testing_database")
        test_config.set_user("postgres")
        test_config.set_password("rocketman1")
        test_config.set_host("localhost")
        test_config.set_port("5433")

        return test_config

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


@pytest.fixture()
def access_env():
    if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
        os.chdir("C:/Users/Asus/Desktop/git_for_gitlab/swagger_server/tests")
        my_connect = connect.connect_manager.ConnectManager("test_create_database.ini")
        my_base_commands = BaseChooser.choose(my_connect)
        return my_base_commands


def test_make_connection_ok_classic():
    connection = sqlite3.connect(':memory:')

    c = connection.cursor

    assert (c is not None)


def test_make_connection_ok_mocking(mocker):
    print(os.getcwd())
    mocker.patch('connect.connect_manager.ConnectManager.read_connection_config', return_value=BuildData().build_config_ok().to_dict())
    if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
        mocker.patch('connect.connect_manager.ConnectManager', return_value=(True, True))

    cm = connect.connect_manager.ConnectManager()
    d, c = cm.database, cm.cursor

    assert (d is not None and c is not None)


# def test_make_connection_bad_classic():
#     os.chdir("./tests")
#
#     with pytest.raises(psycopg2.errors.ConnectionFailure) as c:
#         connect.connect_manager.ConnectManager('test_connection_bad.ini')
#
#     assert(c)
#
#
# def test_make_connection_bad_mocking(mocker):
#     mocker.patch('connect.connect_manager.ConnectManager.read_connection_config', return_value=BuildData().build_config_bad().to_dict())
#
#     with pytest.raises(psycopg2.errors.ConnectionFailure) as c:
#         connect.connect_manager.ConnectManager()
#
#     assert(c)
#
#
# def test_create_database(mocker):
#     if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
#         mocker.patch('connect.connect_manager.ConnectManager.read_connection_config', return_value=BuildData().build_config_ok().to_dict())
#         admin_connect = connect.connect_manager.ConnectManager()
#         AdminTool(admin_connect).admin_tool().create_database(config=BuildData().build_config_testing().to_dict())
#         mocker.patch('connect.connect_manager.ConnectManager.read_connection_config', return_value=BuildData().build_config_testing().to_dict())
#         my_connect = connect.connect_manager.ConnectManager()
#         my_base_commands = BaseChooser.choose(my_connect)
#         AdminTool(my_connect).admin_tool().create_tables()
#
#         assert(my_base_commands.connectmanager.database is not None and my_base_commands.connectmanager.cursor is not None)
#
#     else:
#         assert True
#
#
# def test_push_picture(access_env):
#     if os.getcwd() != '/builds/SI7-Agent/web/swagger_server':
#         push_data = BuildData().build_picture_testing()
#         exp_id = access_env.push_picture(push_data.picture, push_data.mime)
#
#         assert(exp_id > 0)
#     else:
#         assert True
#
#
# def test_get_picture_by_id_ok(access_env):
#     if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
#         test_id = 3
#         test_values = access_env.get_picture_props(filters='WHERE pics.id_pic='+str(test_id))
#
#         assert(test_values[-1][-2] == 'unical_picture')
#     else:
#         assert True
#
#
# def test_get_picture_by_id_zero(access_env):
#     if os.getcwd() == '/builds/SI7-Agent/web/swagger_server':
#         test_id = 100000
#         test_values = access_env.get_picture_props(filters='WHERE pics.id_pic='+str(test_id))
#         assert(test_values == [])
#     else:
#         assert True
