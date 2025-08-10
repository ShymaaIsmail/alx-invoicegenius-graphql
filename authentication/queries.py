import graphene
from graphql_jwt.decorators import login_required
from .types import UserType


class AuthQuery(graphene.ObjectType):
    """
    Authentication-related GraphQL queries.

    Currently provides:
    - `me`: Returns information about the currently authenticated user.
    """

    me = graphene.Field(
        UserType,
        description=(
            "Return details of the currently authenticated user. "
            "Requires a valid JWT access token."
        )
    )

    @login_required
    def resolve_me(self, info):
        """
        Resolve the `me` query.

        Returns:
            UserType: The user object for the authenticated request.
        """
        return info.context.user
