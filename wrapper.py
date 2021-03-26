# -*- coding: utf-8 -*-

import requests
import functools
import os
from typing import Literal

METHOD = Literal['GET', 'POST', 'PUT', 'DELETE', 'PATCH']


def _process_request(*, method: METHOD = 'GET', url: str = None, data: dict = None, token: str = None):
    if not url or not token:
        raise ValueError('bad url or token param')
    res = requests.request(method=method, url=url, data=data,
                           headers={
                               'Authorization': f"Bearer {token}",
                           })
    return res.json()


process_request = functools.partial(_process_request, token=os.environ.get('OA_DIRECTUS_TOKEN', None))

