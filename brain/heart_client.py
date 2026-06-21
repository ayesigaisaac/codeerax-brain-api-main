import json
import urllib.error
import urllib.request

from django.conf import settings
from rest_framework.exceptions import ValidationError

from heart.schemas import HeartExecuteSchema
from heart.services import execute_internal_task


def get_heart_connection_info() -> dict:
    execute_url = getattr(settings, "HEART_EXECUTE_URL", "").strip()
    return {
        "mode": "external" if execute_url else "internal",
        "execute_url": execute_url or None,
        "token_configured": bool(getattr(settings, "HEART_INTERNAL_TOKEN", "").strip()),
        "timeout_seconds": int(getattr(settings, "HEART_REQUEST_TIMEOUT_SECONDS", 15)),
    }


def dispatch_to_heart(data: HeartExecuteSchema):
    connection_info = get_heart_connection_info()
    execute_url = connection_info["execute_url"]

    if not execute_url:
        return execute_internal_task(data)

    payload = json.dumps(
        {
            "project_id": data.project_id,
            "user_id": data.user_id,
            "feature": data.feature,
            "requested_engine": data.requested_engine,
            "prompt": data.prompt,
            "metadata": data.metadata,
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        execute_url,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "X-Internal-Token": getattr(settings, "HEART_INTERNAL_TOKEN", ""),
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(
            request,
            timeout=connection_info["timeout_seconds"],
        ) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="replace")
        raise ValidationError(
            {
                "heart": (
                    "Heart returned an error while processing this task. "
                    f"status={exc.code} body={response_body}"
                )
            }
        )
    except urllib.error.URLError as exc:
        raise ValidationError(
            {
                "heart": (
                    "Brain could not reach Heart. "
                    f"url={execute_url} reason={exc.reason}"
                )
            }
        )
    except TimeoutError:
        raise ValidationError(
            {
                "heart": (
                    "Brain timed out while waiting for Heart. "
                    f"url={execute_url} timeout={connection_info['timeout_seconds']}s"
                )
            }
        )

