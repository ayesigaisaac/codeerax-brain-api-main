from django.test import TestCase
from rest_framework.test import APIClient

from .builder import build_auth_engine
from .models import User
from .utils.auth import create_jwt_token
from .utils.logout import blacklist_token


class AuthEngineBuilderTests(TestCase):
    def test_build_auth_engine_merges_config_and_builds_heart_payload(self):
        result = build_auth_engine(
            {
                "app_name": "My Auth App",
                "theme": {"primary": "#0F172A"},
                "config": {"include_profile": True, "password_policy": {"min_length": 12}},
                "project_id": "project-123",
                "user_id": "user-123",
            }
        )

        self.assertEqual(result["status"], "queued")
        self.assertEqual(result["progress"], 0)
        self.assertEqual(result["progress_history"], [30, 70, 100])
        self.assertEqual(result["config"]["password_policy"]["min_length"], 12)
        self.assertIn("profile", result["engines"])

        heart_execute = result["heart_execute"]
        self.assertEqual(heart_execute.project_id, "project-123")
        self.assertEqual(heart_execute.requested_engine, "auth")
        self.assertEqual(heart_execute.metadata["app_name"], "My Auth App")
        self.assertEqual(heart_execute.metadata["config"]["preseed_admin"], False)


class JWTBlacklistAuthenticationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="blacklist@test.com",
            password="StrongPass1!",
            username="blacklist-user",
            is_active=True,
        )

    def test_me_endpoint_accepts_non_blacklisted_token(self):
        token = create_jwt_token(self.user)
        response = self.client.get("/auth/me/", HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["email"], self.user.email)

    def test_me_endpoint_rejects_blacklisted_token(self):
        token = create_jwt_token(self.user)
        blacklist_token(token)

        response = self.client.get("/auth/me/", HTTP_AUTHORIZATION=f"Bearer {token}")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["error"]["message"], "Token has been revoked.")
