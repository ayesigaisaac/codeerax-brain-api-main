import json
from unittest.mock import patch

from django.test import TestCase
from rest_framework.test import APIClient

from engines.auth_engine.builder import build_auth_engine
from brain.serializers import AuthEngineBuildSerializer


class AuthEngineBuildSerializerTests(TestCase):
    def test_serializer_accepts_valid_payload(self):
        serializer = AuthEngineBuildSerializer(
            data={
                "app_name": "My Auth App",
                "theme": {"primary": "#7C3AED"},
                "config": {"preseed_admin": True},
                "project_id": "project-1",
                "user_id": "user-1",
            }
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data["app_name"], "My Auth App")

    def test_serializer_rejects_blank_app_name(self):
        serializer = AuthEngineBuildSerializer(data={"app_name": "   "})

        self.assertFalse(serializer.is_valid())
        self.assertIn("app_name", serializer.errors)


class AuthBuilderTests(TestCase):
    def test_build_auth_engine_returns_expected_structure(self):
        input_data = {
            "app_name": "Test App",
            "theme": {"primary": "#7C3AED"},
            "config": {"password_policy": {"min_length": 10}, "include_profile": True},
        }

        result = build_auth_engine(input_data)

        # Basic keys
        self.assertIn("task_id", result)
        self.assertIn("status", result)
        self.assertIn("progress", result)
        self.assertIn("config", result)
        self.assertIn("engines", result)
        self.assertIn("heart_execute", result)
        self.assertEqual(result["status"], "queued")
        self.assertEqual(result["progress"], 0)

        # Config merging happened
        self.assertEqual(result["config"]["password_policy"]["min_length"], 10)
        # include_profile should add profile engine
        self.assertIn("profile", result["engines"])
        self.assertEqual(result["progress_history"], [30, 70, 100])


class BrainAuthFlowIntegrationTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("brain.services.update_task")
    @patch("brain.services.set_task")
    @patch("brain.services.dispatch_to_heart")
    def test_brain_build_auth_calls_builder_and_dispatches(self, mock_dispatch, mock_set_task, mock_update_task):
        mock_dispatch.return_value = {"status": "completed", "runtime_url": "/runtime/test/"}

        payload = {
            "prompt": "Build auth",
            "requested_engine": "auth",
            "metadata": {"app_name": "MyAuthApp", "config": {"preseed_admin": True}},
        }

        response = self.client.post("/brain/build/", payload, format="json")

        self.assertEqual(response.status_code, 202)
        data = response.data

        # Response should include builder metadata
        self.assertIn("task_id", data)
        self.assertIn("status", data)
        self.assertIn("progress", data)
        self.assertIn("config", data)
        self.assertIn("engines", data)

        # Ensure dispatch_to_heart was used
        self.assertTrue(mock_dispatch.called)
        self.assertTrue(mock_set_task.called)
        self.assertGreaterEqual(mock_update_task.call_count, 2)

        first_update = mock_update_task.call_args_list[0].args[1]
        self.assertEqual(first_update["status"], "in_progress")
        self.assertEqual(first_update["progress"], 30)

        last_update = mock_update_task.call_args_list[-1].args[1]
        self.assertEqual(last_update["status"], "completed")
        self.assertEqual(last_update["progress"], 100)

    @patch("brain.services.dispatch_to_heart")
    def test_dedicated_auth_endpoint_and_status_polling(self, mock_dispatch):
        mock_dispatch.return_value = {"status": "completed", "runtime_url": "/runtime/test/"}

        payload = {
            "app_name": "MyAuthApp",
            "theme": {"primary": "#7C3AED"},
            "config": {"preseed_admin": True},
        }

        response = self.client.post("/brain/build/auth/", payload, format="json")

        self.assertEqual(response.status_code, 202)
        data = response.data
        task_id = data.get("task_id")
        self.assertIsNotNone(task_id)

        # Poll status endpoint
        status_resp = self.client.get(f"/brain/build/status/{task_id}/")
        self.assertEqual(status_resp.status_code, 200)
        status_data = status_resp.data
        self.assertEqual(status_data.get("task_id"), task_id)
        self.assertIn("progress", status_data)
        self.assertEqual(status_data.get("status"), "completed")

    @patch("brain.services.update_task")
    @patch("brain.services.set_task")
    @patch("brain.services.dispatch_to_heart")
    def test_brain_build_auth_marks_failed_when_dispatch_errors(self, mock_dispatch, mock_set_task, mock_update_task):
        mock_dispatch.side_effect = RuntimeError("Heart dispatch failed")

        payload = {
            "prompt": "Build auth",
            "requested_engine": "auth",
            "metadata": {"app_name": "MyAuthApp", "config": {"preseed_admin": True}},
        }

        response = self.client.post("/brain/build/", payload, format="json")

        self.assertEqual(response.status_code, 502)
        data = response.data
        self.assertEqual(data["status"], "failed")
        self.assertEqual(data["heart_status"], "failed")
        self.assertNotIn("error_message", data)
        self.assertTrue(mock_set_task.called)
        self.assertGreaterEqual(mock_update_task.call_count, 2)

        last_update = mock_update_task.call_args_list[-1].args[1]
        self.assertEqual(last_update["status"], "failed")
        self.assertEqual(last_update["error_message"], "Heart dispatch failed")
