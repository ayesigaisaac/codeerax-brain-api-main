from django.test import TestCase, override_settings
from rest_framework.test import APIClient


class HeartExecuteSecurityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.payload = {
            "project_id": "project-sec-1",
            "requested_engine": "auth",
            "prompt": "Build authentication flow",
        }

    def assert_structured_error(self, response, expected_status_code, expected_message):
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data["success"], False)
        self.assertEqual(response.data["error"]["message"], expected_message)
        self.assertIn("type", response.data["error"])
        self.assertIn("code", response.data["error"])
        self.assertIn("details", response.data["error"])

    @override_settings(DEBUG=False, HEART_INTERNAL_TOKEN="")
    def test_execute_rejects_when_token_not_configured_in_production(self):
        response = self.client.post("/internal/execute/", self.payload, format="json")

        self.assert_structured_error(
            response,
            503,
            "Server misconfiguration: HEART_INTERNAL_TOKEN is required.",
        )

    @override_settings(DEBUG=False, HEART_INTERNAL_TOKEN="heart-secret")
    def test_execute_rejects_missing_request_token_in_production(self):
        response = self.client.post("/internal/execute/", self.payload, format="json")

        self.assert_structured_error(
            response,
            403,
            "X-Internal-Token header is required.",
        )

    @override_settings(DEBUG=False, HEART_INTERNAL_TOKEN="heart-secret")
    def test_execute_rejects_invalid_request_token(self):
        response = self.client.post(
            "/internal/execute/",
            self.payload,
            format="json",
            HTTP_X_INTERNAL_TOKEN="wrong-secret",
        )

        self.assert_structured_error(response, 403, "Invalid internal token.")

    @override_settings(DEBUG=False, HEART_INTERNAL_TOKEN="heart-secret")
    def test_execute_accepts_valid_request_token(self):
        response = self.client.post(
            "/internal/execute/",
            self.payload,
            format="json",
            HTTP_X_INTERNAL_TOKEN="heart-secret",
        )

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["project_id"], self.payload["project_id"])

    @override_settings(DEBUG=True, HEART_INTERNAL_TOKEN="")
    def test_execute_allows_missing_token_in_debug_mode(self):
        # In debug mode with no internal token set, enforcement is disabled.
        response = self.client.post("/internal/execute/", self.payload, format="json")

        self.assertEqual(response.status_code, 202)
        
