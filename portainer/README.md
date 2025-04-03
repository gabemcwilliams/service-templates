# Portainer Setup and Configuration

## Overview
Portainer is a lightweight management UI that allows easy control of Docker environments, including standalone instances and Swarm clusters. This setup ensures secure access via Nginx reverse proxy and integrates into the `infra_dlc-saturn` infrastructure.

## Installation Guide
### Prerequisites
- Docker and Docker Compose installed
- Nginx reverse proxy configured
- `docker-compose.yaml` for managing the service

### Deployment with Docker Compose
The Portainer service is deployed using the following `docker-compose.yaml` file:

```yaml
name: utilities

networks:
  utilities:
    name: utilities
    driver: bridge
    ipam:
      driver: default
      config:
        - subnet: 10.0.5.0/24

services:
  portainer-enterprise:
    image: portainer/portainer-ee
    container_name: portainer-enterprise
    restart: unless-stopped
    ports:
      - "9100:9000"
    networks:
      utilities:
        ipv4_address: 10.0.5.100
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - "${storage}/portainer_data:/data"
    environment:
      - "PORTAINER_LICENSE_KEY=${PORTAINER_LICENSE_KEY}"

volumes:
  portainer_data:
```

### Deploying Portainer
```sh
docker compose up -d
```
This starts the Portainer container and exposes it on **port 9100**.

## Reverse Proxy Configuration (Nginx)
To securely expose Portainer, update the Nginx configuration to route requests correctly.

```nginx
server {
    listen 443 ssl http2;
    server_name portainer.data-automation.internal;

    ssl_certificate /etc/nginx/certs/public.crt;
    ssl_certificate_key /etc/nginx/certs/private.key;

    location / {
        proxy_pass http://127.0.0.1:9100/;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart Nginx to apply changes:
```sh
sudo systemctl restart nginx
```

## Accessing Portainer
Once the service is running, visit:
```
https://portainer.data-automation.internal/
```

The first login will prompt you to create an admin account.

## Troubleshooting
### 1. Portainer Not Accessible
- Ensure the container is running:
  ```sh
  docker ps | grep portainer
  ```
- Check logs for errors:
  ```sh
  docker logs portainer-enterprise
  ```
- Ensure Nginx is correctly forwarding requests:
  ```sh
  sudo journalctl -u nginx --no-pager | tail -n 50
  ```

### 2. Port Conflict
If another service is using **port 9000**, update the `docker-compose.yaml` to use an alternative port (e.g., **9100**), then restart Portainer and Nginx.

## Conclusion
Portainer is now deployed and accessible through the Nginx reverse proxy. This setup ensures secure access and easy container management.

