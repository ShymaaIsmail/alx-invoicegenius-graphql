# authentication/types.py
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

User = get_user_model()

class UserType(DjangoObjectType):
    """GraphQL type for the User model."""
    class Meta:
        model = User
        fields = ("id", "username", "email", "first_name", "last_name")
