import textwrap
import requests

import error


class HTTPClient(object):

    def request(self, method, url, headers, post_data=None):
        raise NotImplementedError('HTTPClient subclasses must implement `request`')


class RequestsClient(HTTPClient):

    def request(self, method, url, headers, post_data=None):
        try:
            result = requests.request(
                method,
                url,
                headers=headers,
                json=post_data)

            content = result.content
            status_code = result.status_code

        except Exception as e:
            self._handle_request_error(e)

        return content, status_code, result.headers

    def _handle_request_error(self, e):
        if isinstance(e, requests.exceptions.RequestException):
            msg = ('There was a problem communicating with Iterable.')
            err = '%s %s' % (type(e).__name__, str(e))

        else:
            msg = ('There was a problem communicating with Iterable. '
                   'This is likely do to a local configuration problem.')
            err = 'A %s was raised' % (type(e).__name__, )
            if str(e):
                err += ' with error message %s' % (str(e), )
            else:
                err += ' with no error message'

        msg = textwrap.fill(msg) + '\n\n(Network error: %s)' % (err, )
        raise error.APIConnectionError(msg)
