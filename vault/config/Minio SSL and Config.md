# MinIO SSL and Configuration

## Step 1: Copy Vault-Issued Certificates to MinIO
MinIO expects its certificates to be stored in `/home/minio/.minio/certs/`.

```sh
sudo mkdir -p /home/minio/.minio/certs/CAs

# Copy main certificates
sudo cp /mnt/data/swarm/certs/vault/public.crt /home/minio/.minio/certs/public.crt
sudo cp /mnt/data/swarm/certs/vault/private.key /home/minio/.minio/certs/private.key

# Copy CA certificate for trusted verification
sudo cp /mnt/data/swarm/certs/vault/ca.crt /home/minio/.minio/certs/CAs/ca.crt
```

## Step 2: Set Correct Ownership and Permissions

```sh
sudo chown -R minio:minio /home/minio/.minio/certs
sudo chmod 600 /home/minio/.minio/certs/private.key
sudo chmod 644 /home/minio/.minio/certs/public.crt /home/minio/.minio/certs/CAs/ca.crt
```

## Step 3: Configure MinIO for SSL
Edit the MinIO environment file:
```sh
sudo nano /etc/default/minio
```
Ensure the following lines exist:
```sh
MINIO_SERVER_URL=https://minio.example.internal:9000
MINIO_CERT_FILE=/home/minio/.minio/certs/public.crt
MINIO_KEY_FILE=/home/minio/.minio/certs/private.key
```

## Step 4: Restart MinIO
```sh
sudo systemctl restart minio
sudo systemctl status minio
```

## Step 5: Verify HTTPS Connection
Run:
```sh
curl -v https://minio.example.internal:9000 --cacert /home/minio/.minio/certs/CAs/ca.crt
```
✔ If MinIO responds, it’s correctly using Vault-issued TLS certificates!

---

MinIO is now secured using Vault-issued SSL certificates.

