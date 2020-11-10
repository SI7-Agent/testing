# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.user import User  # noqa: E501
from swagger_server.models.user_token import UserToken  # noqa: E501
from swagger_server.models.user_update import UserUpdate  # noqa: E501
from swagger_server.test import BaseTestCase


class TestUserController(BaseTestCase):
    """UserController integration test stubs"""

    def test_create_user(self):
        """Test case for create_user

        Create user
        """
        userdata = User()
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/user',
            method='POST',
            data=json.dumps(userdata),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_user(self):
        """Test case for delete_user

        Delete user
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/user/{username}'.format(username='username_example'),
            method='DELETE',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_unique_user(self):
        """Test case for get_unique_user

        Get user by user name
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/user/{username}'.format(username='username_example'),
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_login(self):
        """Test case for login

        Logs user into the system
        """
        query_string = [('username', 'username_example'),
                        ('password', 'password_example')]
        response = self.client.open(
            '/api/v1/user/login',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_logout(self):
        """Test case for logout

        Logs out current logged in user session
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/user/logout',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_patch_user_data(self):
        """Test case for patch_user_data

        Updated user
        """
        body = UserUpdate()
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/user/{username}'.format(username='username_example'),
            method='PATCH',
            data=json.dumps(body),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
