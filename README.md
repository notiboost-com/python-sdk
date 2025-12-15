# NotiBoost Python SDK

Official Python SDK for NotiBoost - Notification Orchestration Platform.

## Installation

```bash
pip install notiboost
```

## Requirements

- Python 3.7 or higher

## Quick Start

```python
from notiboost import NotiBoostClient
from datetime import datetime

client = NotiBoostClient(
    api_key='YOUR_API_KEY'
)

# Send an event
result = client.events.ingest({
    'event_name': 'order_created',
    'event_id': 'evt_001',
    'occurred_at': datetime.now().isoformat(),
    'user_id': 'u_123',
    'properties': {
        'order_id': 'A001',
        'amount': 350000
    }
})

print(f"Trace ID: {result['trace_id']}")
```

## API Reference

### Constructor

```python
NotiBoostClient(api_key, base_url=None, timeout=30, retries=3)
```

**Parameters:**
- `api_key` (str, required) - Your NotiBoost API key
- `base_url` (str, optional) - Custom API base URL (default: `https://api.notiboost.com`)
- `timeout` (int, optional) - Request timeout in seconds (default: `30`)
- `retries` (int, optional) - Number of retry attempts (default: `3`)

### Events

#### `events.ingest(event)`

Ingest a single event.

```python
result = client.events.ingest({
    'event_name': 'order_created',
    'event_id': 'evt_001',
    'occurred_at': datetime.now().isoformat(),
    'user_id': 'u_123',
    'properties': {
        'order_id': 'A001',
        'amount': 350000
    }
})
```

#### `events.ingest_batch(events)`

Ingest multiple events in a single request.

```python
result = client.events.ingest_batch([
    {
        'event_name': 'order_created',
        'event_id': 'evt_001',
        'user_id': 'u_123',
        'properties': {'order_id': 'A001'}
    },
    {
        'event_name': 'payment_success',
        'event_id': 'evt_002',
        'user_id': 'u_123',
        'properties': {'order_id': 'A001'}
    }
])
```

### Users

#### `users.create(user)`

Create a new user.

```python
client.users.create({
    'user_id': 'u_123',
    'name': 'Nguyễn Văn A',
    'email': 'user@example.com',
    'phone': '+84901234567',
    'properties': {
        'segment': 'vip',
        'preferred_channel': 'zns'
    }
})
```

#### `users.get(user_id)`

Get user by ID.

```python
user = client.users.get('u_123')
```

#### `users.update(user_id, data)`

Update user.

```python
client.users.update('u_123', {
    'name': 'Nguyễn Văn B'
})
```

#### `users.delete(user_id)`

Delete user.

```python
client.users.delete('u_123')
```

#### `users.set_channel_data(user_id, channel_data)`

Set channel data for user.

```python
client.users.set_channel_data('u_123', {
    'email': 'user@example.com',
    'phone': '+84901234567',
    'push_token': 'fcm_token_abc123',
    'push_platform': 'android',
    'zns_oa_id': '123456789'
})
```

#### `users.set_preferences(user_id, preferences)`

Set user notification preferences.

```python
client.users.set_preferences('u_123', {
    'channels': {
        'zns': {'enabled': True},
        'email': {'enabled': True},
        'sms': {'enabled': True},
        'push': {'enabled': True}
    },
    'categories': {
        'order': {'enabled': True},
        'marketing': {'enabled': False}
    }
})
```

#### `users.create_batch(users)`

Create multiple users in a single request.

```python
client.users.create_batch([
    {
        'user_id': 'u_123',
        'name': 'Nguyễn Văn A',
        'email': 'user1@example.com',
        'phone': '+84901234567'
    },
    {
        'user_id': 'u_124',
        'name': 'Trần Thị B',
        'email': 'user2@example.com',
        'phone': '+84901234568',
        'push_token': 'fcm_token_xyz789',
        'push_platform': 'ios'
    }
])
```

### Flows

#### `flows.create(flow)`

Create a notification flow.

```python
client.flows.create({
    'name': 'order_confirmation',
    'description': 'Send order confirmation via ZNS',
    'rules': [
        {
            'condition': "event_name == 'order_created'",
            'action': 'send_zns'
        }
    ],
    'channels': ['zns'],
    'template_id': 'tpl_order_confirm'
})
```

### Templates

#### `templates.create(template)`

Create a template.

```python
client.templates.create({
    'name': 'order_confirmation_zns',
    'channel': 'zns',
    'content': {
        'header': 'Xác nhận đơn hàng',
        'body': 'Đơn hàng {{order_id}} đã được xác nhận. Tổng tiền: {{amount}} VNĐ',
        'footer': 'Cảm ơn bạn đã mua sắm'
    },
    'variables': ['order_id', 'amount']
})
```

#### `templates.list(**options)`

List templates.

```python
templates = client.templates.list(channel='zns')
```

#### `templates.get(template_id)`

Get template by ID.

```python
template = client.templates.get('tpl_order_confirm')
```

#### `templates.update(template_id, data)`

Update template.

```python
client.templates.update('tpl_order_confirm', {
    'content': {
        'body': 'Updated body content'
    }
})
```

### Webhooks

#### `webhooks.create(webhook)`

Create a webhook.

```python
client.webhooks.create({
    'url': 'https://your-app.com/webhooks/notiboost',
    'events': ['message.sent', 'message.delivered', 'message.failed'],
    'secret': 'your_webhook_secret'
})
```

## Error Handling

```python
from notiboost.exceptions import NotiBoostException

try:
    client.events.ingest(event)
except NotiBoostException as e:
    if e.status_code == 429:
        # Rate limit exceeded
        print('Rate limit exceeded, retrying...')
    elif e.status_code == 401:
        # Invalid API key
        print('Invalid API key')
    else:
        print(f'Error: {e.message}')
```

## Idempotency

Use `Idempotency-Key` header for idempotent requests:

```python
client.events.ingest(event, headers={
    'Idempotency-Key': 'unique-key-12345'
})
```

## Best Practices

1. Use singleton pattern for client instance
2. Store API key in environment variables
3. Handle exceptions properly
4. Use idempotency keys for critical operations

