# authentication/queries.py
import graphene
from graphql_jwt.decorators import login_required
from .types import UserType

class AuthQuery(graphene.ObjectType):
    """Authentication queries for the GraphQL API."""
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        """Resolve the 'me' query to return the currently authenticated user."""
        print("Resolving 'me' query for user:", info.context.user)
        return info.context.user
