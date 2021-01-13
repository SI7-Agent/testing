import sqlite3
import pytest



@pytest.fixture()
def database_env():
    connection = sqlite3.connect(":memory:")
    cursor = connection.cursor()
    sql_file = open("setup.sql")
    sql_as_string = sql_file.read()
    cursor.executescript(sql_as_string)
    return cursor


def test_int_human_module_and_gender_module_mock():
    pass


def test_int_human_module_and_emote_module_mock():
    pass
