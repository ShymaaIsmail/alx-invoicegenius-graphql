from django.test import TestCase
from ai_parser.utils import parse_invoice_text

class AIParserTest(TestCase):
    def test_parse_invoice_text(self):
        sample = "Invoice Number: 12345\nVendor: ACME\nTotal: $250.00"
        parsed = parse_invoice_text(sample)
        self.assertEqual(parsed.get("invoice_number"), "12345")


# authentication/tests/test_mutations.py
from graphene_django.utils.testing import GraphQLTestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

User = get_user_model()

class AuthMutationTest(GraphQLTestCase):
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

        self.assertIsNone(response.errors)
        data = response.json()["data"]["googleLogin"]
        self.assertEqual(data["email"], "testuser@example.com")
