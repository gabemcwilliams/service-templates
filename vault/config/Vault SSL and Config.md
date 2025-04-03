# Vault SSL and Configuration

## Step 1: Store and Secure Certificates

Extract and copy certificate details from `multi_san_cert.txt` into separate files.

### Create the Vault certificate directory:
```sh
mkdir -p /mnt/data/swarm/certs/vault
cd /mnt/data/swarm/certs/vault
```

### Open the cert file for manual extraction:
```sh
nano multi_san_cert.txt
```

### Extract and copy the relevant sections:
```sh
nano ca_chain.crt    # Copy the CA chain
nano ca.crt          # Copy only the Root CA
nano private.key     # Copy the Private Key
nano public.crt      # Copy the Server Certificate
```

### Secure Certificate Permissions:
```sh
sudo chmod 600 private.key
sudo chmod 644 public.crt ca.crt ca_chain.crt
```

## Step 2: Configure Vault for TLS

Modify Vault's configuration file:
```sh
sudo nano /etc/vault.d/vault.hcl
```
Ensure the following settings:
```hcl
listener "tcp" {
  address = "0.0.0.0:8200"
  tls_cert_file = "/mnt/data/swarm/certs/vault/public.crt"
  tls_key_file = "/mnt/data/swarm/certs/vault/private.key"
  tls_client_ca_file = "/mnt/data/swarm/certs/vault/ca.crt"
}
```

### Restart Vault to Apply Changes:
```sh
sudo systemctl restart vault
```

---

**Next:** Proceed to [Nginx SSL and Configuration](#) to integrate Vault's certificates into Nginx.

