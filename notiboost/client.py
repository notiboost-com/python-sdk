import json
import time
import requests
from typing import Dict, List, Optional, Any
from .exceptions import NotiBoostException
from .resources import EventsClient, UsersClient, FlowsClient, TemplatesClient, WebhooksClient


class NotiBoostClient:
    def __init__(
        self,
        api_key: str,
        base_url: str = 'https://api.notiboost.com',
        timeout: int = 30,
        retries: int = 3
    ):
        if not api_key:
            raise ValueError('API key is required')

        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.retries = retries

        # Initialize resource clients
        self.events = EventsClient(self)
        self.users = UsersClient(self)
        self.flows = FlowsClient(self)
        self.templates = TemplatesClient(self)
        self.webhooks = WebhooksClient(self)

    def request(
        self,
        method: str,
        path: str,
        data: Optional[Dict] = None,
        options: Optional[Dict] = None
    ) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

        if options and 'headers' in options:
            headers.update(options['headers'])

        last_error = None
        for attempt in range(self.retries + 1):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    json=data if data else None,
                    headers=headers,
                    timeout=self.timeout
                )

                if response.status_code >= 200 and response.status_code < 300:
                    return response.json()
                elif response.status_code == 429 and attempt < self.retries:
                    # Rate limit - wait and retry
                    retry_after = int(response.headers.get('Retry-After', 1))
                    time.sleep(retry_after)
                    continue
                else:
                    error_data = response.json() if response.text else {}
                    raise NotiBoostException(
                        error_data.get('message', f'HTTP {response.status_code}'),
                        response.status_code,
                        error_data
                    )
            except requests.exceptions.RequestException as e:
                last_error = e
                if attempt < self.retries:
                    time.sleep(2 ** attempt)  # Exponential backoff
                    continue
                raise NotiBoostException(str(e), 0, {})

        raise last_error


