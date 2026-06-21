from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from brain.build_store import set_task

User = get_user_model()


def _make_user(email, password="testpass123"):
    return User.objects.create_user(
        email=email,
        password=password,
        username=email.split("@")[0],
    )


def _auth_header(client, user, password="testpass123"):
    resp = client.post(
        "/auth/login/",
        {"email": user.email, "password": password},
        format="json",
    )
    token = resp.data.get("token")
    return {"HTTP_AUTHORIZATION": f"Bearer {token}"}


class BuildStatusOwnershipTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = _make_user("owner@example.com")
        self.other = _make_user("other@example.com")

    def _seed_task(self, task_id, user_id):
        set_task(task_id, {
            "task_id": task_id,
            "project_id": "proj-1",
            "user_id": str(user_id),
            "requested_engine": "auth",
            "status": "completed",
            "progress": 100,
            "progress_history": [],
            "message": "Done.",
            "config": {},
            "engines": ["auth"],
            "heart_status": "completed",
            "runtime_url": "/runtime/proj-1/",
        })

    def test_unauthenticated_request_is_rejected(self):
        self._seed_task("task-unauth-1", self.owner.id)
        resp = self.client.get("/brain/build/status/task-unauth-1/")
        self.assertEqual(resp.status_code, 401)

    def test_owner_can_access_their_task(self):
        self._seed_task("task-owner-1", self.owner.id)
        headers = _auth_header(self.client, self.owner)
        resp = self.client.get("/brain/build/status/task-owner-1/", **headers)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data["task_id"], "task-owner-1")

    def test_other_user_cannot_access_task(self):
        self._seed_task("task-owner-2", self.owner.id)
        headers = _auth_header(self.client, self.other)
        resp = self.client.get("/brain/build/status/task-owner-2/", **headers)
        self.assertEqual(resp.status_code, 404)

    def test_task_with_no_user_id_is_accessible_by_any_authenticated_user(self):
        set_task("task-anon-1", {
            "task_id": "task-anon-1",
            "project_id": "proj-anon",
            "user_id": "",
            "requested_engine": "dashboard",
            "status": "completed",
            "progress": 100,
            "progress_history": [],
            "message": "Done.",
            "config": {},
            "engines": ["dashboard"],
            "heart_status": "completed",
            "runtime_url": "/runtime/proj-anon/",
        })
        headers = _auth_header(self.client, self.other)
        resp = self.client.get("/brain/build/status/task-anon-1/", **headers)
        self.assertEqual(resp.status_code, 200)

    @patch("brain.services.dispatch_to_heart")
    def test_build_task_is_tied_to_authenticated_user(self, mock_dispatch):
        mock_dispatch.return_value = {"status": "completed", "runtime_url": "/runtime/test/"}
        headers = _auth_header(self.client, self.owner)

        resp = self.client.post(
            "/brain/build/",
            {"prompt": "Build a dashboard with analytics", "feature": "dashboard"},
            format="json",
            **headers,
        )
        self.assertEqual(resp.status_code, 202)
        task_id = resp.data.get("task_id")
        self.assertIsNotNone(task_id)

        # Owner can poll
        status_resp = self.client.get(f"/brain/build/status/{task_id}/", **headers)
        self.assertEqual(status_resp.status_code, 200)

        # Other user gets 404
        other_headers = _auth_header(self.client, self.other)
        blocked_resp = self.client.get(f"/brain/build/status/{task_id}/", **other_headers)
        self.assertEqual(blocked_resp.status_code, 404)
