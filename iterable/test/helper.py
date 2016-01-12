import unittest

from mock import patch, Mock

import iterable


class IterableTestCase(unittest.TestCase):

    def setUp(self):
        super(IterableTestCase, self).setUp()
        iterable.api_key = '0231ab012f5448e7b080a1c47ec2d28b'


class IterableUnitTestCase(IterableTestCase):

    def setUp(self):
        super(IterableUnitTestCase, self).setUp()

        patcher = patch('iterable.http_client.requests')

        self.request_mock = patcher.start()
        self.request_patcher = patcher
    
    def tearDown(self):
        super(IterableUnitTestCase, self).tearDown()

        self.request_patcher.stop()


class IterableApiTestCase(IterableTestCase):

    def setUp(self):
        super(IterableApiTestCase, self).setUp()

        self.requestor_patcher = patch('iterable.resource.APIRequestor')
        requestor_class_mock = self.requestor_patcher.start()
        self.requestor_mock = requestor_class_mock.return_value

    def tearDown(self):
        super(IterableApiTestCase, self).tearDown()

        self.requestor_patcher.stop()

    def mock_response(self, res):
        self.requestor_mock.request = Mock(return_value=res)
