"""
dlt source to load Zoom meeting and webinar data.
How to use it:
1. Create a server-to-server app: https://developers.zoom.us/docs/internal-apps/create/
2. Copy the account id, client id, and client secret into your secrets.toml
3. Add the required scopes to your app. This depends on which resources you want to load.
For example, user:read:list_users:admin, user:read:user:admin, report:read:list_meeting_participants:admin, webinar:read:list_webinars:admin

In case of errors: See the HTTP error responses, Zoom tells which scopes are missing in your app.
"""

from base64 import b64encode
from typing import (
    Any,
    Dict,
)

import dlt

from rest_api import RESTAPIConfig, rest_api_source
from rest_api.auth import OAuth2ImplicitFlow
from rest_api.paginators import JSONResponseCursorPaginator


class OAuth2Zoom(OAuth2ImplicitFlow):
    def build_access_token_request(self) -> Dict[str, Any]:
        authentication: str = b64encode(
            f"{self.client_id}:{self.client_secret}".encode()
        ).decode()
        return {
            "url": "https://zoom.us/oauth/token",
            "headers": {
                "Authorization": f"Basic {authentication}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            "data": self.access_token_request_data,
        }


resolve_meeting_id = {
    "meeting_id": {
        "type": "resolve",
        "resource": "meetings",
        "field": "id",
    }
}

resolve_user_id = {
    "user_id": {
        "type": "resolve",
        "resource": "users",
        "field": "id",
    }
}

resolve_webinar_id = {
    "webinar_id": {
        "type": "resolve",
        "resource": "webinars",
        "field": "id",
    }
}

config: RESTAPIConfig = {
    "client": {
        "base_url": "https://api.zoom.us/v2",
        "auth": OAuth2Zoom(
            access_token_request_data={
                "grant_type": "account_credentials",
                "account_id": dlt.secrets["sources.zoom.account_id"],
            },
            client_id=dlt.secrets["sources.zoom.client_id"],
            client_secret=dlt.secrets["sources.zoom.client_secret"],
        ),
        "paginator": JSONResponseCursorPaginator(
            cursor_path="response.next_page_token",
            cursor_param="page_number",
        ),
    },
    "resources": [
        "users",
        # Meetings
        {
            "name": "meetings",
            "endpoint": {
                "path": "users/{user_id}/meetings",
                "params": resolve_user_id,
            },
        },
        {
            "name": "meeting_registrants",
            "endpoint": {
                "path": "/meetings/{meeting_id}/registrants",
                "params": resolve_meeting_id,
                "response_actions": [
                    {
                        "content": "Registration has not been enabled for this meeting",
                        "action": "ignore",
                    },
                ],
            },
        },
        {
            "name": "meeting_polls",
            "endpoint": {
                "path": "/meetings/{meeting_id}/polls",
                "params": resolve_meeting_id,
                "response_actions": [
                    {"status_code": 400, "action": "ignore"},
                ],
            },
        },
        {
            "name": "meeting_polls_results",
            "endpoint": {
                "path": "/past_meetings/{meeting_id}/polls",
                "params": resolve_meeting_id,
                "response_actions": [
                    {"status_code": 400, "action": "ignore"},
                    {"status_code": 404, "action": "ignore"},
                ],
            },
        },
        {
            "name": "meeting_registration_questions",
            "endpoint": {
                "path": "/meetings/{meeting_id}/registrants/questions",
                "params": resolve_meeting_id,
                "response_actions": [
                    {
                        "content": "Registration has not been enabled for this meeting",
                        "action": "ignore",
                    },
                ],
            },
        },
        # Webinars
        {
            "name": "webinars",
            "endpoint": {
                "path": "/users/{user_id}/webinars",
                "params": resolve_user_id,
                "response_actions": [
                    {"content": "Webinar plan is missing", "action": "ignore"},
                ],
            },
        },
        {
            "name": "webinar_panelists",
            "endpoint": {
                "path": "/webinars/{webinar_id}/panelists",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_registrants",
            "endpoint": {
                "path": "/webinars/{webinar_id}/registrants",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_absentees",
            "endpoint": {
                "path": "/past_webinars/{webinar_id}/absentees",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_polls",
            "endpoint": {
                "path": "/webinars/{webinar_id}/polls",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_poll_results",
            "endpoint": {
                "path": "/past_webinars/{webinar_id}/polls",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_registration_questions",
            "endpoint": {
                "path": "/webinars/{webinar_id}/registrants/questions",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_tracking_sources",
            "endpoint": {
                "path": "/webinars/{webinar_id}/tracking_sources",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_qa",
            "endpoint": {
                "path": "/past_webinars/{webinar_id}/qa",
                "params": resolve_webinar_id,
            },
        },
        # Reports
        {
            "name": "meetings_report",
            "endpoint": {
                "path": "/report/users/{user_id}/meetings",
                "params": resolve_user_id,
            },
        },
        {
            "name": "meeting_participants_report",
            "endpoint": {
                "path": "/report/meetings/{meeting_id}/participants",
                "params": resolve_meeting_id,
                "response_actions": [
                    {"status_code": 404, "action": "ignore"},
                ],
            },
        },
        {
            "name": "webinar_details_report",
            "endpoint": {
                "path": "/report/webinars/{webinar_id}",
                "params": resolve_webinar_id,
            },
        },
        {
            "name": "webinar_participants_report",
            "endpoint": {
                "path": "/report/webinars/{webinar_id}/participants",
                "params": resolve_webinar_id,
            },
        },
    ],
}

source = rest_api_source(config)
