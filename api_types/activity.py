from datetime import datetime
from typing import Literal, Optional, Callable, List

from pydantic import BaseModel, constr, conint, IPvAnyAddress, UUID4


class ActivityObject(BaseModel):
    """
    All events that within Directus are tracked and stored in the activities collection.
    This gives you full accountability over everything that happens.
    https://docs.directus.io/concepts/activity/
    """
    action: str  # Action that was performed.
    collection: constr(min_length=1)  # Collection identifier in which the item resides.
    # User comment. This will store the comments show up in the right sidebar of the item edit page in the admin app.
    comment: Optional[str] = None
    id: conint(ge=0)  # Unique identifier for the object.
    ip: IPvAnyAddress  # The IP address of the user at the time the action took place.
    # Unique identifier for the item the action applied to. This is always a string, even for integer primary keys.
    item: str
    timestamp: datetime  # When the action happened.
    user: UUID4  # The user who performed this action. Many-to-one to users.
    user_agent: str  # User agent string of the browser the user used when the action took place.
    revisions: list  # Any changes that were made in this activity. One-to-many to revisions.


class ActivityList(BaseModel):
    data: List[ActivityObject]


class ActivitySingle(BaseModel):
    data: ActivityObject


class ActivityAction(BaseModel):
    list: Callable[[], ActivityList]
    list_by_id: Callable[[constr(min_length=1)], ActivitySingle]
