from typing import Dict, List, Any, Optional
from datetime import datetime
from .client import NotiBoostClient


class EventsClient:
    def __init__(self, client: NotiBoostClient):
        self.client = client

    def ingest(self, event: Dict[str, Any]) -> Dict[str, Any]:
        if 'occurred_at' not in event:
            event['occurred_at'] = datetime.now().isoformat()
        return self.client.request('POST', '/api/v1/events', event)

    def ingest_batch(self, events: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/events/batch', {'events': events})


class UsersClient:
    def __init__(self, client: NotiBoostClient):
        self.client = client

    def create(self, user: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/users', user)

    def get(self, user_id: str) -> Dict[str, Any]:
        return self.client.request('GET', f'/api/v1/users/{user_id}')

    def update(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('PUT', f'/api/v1/users/{user_id}', data)

    def delete(self, user_id: str) -> Dict[str, Any]:
        return self.client.request('DELETE', f'/api/v1/users/{user_id}')

    def set_channel_data(self, user_id: str, channel_data: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('PUT', f'/api/v1/users/{user_id}/channel_data', channel_data)

    def set_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('PUT', f'/api/v1/users/{user_id}/preferences', preferences)

    def create_batch(self, users: List[Dict[str, Any]]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/users/batch', {'users': users})


class FlowsClient:
    def __init__(self, client: NotiBoostClient):
        self.client = client

    def create(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/flows', flow)


class TemplatesClient:
    def __init__(self, client: NotiBoostClient):
        self.client = client

    def create(self, template: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/templates', template)

    def list(self, **options: Any) -> Dict[str, Any]:
        query = '&'.join([f'{k}={v}' for k, v in options.items()])
        path = f'/api/v1/templates?{query}' if query else '/api/v1/templates'
        return self.client.request('GET', path)

    def get(self, template_id: str) -> Dict[str, Any]:
        return self.client.request('GET', f'/api/v1/templates/{template_id}')

    def update(self, template_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('PUT', f'/api/v1/templates/{template_id}', data)


class WebhooksClient:
    def __init__(self, client: NotiBoostClient):
        self.client = client

    def create(self, webhook: Dict[str, Any]) -> Dict[str, Any]:
        return self.client.request('POST', '/api/v1/webhooks', webhook)

