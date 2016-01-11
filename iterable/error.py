class IterableError(Exception):
    
    def __init__(self, message=None, http_body=None, http_status=None, json_body=None, headers=None):
        super(IterableError, self).__init__(message)

        if http_body and hasattr(http_body, 'decode'):
            try:
                http_body = http_body.decode('utf-8')
            except:
                http_body = ('<Could not decode as utf-8.>')

        self._message = message
        self.http_body = http_body
        self.http_status = http_status
        self.json_body = json_body
        self.headers = headers or {}

        def __unicode__(self):
            return self._message


class AuthenticationError(IterableError):
    pass


class APIConnectionError(IterableError):
    pass


class APIError(IterableError):
    pass
