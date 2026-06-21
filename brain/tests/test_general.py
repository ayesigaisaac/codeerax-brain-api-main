import json
import uuid
from unittest.mock import MagicMock, patch

from django.test import TestCase, override_settings
from rest_framework.test import APIClient

class BrainApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health_reports_internal_mode_when_no_external_url(self):
        response = self.client.get("/brain/health/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["service"], "brain")
        self.assertEqual(response.data["heart_connection"]["mode"], "internal")

    def test_build_chooses_dashboard_engine_from_prompt_keywords(self):
        payload = {"prompt": "Build an analytics dashboard with charts and activity"}
        response = self.client.post("/brain/build/", payload, format="json")

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["requested_engine"], "dashboard")
        self.assertEqual(response.data["heart_status"], "completed")
        self.assertIn("/runtime/", response.data["runtime_url"])

    @override_settings(
        HEART_EXECUTE_URL="https://heart.example/internal/execute/",
        HEART_INTERNAL_TOKEN="brain-heart-token",
        HEART_REQUEST_TIMEOUT_SECONDS=9,
    )
    @patch("brain.heart_client.urllib.request.urlopen")
    def test_build_dispatches_to_external_heart_when_url_configured(self, mock_urlopen):
        fake_response = MagicMock()
        fake_response.read.return_value = json.dumps(
            {
                "project_id": "p-123",
                "status": "queued",
                "runtime_url": "/runtime/p-123/",
                "runtime_data": {"ok": True},
            }
        ).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = fake_response

        payload = {
            "project_id": "p-123",
            "prompt": "Create profile setup flow",
            "requested_engine": "profile",
        }
        response = self.client.post("/brain/build/", payload, format="json")

        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.data["requested_engine"], "profile")
        self.assertEqual(response.data["heart_status"], "queued")
        self.assertEqual(response.data["runtime_url"], "/runtime/p-123/")

        self.assertTrue(mock_urlopen.called)
        _, kwargs = mock_urlopen.call_args
        self.assertEqual(kwargs["timeout"], 9)



class BrainToHeartIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_build_then_fetch_runtime_end_to_end(self):
        project_id = str(uuid.uuid4())
        payload = {
            "project_id": project_id,
            "prompt": "Build a dashboard with analytics cards and activity feed",
            "feature": "dashboard",
        }

        build_response = self.client.post("/brain/build/", payload, format="json")
        self.assertEqual(build_response.status_code, 202)
        self.assertEqual(build_response.data["project_id"], project_id)
        self.assertEqual(build_response.data["requested_engine"], "dashboard")
        self.assertEqual(build_response.data["heart_status"], "completed")

        runtime_url = build_response.data["runtime_url"]
        runtime_response = self.client.get(runtime_url)
        self.assertEqual(runtime_response.status_code, 200)

        self.assertEqual(runtime_response.data["project_id"], project_id)
        self.assertEqual(runtime_response.data["status"], "completed")
        self.assertEqual(runtime_response.data["requested_engine"], "dashboard")
        self.assertEqual(
            runtime_response.data["runtime_data"]["engine"],
            "dashboard",
        )
        self.assertEqual(
            runtime_response.data["runtime_data"]["status"],
            "completed",
        )

    @patch("brain.services.dispatch_to_heart")
    def test_build_generic_flow_returns_502_on_dispatch_error(self, mock_dispatch):
        """Verify generic flow dispatch errors return 502 BAD_GATEWAY with status=failed"""
        mock_dispatch.side_effect = RuntimeError("Heart dispatch failed")

        payload = {
            "prompt": "Build something",
            "requested_engine": "generic",
        }

        response = self.client.post("/brain/build/", payload, format="json")

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.data["status"], "failed")
        self.assertEqual(response.data["heart_status"], "failed")
        self.assertEqual(response.data["runtime_url"], "")
        self.assertIn("failed", response.data["message"].lower())

