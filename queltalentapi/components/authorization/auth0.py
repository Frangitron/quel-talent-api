import os
import base64

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import jwt

import requests

from httpapifoundation.authorization.abstract import AbstractAuthorization
from httpapifoundation.http.user_claims import UserClaims


class Auth0Authorization(AbstractAuthorization):
    def __init__(self):
        self.json_web_token_keys = requests.get(
            f"https://{os.getenv('AUTH_DOMAIN')}/{os.getenv('AUTH_JWKS_ENDPOINT')}"
        ).json()['keys']

    def get_user_claims(self, token: str | None) -> UserClaims:
        audience = os.getenv('AUTH_AUDIENCE')
        unverified_header = jwt.get_unverified_header(token)
        key_id = unverified_header.get("kid")
        if not key_id:
            raise ValueError("Token is missing 'kid' in header")

        public_key = self._find_public_key(key_id)
        if not public_key:
            raise ValueError(f"No matching public key found for kid {key_id}")

        decoded_token = jwt.decode(
            jwt=token,
            key=self._jwk_to_pem(public_key),
            algorithms=["RS256"],
            audience=audience,
            options={"verify_exp": True}
        )

        return UserClaims(
            name=decoded_token['sub'],
            #permissions=decoded_token['permissions']
        )

    def _jwk_to_pem(self, jwk):
        """
        Convert a JWK (JSON Web Key) to PEM format.
        """
        if jwk.get("kty") != "RSA":
            raise ValueError("Only 'RSA' keys are supported")

        # Initialize an RSA public key from the JWK
        public_key = rsa.RSAPublicNumbers(
            e=int.from_bytes(self._base64url_decode(jwk["e"]), "big"),
            n=int.from_bytes(self._base64url_decode(jwk["n"]), "big"),
        ).public_key(default_backend())

        # Convert the key to PEM format
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem

    def _find_public_key(self, key_id: str):
        for key in self.json_web_token_keys:
            if key['kid'] == key_id:
                return key
            return None

        return None

    @staticmethod
    def _base64url_decode(input_data):
        """
        Decodes Base64URL-encoded strings, adding necessary padding.
        """
        # Add padding if necessary
        padding = "=" * (4 - (len(input_data) % 4))
        return base64.urlsafe_b64decode(input_data + padding)
