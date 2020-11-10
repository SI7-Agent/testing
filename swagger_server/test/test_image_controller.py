# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.object import Object  # noqa: E501
from swagger_server.models.picture import Picture  # noqa: E501
from swagger_server.test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_get_image_list(self):
        """Test case for get_image_list

        Return a list of available objects to detect
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/image',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_process_image(self):
        """Test case for process_image

        Send a picture to process
        """
        picture = Picture()
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/image',
            method='POST',
            data=json.dumps(picture),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
