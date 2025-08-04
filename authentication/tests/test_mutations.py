from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class AuthMutationTest(GraphQLTestCase):
    GRAPHQL_URL = "/graphql/"  # Set your actual GraphQL endpoint here

    @patch("authentication.mutations.google_id_token.verify_oauth2_token")
    def test_google_login_success(self, mock_verify):
        mock_verify.return_value = {
            "email": "testuser@example.com",
            "name": "Test User",
            "sub": "google123"
        }

        response = self.query(
            """
            mutation GoogleLogin($token: String!) {
              googleLogin(idTokenStr: $token) {
                token
                username
                email
              }
            }
            """,
            variables={"token": "fake_token_value"},
        )

        self.assertEqual(response.status_code, 200)
        content = response.json()
        self.assertNotIn("errors", content)

        data = content["data"]["googleLogin"]
        self.assertEqual(data["email"], "testuser@example.com")
