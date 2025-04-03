
## 🧠 Redis Service Overview

This service runs a standalone Redis instance intended for local development, internal caching, or testing infrastructure integrations.

---

### 🔧 Service Details

| Setting         | Value                  |
|----------------|------------------------|
| Image          | `redis:latest`         |
| Port           | `6379` (default Redis) |
| Network        | `redis` (bridge)       |
| IP Address     | `10.0.80.2`            |
| Container Name | `redis`                |

---

### 📦 Docker Compose Example

```yaml
services:
  redis:
    image: redis
    container_name: redis
    ports:
      - "6379:6379"
    networks:
      redis:
        ipv4_address: 10.0.80.2
    restart: unless-stopped

networks:
  redis:
    name: redis
    driver: bridge
    ipam:
      config:
        - subnet: "10.0.80.0/24"
```

---

### 🧪 Connection Test (Python)

Use this snippet to verify Redis connectivity:

```python
import redis

redis_host = '192.168.55.13'  # Or use the container hostname or DNS
redis_port = 6379

try:
    r = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
    r.set('test_key', 'Hello, Redis!')
    value = r.get('test_key')

    if value == 'Hello, Redis!':
        print("✅ Redis connection successful!")
    else:
        print("⚠️ Unexpected value:", value)

except Exception as e:
    print(f"❌ Error connecting to Redis: {e}")
finally:
    if r:
        r.close()
```

---

### 🔐 Security Notes

- No password or authentication is configured by default. **Do not expose this to the public internet.**
- Add `requirepass` in a custom `redis.conf` for production.

---

### 📎 Related Use Cases

- Caching layer for FastAPI / Flask
- Backend store for Celery
- Pub/Sub messaging
- Promtail logs buffering (Grafana stack)
