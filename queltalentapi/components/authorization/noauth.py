from queltalentapi.foundation.authorization.abstract import AbstractAuthorization
from queltalentapi.foundation.http.user_claims import UserClaims


class NoAuthorization(AbstractAuthorization):

    def get_user_claims(self, token: str | None) -> UserClaims:
        return UserClaims(name='NoAuth')
