import io
import json
from types import SimpleNamespace
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from django.test import SimpleTestCase, override_settings
from rest_framework.exceptions import ValidationError

from brain.heart_client import dispatch_to_heart, get_heart_connection_info


class HeartDispatchTests(SimpleTestCase):
    @override_settings(
        HEART_EXECUTE_URL="   ",
        HEART_INTERNAL_TOKEN="",
        HEART_REQUEST_TIMEOUT_SECONDS=15,
    )
    def test_get_heart_connection_info_internal(self):
        info = get_heart_connection_info()

        self.assertEqual(info["mode"], "internal")
        self.assertIsNone(info["execute_url"])
        self.assertFalse(info["token_configured"])
        self.assertEqual(info["timeout_seconds"], 15)

    @override_settings(
        HEART_EXECUTE_URL="  https://heart.example.com/execute  ",
        HEART_INTERNAL_TOKEN="secret-token",
        HEART_REQUEST_TIMEOUT_SECONDS=30,
    )
    def test_get_heart_connection_info_external(self):
        info = get_heart_connection_info()

        self.assertEqual(info["mode"], "external")
        self.assertEqual(info["execute_url"], "https://heart.example.com/execute")
        self.assertTrue(info["token_configured"])
        self.assertEqual(info["timeout_seconds"], 30)

    @override_settings(HEART_EXECUTE_URL="", HEART_INTERNAL_TOKEN="")
    @patch("brain.heart_client.execute_internal_task")
    def test_dispatch_to_heart_uses_internal_when_no_url(self, mock_internal):
        data = SimpleNamespace(
            project_id=1,
            user_id=2,
            feature="feat",
            requested_engine="gpt",
            prompt="hello",
            metadata={"a": 1},
        )
        mock_internal.return_value = {"ok": True}

        result = dispatch_to_heart(data)

        self.assertEqual(result, {"ok": True})
        mock_internal.assert_called_once_with(data)

    @override_settings(
        HEART_EXECUTE_URL="https://heart.example.com/execute",
        HEART_INTERNAL_TOKEN="secret-token",
        HEART_REQUEST_TIMEOUT_SECONDS=12,
    )
    @patch("brain.heart_client.urllib.request.urlopen")
    def test_dispatch_to_heart_posts_json_and_returns_response(self, mock_urlopen):
        data = SimpleNamespace(
            project_id=1,
            user_id=2,
            feature="feat",
            requested_engine="gpt",
            prompt="hello",
            metadata={"a": 1},
        )

        response = Mock()
        response.read.return_value = json.dumps({"ok": True}).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = response

        result = dispatch_to_heart(data)

        self.assertEqual(result, {"ok": True})

        request = mock_urlopen.call_args.args[0]
        self.assertEqual(request.full_url, "https://heart.example.com/execute")

        sent_body = json.loads(request.data.decode("utf-8"))
        self.assertEqual(sent_body["project_id"], 1)
        self.assertEqual(sent_body["user_id"], 2)
        self.assertEqual(mock_urlopen.call_args.kwargs["timeout"], 12)

    @override_settings(HEART_EXECUTE_URL="https://heart.example.com/execute")
    @patch("brain.heart_client.urllib.request.urlopen")
    def test_dispatch_to_heart_http_error(self, mock_urlopen):
        data = SimpleNamespace(
            project_id=1,
            user_id=2,
            feature="feat",
            requested_engine="gpt",
            prompt="hello",
            metadata={},
        )

        mock_urlopen.side_effect = HTTPError(
            url="https://heart.example.com/execute",
            code=500,
            msg="Server Error",
            hdrs=None,
            fp=io.BytesIO(b"boom"),
        )

        with self.assertRaises(ValidationError) as ctx:
            dispatch_to_heart(data)

        self.assertIn("status=500", str(ctx.exception))
        self.assertIn("boom", str(ctx.exception))

    @override_settings(HEART_EXECUTE_URL="https://heart.example.com/execute")
    @patch("brain.heart_client.urllib.request.urlopen")
    def test_dispatch_to_heart_url_error(self, mock_urlopen):
        data = SimpleNamespace(
            project_id=1,
            user_id=2,
            feature="feat",
            requested_engine="gpt",
            prompt="hello",
            metadata={},
        )

        mock_urlopen.side_effect = URLError("no route")

        with self.assertRaises(ValidationError) as ctx:
            dispatch_to_heart(data)

        self.assertIn("could not reach Heart", str(ctx.exception))
        self.assertIn("no route", str(ctx.exception))

    @override_settings(HEART_EXECUTE_URL="https://heart.example.com/execute")
    @patch("brain.heart_client.urllib.request.urlopen")
    def test_dispatch_to_heart_timeout_error(self, mock_urlopen):
        data = SimpleNamespace(
            project_id=1,
            user_id=2,
            feature="feat",
            requested_engine="gpt",
            prompt="hello",
            metadata={},
        )

        mock_urlopen.side_effect = TimeoutError()

        with self.assertRaises(ValidationError) as ctx:
            dispatch_to_heart(data)

        self.assertIn("timed out", str(ctx.exception))
