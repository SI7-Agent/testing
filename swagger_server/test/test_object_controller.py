# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.object import Object  # noqa: E501
from swagger_server.models.picture import Picture  # noqa: E501
from swagger_server.models.result_filtered_picture import ResultFilteredPicture  # noqa: E501
from swagger_server.test import BaseTestCase


class TestObjectController(BaseTestCase):
    """ObjectController integration test stubs"""

    def test_get_filter_image(self):
        """Test case for get_filter_image

        Return an image with special mark and id
        """
        query_string = [('id', 56),
                        ('mark', 'mark_example'),
                        ('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/object/findbymarkid',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_object_list(self):
        """Test case for get_object_list

        Return a list of available objects to detect
        """
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/object',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_process_object_image(self):
        """Test case for process_object_image

        Send a picture to process with object properties
        """
        picture = Picture()
        query_string = [('authorization', 'authorization_example')]
        response = self.client.open(
            '/api/v1/object',
            method='POST',
            data=json.dumps(picture),
            content_type='application/json',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
