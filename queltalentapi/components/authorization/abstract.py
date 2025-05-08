from abc import ABC, abstractmethod

from queltalentapi.components.http.user_claims import UserClaims


class AbstractAuthorization(ABC):

    @abstractmethod
    def validate_token(self, token: str | None) -> UserClaims:
        pass
