# authentication/mutations.py
import graphene
import graphql_jwt
from django.contrib.auth import get_user_model
from graphql_jwt.refresh_token.shortcuts import create_refresh_token
from graphql_jwt.refresh_token.models import RefreshToken
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import jwt_encode
from google.oauth2 import id_token as google_id_token
from google.auth.transport import requests as google_requests
from django.conf import settings

User = get_user_model()

# Helper
def generate_token(user):
    payload = jwt_settings.JWT_PAYLOAD_HANDLER(user)
    return jwt_encode(payload)


class GoogleLogin(graphene.Mutation):
    class Arguments:
        id_token_str = graphene.String(required=True)

    token = graphene.String()
    refresh_token = graphene.String()
    username = graphene.String()
    user_id = graphene.ID()
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()

    def mutate(self, info, id_token_str):
        try:
            idinfo = google_id_token.verify_oauth2_token(
                id_token_str, google_requests.Request(), settings.GOOGLE_CLIENT_ID
            )

            email = idinfo.get("email")
            name = idinfo.get("name")

            user, _ = User.objects.get_or_create(
                email=email,
                defaults={
                    "username": email.split("@")[0],
                    "first_name": name.split()[0] if name else "",
                    "last_name": " ".join(name.split()[1:]) if name else "",
                },
            )

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
    success = graphene.Boolean()

    class Arguments:
        refresh_token = graphene.String(required=True)

    def mutate(self, info, refresh_token):
        try:
            token = RefreshToken.objects.get(token=refresh_token)
            token.revoke()
            return Logout(success=True)
        except RefreshToken.DoesNotExist:
            return Logout(success=False)


class AuthMutation(graphene.ObjectType):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    revoke_token = graphql_jwt.Revoke.Field()
    google_login = GoogleLogin.Field()
    logout = Logout.Field()
