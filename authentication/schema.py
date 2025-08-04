# authentication/schema.py
import graphene
from .queries import AuthQuery
from .mutations import AuthMutation

class Query(AuthQuery, graphene.ObjectType):
    """Root query for the GraphQL API."""
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    """Root mutation for the GraphQL API."""
    pass
