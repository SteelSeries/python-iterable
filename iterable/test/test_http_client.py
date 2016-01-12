from mock import Mock

import iterable

from iterable.test.helper import IterableUnitTestCase

VALID_API_METHODS = ('get', 'post')


class RequestsClientTests(IterableUnitTestCase):

    @property
    def valid_url(self, path='/foo'):
        return 'https://api.iterable.com/api%s' % (path,)

    def make_request(self, method, url, headers, post_data):
        client = iterable.http_client.RequestsClient()
        return client.request(method, url, headers, post_data)

    def mock_response(self, mock, body, code):
        result = Mock()
        result.content = body
        result.status_code = code

        mock.request = Mock(return_value=result)

    def mock_error(self, mock):
        mock.exceptions.RequestException = Exception
        mock.request.side_effect = mock.exceptions.RequestException()

    def check_call(self, mock, meth, url, headers, post_data):
        mock.request.assert_called_with(meth, url, headers=headers, json=post_data)

    def test_request(self):
        self.mock_response(self.request_mock, '{"foo": "baz"}', 200)

        for meth in VALID_API_METHODS:
            abs_url = self.valid_url
            data = ''

            if meth != 'post':
                data = None

            headers = {'my-header': 'header val'}

            body, code, _ = self.make_request(meth, abs_url, headers, data)

            self.assertEqual(200, code)
            self.assertEqual('{"foo": "baz"}', body)

            self.check_call(self.request_mock, meth, abs_url, headers, data)

    def test_exception(self):
        self.mock_error(self.request_mock)
        self.assertRaises(iterable.error.APIConnectionError, self.make_request, 'get', self.valid_url, {}, None)
