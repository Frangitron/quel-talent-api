from dataclasses import dataclass


@dataclass()
class RouteDetails:
    path: str
    method: str
