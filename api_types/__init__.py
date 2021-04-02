from typing import Literal as _Literal
from .activity import ActivityObject, ActivityList, ActivityAction, ActivitySingle

methods = _Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE', 'HEAD', 'OPTION']
