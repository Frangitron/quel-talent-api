from abc import ABC, abstractmethod

from queltalentapi.foundation.http.user_claims import UserClaims


class AbstractAuthorization(ABC):

    @abstractmethod
    def get_user_claims(self, token: str | None) -> UserClaims:
        pass
