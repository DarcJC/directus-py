# -*- coding: utf-8 -*-
from api_types import *
from typing import Optional, Callable

import requests
import functools

from pydantic.types import constr


class _Map(dict):
    def __getattr__(self, item):
        return self[item]


class DirectusClient(object):
    def __init__(self, *, base_url: constr(min_length=5), token: constr(min_length=16)):
        self._token = token
        self._base_url = base_url

    @property
    def _request(self):
        return functools.partial(requests.request, headers={
            "Authorization": f"Bearer {self._token}",
        })

    def _fetch(self, *,
               url: constr(min_length=1),
               method: methods = 'GET',
               data: Optional[dict] = None,
               params: Optional[dict] = None) -> dict:
        return _Map(
            self._request(
                method=method,
                url=f"{self._base_url}{url}",
                data=data,
                params=params,
            ).json()
        )

    @staticmethod
    def _map(*args: Callable):
        def format_name(name: str):
            if name.startswith('_'):
                return name[1:]
            return name

        return _Map({format_name(i.__name__): i for i in args})

    @property
    def activity(self) -> ActivityAction:
        def _list():
            _url = '/activity'
            return self._fetch(url=_url, method='GET')

        def _list_by_id(_id: constr(min_length=1)):
            _url = f'/activity/{_id}'
            return self._fetch(url=_url, method='GET')

        return self._map(
            _list,
            _list_by_id,
        )


if __name__ == '__main__':
    _token = 'a' * 16
    client = DirectusClient(token=_token, base_url='http://localhost:8055')
    print(client.activity.__dir__())
