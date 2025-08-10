import graphene
from .queries import AuthQuery
from .mutations import AuthMutation


class Query(AuthQuery, graphene.ObjectType):
    """
    Root query for authentication-related operations.

    Includes:
    - `me`: Get the currently authenticated user's profile information.
    """
    pass


class Mutation(AuthMutation, graphene.ObjectType):
    """
    Root mutation for authentication-related operations.

    Includes:
    - Standard JWT authentication (obtain, verify, refresh, revoke)
    - Google login
    - Logout
    """
    pass


schema = graphene.Schema(
    query=Query,
    mutation=Mutation,
)
