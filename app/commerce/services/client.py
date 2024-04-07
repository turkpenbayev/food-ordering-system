import abc
import typing

import requests
from django.conf import settings
from commerce.services import exceptions


class AbstractTelegramClient(abc.ABC):
    DEFAULT_API_ROOT = 'https://api.telegram.org'
    BASE_URL = '{api_root}/bot{bot_token}/{path}'
    DEFAULT_HEADERS = {
        'cache-control': 'no-cache'
    }

    def __init__(self, *args, **kwargs):
        api_root = kwargs.get('api_root')
        if api_root is None:
            self.API_ROOT = self.DEFAULT_API_ROOT
        else:
            self.API_ROOT = api_root

    def make_url(self, path: str) -> str:
        return self.BASE_URL.format(
            api_root=self.API_ROOT,
            bot_token=settings.BOT_TOKEN,
            path=path
        )

    @abc.abstractmethod
    def _post(
            self, url: str, data: str = None, timeout: typing.Union[int, typing.Tuple[int, int], None] = (1.0, 10.0)
    ) -> typing.Union[typing.Dict, typing.List]:
        raise NotImplementedError()

    @abc.abstractmethod
    def _get(
            self, url: str, timeout: typing.Union[int, typing.Tuple[int, int], None] = (1.0, 10.0)
    ) -> typing.Union[typing.Dict, typing.List]:
        raise NotImplementedError()

    @abc.abstractmethod
    def notify_user(self, chat_id: str, text: str):
        pass


class TelegramSyncClient(AbstractTelegramClient):
    def __init__(self, *args, **kwargs):
        super(TelegramSyncClient, self).__init__(*args, **kwargs)
        self.session = requests.Session()

    def close(self):
        self.session.close()

    def _post(
            self, url: str, data: str = None, timeout: typing.Union[int, typing.Tuple[int, int], None] = (1.0, 10.0)
    ) -> typing.Union[typing.Dict, typing.List]:
        try:
            response = self.session.post(url, data, headers=self.DEFAULT_HEADERS, timeout=timeout)
            response.raise_for_status()
            result = response.json()
        except requests.HTTPError as e:
            raise exceptions.ServiceException(status_code=e.response.status_code, data=e.response.content) from e
        except requests.RequestException as e:
            raise exceptions.RequestException() from e
        return result

    def _get(
            self, url: str, timeout: typing.Union[int, typing.Tuple[int, int], None] = (1.0, 10.0)
    ) -> typing.Union[typing.Dict, typing.List]:
        try:
            response = self.session.get(url, headers=self.DEFAULT_HEADERS, timeout=timeout)
            response.raise_for_status()
            if response.status_code == 204:
                return None
            else:
                return response.json()
        except requests.HTTPError as e:
            raise exceptions.ServiceException(status_code=e.response.status_code, data=e.response.content) from e
        except requests.RequestException as e:
            raise exceptions.RequestException() from e

    def notify_user(self, chat_id: str, text: str) -> None:
        path = 'sendMessage'
        payload = {
            'chat_id': chat_id,
            'text': text,
            'parse_mode': 'HTML'
        }
        result = self._post(self.make_url(path), data=payload)
        return None
