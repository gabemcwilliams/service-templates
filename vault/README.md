# Vault Service Overview

## Purpose

This setup provides a **locally hosted Vault instance** for secure secret management, configured to use:

- **S3 (MinIO)** as backend storage
- **AWS KMS** for auto-unseal
- TLS certificates (but optionally disabled for local testing)

## Key Features

- **UI Enabled**: Vault’s web UI is available at `http://vault.internal:8200`.
- **S3 Backend**: Secrets are stored in an object storage bucket (`vault`) managed by MinIO.
- **KMS Seal**: Automatically unseals Vault using AWS KMS (or a simulated KMS if mocked).
- **TLS Support**: SSL certificates are supported but disabled by default in this config.

---

## Configuration Summary

### Vault Settings

| Setting         | Value                              |
|-----------------|------------------------------------|
| `api_addr`      | `http://vault.internal:8200`       |
| `ui`            | `true`                             |
| `disable_mlock` | `true` (avoid using in production) |

---

### Storage (S3 via MinIO)

```hcl
storage "s3" {
  bucket              = "vault"
  access_key          = "PLACEHOLDER_ACCESS_KEY"
  secret_key          = "PLACEHOLDER_SECRET_KEY"
  endpoint            = "http://minio.internal:9000"
  scheme              = "https"
  s3_force_path_style = true
  disable_ssl         = true
}
```

> 📝 This config uses `disable_ssl = true` and `scheme = "https"` which can feel contradictory. It's fine for MinIO, but
> in prod you'd fix this.

---

### Listener

```hcl
listener "tcp" {
  address       = "0.0.0.0:8200"
  tls_cert_file = "/etc/vault.d/public.crt"
  tls_key_file  = "/etc/vault.d/private.key"
  tls_disable   = 1  # HTTP only. Don't do this outside your basement.
}
```

- `tls_disable = 1` makes this a **non-TLS** endpoint.
- Great for testing, terrible for production.

---

### Seal with AWS KMS

```hcl
seal "awskms" {
  region     = "us-west-2"
  kms_key_id = "PLACEHOLDER_KMS_KEY_ID"
  access_key = "PLACEHOLDER_KMS_ACCESS_KEY"
  secret_key = "PLACEHOLDER_KMS_SECRET_KEY"
  disabled   = false
}
```

- Automatically unseals Vault using AWS KMS.
- Replace placeholders with valid credentials and key ID.

---

### High Availability

```hcl
ha_enabled = true
```

- This turns on HA mode. Totally harmless in dev unless you're clustering Vault.

---

## Security Warnings (Because I Care)

- `disable_mlock = true`: Makes startup easier, but sacrifices security.
- `tls_disable = 1`: Just don't expose this outside Docker or localhost.
- Do not commit real keys in this config. Use env vars or templates.
- Avoid storing this file in plain text with real credentials.

---

## Launch Checklist

- ✅ Replace placeholders with actual secret values (or env var references).
- ✅ Configure your TLS certs (or don’t if you enjoy risk).
- ✅ Make sure MinIO and KMS are reachable.
- ✅ Initialize and unseal Vault (unless KMS takes care of it).

---

## Access Vault

```bash
VAULT_ADDR=http://vault.internal:8200 vault status
```

Or open in your browser: [http://vault.internal:8200](http://vault.internal:8200)
