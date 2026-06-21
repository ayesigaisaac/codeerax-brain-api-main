import uuid

from django.test import TestCase
from rest_framework.test import APIClient


class StructuredApiErrorFormatTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def assert_structured_error(self, response, expected_status_code):
        self.assertEqual(response.status_code, expected_status_code)
        self.assertEqual(response.data["success"], False)
        self.assertIn("error", response.data)
        self.assertIn("type", response.data["error"])
        self.assertIn("code", response.data["error"])
        self.assertIn("message", response.data["error"])
        self.assertIn("details", response.data["error"])

    def test_brain_serializer_error_is_structured(self):
        response = self.client.post("/brain/build/", {}, format="json")
        self.assert_structured_error(response, 400)

    def test_auth_verify_email_error_is_structured(self):
        response = self.client.get("/auth/verify-email/")
        self.assert_structured_error(response, 400)

    def test_profile_public_error_is_structured(self):
        response = self.client.get(f"/profile/public/{uuid.uuid4()}/")
        self.assert_structured_error(response, 400)

    def test_heart_runtime_not_found_error_is_structured(self):
        response = self.client.get("/runtime/non-existent-project-id/")
        self.assert_structured_error(response, 400)


class ApiDocsTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_openapi_schema_endpoint_is_available(self):
        response = self.client.get("/api/schema/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("openapi", response.data)

    def test_swagger_ui_endpoint_is_available(self):
        response = self.client.get("/api/docs/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("swagger-ui", response.content.decode("utf-8"))

    def test_dashboard_endpoint_is_available(self):
        response = self.client.get("/dashboard/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("display_name", response.data)
