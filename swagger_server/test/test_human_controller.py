# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.object import Object  # noqa: E501
from swagger_server.models.picture import Picture  # noqa: E501
from swagger_server.test import BaseTestCase


class TestHumanController(BaseTestCase):
    """HumanController integration test stubs"""

    def test_get_human_list(self):
        """Test case for get_human_list

        Return a list of available human objects to detect
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/human',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_process_human_image(self):
        """Test case for process_human_image

        Send a picture to process with human properties
        """
        picture = Picture()
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/human',
            method='POST',
            data=json.dumps(picture),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
