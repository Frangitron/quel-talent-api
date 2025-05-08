from queltalentapi.components.authorization.abstract import AbstractAuthorization
from queltalentapi.components.http.user_claims import UserClaims


class NoAuthorization(AbstractAuthorization):

    def validate_token(self, token: str | None) -> UserClaims:
        return UserClaims(name='NoAuth')
