import typing


class RequestException(Exception):
    def __init__(self, message: typing.Optional[str] = 'Error sending request to Telegram'):
        super(RequestException, self).__init__(message)


class ServiceException(Exception):
    def __init__(
            self,
            message: typing.Optional[str] = None,
            status_code: typing.Optional[int] = None,
            data: typing.Optional[typing.Any] = None
    ):
        if message is None:
            message = 'HTTP error occurred sending request to Telegram'
        super(ServiceException, self).__init__(message)
        self.status_code = status_code
        self.data = data
