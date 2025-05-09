from dataclasses import dataclass

from queltalentapi.foundation.http.method_enum import HttpMethod


@dataclass()
class RouteDetails:
    method: HttpMethod
    name: str
    operation_id: str
    path: str
