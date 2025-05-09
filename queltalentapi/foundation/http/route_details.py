from dataclasses import dataclass

from queltalentapi.foundation.http.methods import HttpMethods


@dataclass()
class RouteDetails:
    method: HttpMethods
    name: str
    operation_id: str
    path: str
