# authentication/schema.py
import graphene
from .queries import AuthQuery
from .mutations import AuthMutation

class Query(AuthQuery, graphene.ObjectType):
    pass

class Mutation(AuthMutation, graphene.ObjectType):
    pass
