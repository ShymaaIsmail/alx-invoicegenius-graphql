# authentication/queries.py
import graphene
from graphql_jwt.decorators import login_required
from .types import UserType

class AuthQuery(graphene.ObjectType):
    me = graphene.Field(UserType)

    @login_required
    def resolve_me(self, info):
        return info.context.user
