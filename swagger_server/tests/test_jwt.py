import pytest

from easy_jwt import JWT


@pytest.fixture()
def jwt_env():
    jwt_module = JWT()
    return jwt_module


def test_jwt_validate_ok(jwt_env):
    jwt_to_validate = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6Im5pZ2dhOTIxMSJ9.iJFYncQ9p6yROkqL_CrHRBhpP8rnr3jVqmvrkvrnDpg'
    test_values = jwt_env.verify_token(jwt_to_validate)
    assert(test_values['username'] == 'nigga9211')


def test_jwt_validate_bad(jwt_env):
    jwt_to_validate = 'aaaaaaa'
    test_values = jwt_env.verify_token(jwt_to_validate)
    assert(test_values is False)


def test_jwt_validate_none(jwt_env):
    jwt_to_validate = None
    test_values = jwt_env.verify_token(jwt_to_validate)
    assert(test_values is False)
