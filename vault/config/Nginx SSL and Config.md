# Nginx SSL and Configuration

## Step 1: Copy Certificates to Nginx
Ensure Vault-issued certificates are available for Nginx.

```sh
sudo cp /mnt/data/swarm/certs/vault/* /etc/nginx/certs/
```

## Step 2: Update Nginx Configuration
Modify `nginx.conf` to use the correct certificate paths.

```sh
sudo nano /etc/nginx/nginx.conf
```
Ensure the following SSL settings:

```nginx
ssl_certificate /etc/nginx/certs/public.crt;
ssl_certificate_key /etc/nginx/certs/private.key;
ssl_trusted_certificate /etc/nginx/certs/ca.crt;
```

## Step 3: Restart Nginx to Apply Changes

```sh
sudo systemctl restart nginx
sudo systemctl status nginx
```

Verify the SSL setup:
```sh
curl -v https://vault.example.internal --cacert /etc/nginx/certs/ca.crt
```

---

**Next:** Proceed to [MinIO SSL Configuration](#) to secure MinIO using Vault-issued certificates.

