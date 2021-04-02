# -*- coding:utf-8 -*-
from typing import List, Literal, AnyStr, MutableMapping, Any, Optional

from pydantic import conint

LogicalOperator = Literal['_and', '_or']
FilterOperator = Literal[
    '_eq',  # Equal to
    '_neq',  # Not equal to
    '_lt',  # Less than
    '_lte',  # Less than or equal to
    '_gt',  # Greater than
    '_gte',  # Greater than or equal to
    '_in',  # Exists in one of the values
    '_nin',  # Not in one of the values
    '_null',  # It is null
    '_nnull',  # It is not null
    '_contains',  # Contains the substring
    '_ncontains',  # Doesn't contain the substring
    '_between',  # The value is between two values
    '_nbetween',  # The value is not between two values
    '_empty',  # The value is empty (null or falsy)
    '_nempty',  # The value is not empty (null or falsy)
]
FilterField = LogicalOperator or AnyStr
FilterDynamicVar = Literal['$CURRENT_USER', '$CURRENT_ROLE', '$NOW']


class GlobalQuery(object):
    def __init__(self):
        self._fields: List[str] = []
        self._filters: MutableMapping[FilterField, MutableMapping] = {}
        self._search: Optional[str] = None
        self._sort: List[str] = []
        self._limit: Optional[Literal[-1] or conint(gt=0)] = None
        self._offset: Optional[conint(ge=0)] = None
        self._page: Optional[conint(ge=1)] = None
        self._deep: MutableMapping[AnyStr, MutableMapping] = {}
        self._meta: Optional[str] = None

    def field(self, *args: str):
        self._fields.extend(args)
        return self

    def filter(self, field: FilterField, operator: FilterOperator, value: AnyStr or FilterDynamicVar):
        self._filters[field] = {
            operator: value
        }
        return self

    def filter_custom(self, field_name: FilterField, val: MutableMapping):
        self._filters[field_name] = val
        return self

    def search(self, data: str):
        self._search = data
        return self

    def sort(self, *data: str):
        self._sort.extend(data)
        return self

    def limit(self, value: Literal[-1] or conint(gt=0)):
        self._limit = value
        return self

    def offset(self, value: conint(ge=0)):
        self._offset = value
        return self

    def page(self, value: conint(ge=1)):
        self._page = value
        return self

    def deep_custom(self, field_name: str, data: MutableMapping):
        self._deep[field_name] = data
        return self

    def meta(self, value: str):
        self._meta = value
        return self

    def __str__(self):
        res = {}
        if len(self._fields) != 0:
            res['fields'] = self._fields
        if len(self._filters.items()) != 0:
            res['filter'] = self._filters
        if self._search:
            res['search'] = self._search
        if len(self._sort) != 0:
            res['sort'] = self._sort
        if self._limit:
            res['limit'] = self._limit
        if self._offset:
            res['offset'] = self._offset
        if self._page:
            res['page'] = self._page
        if len(self._deep.items()) != 0:
            res['deep'] = self._deep
        if self._meta:
            res['meta'] = self._meta
        return res
