from enum import Enum


class EventBusEventType(Enum):
    Create = 0
    Update = 1
    Delete = 2
