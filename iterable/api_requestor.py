import json

import error
import iterable

from .http_client import RequestsClient


class APIRequestor(object):

    ALLOWED_HTTP_METHODS = ['get', 'post']

    def __init__(self, client=None):
        self._api_key = iterable.api_key
        self._client = client or RequestsClient()

    def request(self, method, url, post_data=None, headers=None, root_field=None):
        rbody, rcode, rheaders = self.request_raw(
            method.lower(), url, post_data, headers)

        resp = self.interpret_response(rbody, rcode, rheaders, root_field)
        return resp

    def request_raw(self, method, url, post_data=None, supplied_headers=None):
        if not self._api_key:
            raise error.AuthenticationError('No API key has been provided.')

        if method not in APIRequestor.ALLOWED_HTTP_METHODS:
            raise error.APIConnectionError('Unrecognized HTTP method %r.' % (method, ))

        headers = {'api_key': self._api_key}

        if method == 'post':
            headers['Content-Type'] = 'application/json'

        if supplied_headers is not None:
            for key, val in supplied_headers.iteritems():
                headers[key] = val

        rbody, rcode, rheaders = self._client.request(
            method, url, headers, post_data)

        return rbody, rcode, rheaders

    def interpret_response(self,  rbody, rcode, rheaders, root_field=None):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = json.loads(rbody)

        except Exception:
            raise error.APIError(
                'Invalid response body from API: %s '
                '(HTTP response code was %d)' % (rbody, rcode),
                rbody, rcode, headers=rheaders)

        if rcode != 200:
            self.handle_api_error(rbody, rcode, resp, rheaders)

        if root_field and root_field in resp:
            return resp.get(root_field)

        return resp

    def handle_api_error(self, rbody, rcode, resp, rheaders):
        # TODO: DO SOMETHING REAL HERE
        raise error.APIError('%s %s %s %s' % (rbody, rcode, resp, rheaders))
