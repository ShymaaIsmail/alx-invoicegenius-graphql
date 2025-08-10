import graphene
import graphql_jwt

from django.conf import settings
from django.contrib.auth import get_user_model
from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import jwt_encode

from google.auth.transport import requests as google_requests
from google.oauth2 import id_token as google_id_token

User = get_user_model()


# Helper to generate token using the current JWT settings
def generate_token(user):
    """Generate a JWT access token for the given user."""
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    return jwt_encode(payload)


class GoogleLogin(graphene.Mutation):
    """
    Log in a user using a Google ID token.

    This mutation:
    - Verifies the provided Google ID token against your app's `GOOGLE_CLIENT_ID`.
    - Creates a new user account if one doesn't already exist for the Google account.
    - Returns an access token and refresh token for authenticated requests.
    """

    class Arguments:
        id_token_str = graphene.String(
            required=True,
            description=(
                "The Google ID token obtained from the Google Sign-In flow. "
                "Must be verified against your configured Google client ID."
            )
        )

    token = graphene.String(description="JWT access token for authenticated API calls.")
    refresh_token = graphene.String(description="JWT refresh token for obtaining new access tokens.")
    username = graphene.String(description="The username of the authenticated user.")
    user_id = graphene.ID(description="The unique database ID of the user.")
    email = graphene.String(description="The email address of the authenticated user.")
    first_name = graphene.String(description="The first name of the user.")
    last_name = graphene.String(description="The last name of the user.")

    @classmethod
    def mutate(cls, root, info, id_token_str):
        """Authenticate a user with Google and return tokens and profile information."""
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name")

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "first_name": name.split()[0] if name else "",
                    "last_name": " ".join(name.split()[1:]) if name else "",
                },
            )

            if created:
                user.set_unusable_password()
                user.save()

            token = generate_token(user)
            refresh_token = create_refresh_token(user)

            return GoogleLogin(
                token=token,
                refresh_token=refresh_token.token,
                username=user.username,
                user_id=user.id,
                email=user.email,
                first_name=user.first_name,
                last_name=user.last_name,
            )

        except ValueError:
            raise Exception("Invalid Google ID token")


class Logout(graphene.Mutation):
    """
    Log out a user by revoking their refresh token.

    This mutation invalidates the provided refresh token so it can no longer be used
    to obtain new access tokens.
    """
    success = graphene.Boolean(description="True if the token was successfully revoked.")

    class Arguments:
        refresh_token = graphene.String(
            required=True,
            description="The refresh token to revoke."
        )

    @classmethod
    def mutate(cls, root, info, refresh_token):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.revoke()
            return Logout(success=True)
        except RefreshToken.DoesNotExist:
            return Logout(success=False)


class AuthMutation(graphene.ObjectType):
    """
    Root authentication mutations for the InvoiceGenius GraphQL API.

    Provides:
    - Standard JWT authentication (obtain, verify, refresh, revoke)
    - Google login integration
    - Token-based logout
    """
    token_auth = graphql_jwt.ObtainJSONWebToken.Field(
        description="Authenticate with username and password to obtain a JWT token."
    )
    verify_token = graphql_jwt.Verify.Field(
        description="Verify the validity of a JWT token."
    )
    refresh_token = graphql_jwt.Refresh.Field(
        description="Obtain a new access token using a valid refresh token."
    )
    revoke_token = graphql_jwt.Revoke.Field(
        description="Revoke a refresh token to prevent further use."
    )
    google_login = GoogleLogin.Field(
        description="Log in using a Google ID token."
    )
    logout = Logout.Field(
        description="Log out by revoking the given refresh token."
    )
